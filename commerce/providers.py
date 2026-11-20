"""Task-scoped catalog, evidence and memory adapters."""

import hashlib
import json
import os
import re
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import httpx

from .contracts.models import Evidence, Offer, SensoRef

PROFILE = "https://shopify.dev/ucp/agent-profiles/examples/2026-08-25/valid-with-capabilities.json"
RULE = "I don’t buy final-sale items."
SAMPLE = Path(__file__).parent / "fixtures/demo.json"


class Blocked(Exception):
    """Safe provider status suitable for a buyer-facing response."""


def now():
    return datetime.now(UTC).isoformat(timespec="seconds")


def data(response):
    if not response.is_success:
        raise Blocked(f"Provider returned HTTP {response.status_code}.")
    return response.json()


def request(method, url, **kwargs):
    try:
        return httpx.request(method, url, timeout=8, **kwargs)
    except httpx.RequestError as exc:
        raise Blocked("Provider connection unavailable.") from exc


@dataclass
class Listing:
    offer: Offer
    item: Evidence
    condition: str | None
    checkout: str | None = None
    policy: Evidence | None = None
    policy_url: str | None = None
    list_minor: int | None = None
    policy_note: str | None = None

    def comparison_facts(self):
        # Exclude presentation, observation time and rotating attribution tokens.
        o = self.offer
        return (
            o.priceMinor,
            o.currency,
            o.available,
            o.size,
            o.market,
            o.origin,
            self.condition,
            self.list_minor,
            bool(self.checkout),
            self.policy_url,
            self.item.kind,
            self.item.origin,
            self.item.sellerId,
            self.item.variantId,
            self.item.market,
            self.item.quote,
        )


class SampleCatalog:
    def search(self, brief):
        fixture = json.loads(SAMPLE.read_text())
        result = []
        for raw in fixture["listings"]:
            offer = Offer(**raw["offer"], checks=[], outcome="unknown")
            item = Evidence.model_validate(raw["item"])
            policy = Evidence.model_validate(raw["policy"])
            result.append(Listing(offer, item, raw["condition"], policy=policy))
        return result


def seller_https(url, domain):
    if not isinstance(url, str) or any(c.isspace() or c in "\\\r\n" for c in url):
        return False
    try:
        p = urlsplit(url)
        return (
            p.scheme == "https"
            and p.hostname == domain
            and not p.username
            and not p.password
            and p.port in {443, None}
            and bool(domain)
        )
    except ValueError:
        return False


def size_key(label):
    """Normalize only explicit suit lengths. A bare chest measurement has no length."""
    value = label.strip().upper()
    match = re.fullmatch(r"(\d{2})[ -]*(REGULAR|REG|R|SHORT|S|LONG|L)", value)
    return match[1] + match[2][0] if match else value


def seller_link(url, seller):
    storefront = seller.get("url") or ""
    host = urlsplit(storefront).hostname
    return seller_https(url, seller.get("domain")) or (
        seller_https(storefront, host) and seller_https(url, host)
    )


def checkout_link(variant):
    link = variant.get("checkout_url")
    if not seller_link(link, variant["seller"]):
        return None
    parsed = urlsplit(link)
    if not any(k.startswith("attribution/") or k == "_gsid" for k in parse_qs(parsed.query)):
        return None
    if parsed.path.startswith("/buy/") or variant.get("eligible", {}).get("native_checkout") is not True:
        # Shopify's attributed seller redirect encodes the exact variant and quantity.
        variant_number = variant["id"].rsplit("/", 1)[-1]
        if not variant_number.isdecimal() or parsed.path != f"/buy/{variant_number}:1":
            return None
    return link


def official_policy(url, seller):
    if seller_link(url, seller):
        return True
    shop = seller["id"].rsplit("/", 1)[-1]
    return (
        shop.isdecimal()
        and seller_https(url, "checkout.shopify.com")
        and re.fullmatch(rf"/{shop}/policies/\d+\.html", urlsplit(url).path) is not None
    )


def search_candidates(products, brief):
    candidates = {}
    for product in products:
        labels = [
            value["label"]
            for option in product.get("options", [])
            if option["name"].lower() == "size"
            for value in option.get("values", [])
            if size_key(value["label"]) == size_key(brief.jacketSize)
        ]
        for variant in product.get("variants", []):
            seller = variant.get("seller", {}).get("id", "")
            vid = variant.get("id", "")
            if not seller.startswith("gid://shopify/Shop/") or not vid.startswith(
                "gid://shopify/ProductVariant/"
            ):
                continue
            sizes = [o["label"] for o in variant.get("options", []) if o["name"].lower() == "size"]
            direct = len(sizes) == 1 and size_key(sizes[0]) == size_key(brief.jacketSize)
            if direct:
                target, label = vid, sizes[0]
            elif labels and product.get("id", "").startswith("gid://shopify/p/"):
                target, label = product["id"], labels[0]
            else:
                continue
            price = variant.get("price") or {}
            comparable = price.get("currency") == brief.currency and isinstance(price.get("amount"), int)
            rank = (
                not comparable,
                comparable and price["amount"] > brief.jacketCapMinor,
                not bool(checkout_link(variant)),
                not direct,
                price["amount"] if comparable else 0,
            )
            key = (seller, target, label)
            if key not in candidates or rank < candidates[key]:
                candidates[key] = rank
    return sorted(candidates, key=candidates.get)


@dataclass(frozen=True)
class SearchContinuation:
    candidates: tuple[tuple[str, str, str], ...] = ()
    cursor: str | None = None


class Shopify:
    last_call = 0.0

    def call(self, name, catalog):
        time.sleep(max(0, 0.25 - (time.monotonic() - self.last_call)))
        self.last_call = time.monotonic()
        headers = {"Accept": "application/json, text/event-stream"}
        if token := os.getenv("SHOPIFY_CATALOG_TOKEN"):
            headers["Authorization"] = "Bearer " + token
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": {"meta": {"ucp-agent": {"profile": PROFILE}}, "catalog": catalog},
            },
        }
        response = request(
            "POST", "https://catalog.shopify.com/api/ucp/mcp", json=payload, headers=headers
        )
        if not response.is_success:
            raise Blocked(f"Shopify returned HTTP {response.status_code}.")
        try:
            if "text/event-stream" in response.headers.get("content-type", ""):
                obj = next(
                    json.loads(line[5:])
                    for line in response.text.splitlines()
                    if line.startswith("data:")
                )
            else:
                obj = response.json()
            result = obj["result"]
            if result.get("isError"):
                raise Blocked("Shopify could not resolve this request.")
            body = result.get("structuredContent") or json.loads(result["content"][0]["text"])
            ucp = body["ucp"]
            if (
                ucp.get("version") != "2026-08-25"
                or "dev.shopify.catalog.global" not in ucp["capabilities"]
            ):
                raise Blocked("Shopify catalog capabilities changed.")
            return body
        except (KeyError, ValueError, IndexError, TypeError, StopIteration) as exc:
            raise Blocked("Shopify returned an unreadable catalog response.") from exc

    def search_page(self, brief, cursor):
        pagination = {"limit": 40}
        if cursor:
            pagination["cursor"] = cursor
        response = self.call(
            "search_catalog",
            {
                "query": f"{brief.jacketSize} suit jacket sport coat blazer",
                "sources": ["shopify"],
                "context": {"address_country": brief.market, "currency": brief.currency},
                "filters": {
                    "condition": ["new"],
                    "available": True,
                    "price": {"max": brief.jacketCapMinor},
                    "ships_to": {"country": brief.market},
                },
                "pagination": pagination,
            },
        )
        page = response.get("pagination") or {}
        return search_candidates(response["products"], brief), page.get("cursor") if page.get(
            "has_next_page"
        ) else None

    def search_batch(self, brief, continuation):
        state = continuation or SearchContinuation()
        candidates, cursor = state.candidates, state.cursor
        if not candidates:
            candidates, cursor = self.search_page(brief, cursor)
        listings = {}
        for seller, target, label in candidates[:3]:
            row = self.lookup(brief, seller, target, label)
            if row:
                listings[row.offer.id] = row
        remaining = tuple(candidates[3:])
        next_search = SearchContinuation(remaining, cursor) if remaining or cursor else None
        return list(listings.values()), next_search

    def lookup(self, brief, seller_id, variant_id, size_label=None):
        by_product = variant_id.startswith("gid://shopify/p/")
        body = self.call(
            "get_product",
            {
                "id": variant_id,
                "selected": [{"name": "Size", "label": size_label or brief.jacketSize}],
                "filters": {"shops": [seller_id], "ships_to": {"country": brief.market}},
                "context": {"address_country": brief.market, "currency": brief.currency},
            },
        )
        product = body.get("product") or {}
        sizes = [o["label"] for o in product.get("selected", []) if o["name"].lower() == "size"]
        if by_product and product.get("id") != variant_id:
            return None
        if len(sizes) != 1 or size_key(sizes[0]) != size_key(brief.jacketSize):
            return None
        rows = []
        for v in product.get("variants", []):
            seller = v.get("seller", {})
            if (
                (not by_product and v.get("id") != variant_id)
                or not v.get("id", "").startswith("gid://shopify/ProductVariant/")
                or seller.get("id") != seller_id
                or v.get("source", "shopify") != "shopify"
            ):
                continue
            options = [o["label"] for o in v.get("options", []) if o["name"].lower() == "size"]
            price = v.get("price") or {}
            stock = (v.get("availability") or {}).get("available")
            if options != sizes:
                continue
            link = checkout_link(v)
            vid = v["id"]
            oid = hashlib.sha256((seller_id + "|" + vid).encode()).hexdigest()[:24]
            size = options[0]
            offer = Offer(
                id=oid,
                sellerId=seller_id,
                seller=seller["name"],
                variantId=vid,
                name=v.get("title") or product["title"],
                size=size,
                imageUrl=next(
                    (m.get("url") for m in product.get("media", []) if m.get("type") == "image"), None
                ),
                market=brief.market,
                available=stock,
                priceMinor=price.get("amount"),
                currency=price.get("currency"),
                origin="shopify_live",
                outcome="unknown",
                checks=[],
            )
            description = (v.get("description") or {}).get("plain", "")
            condition = (
                "new"
                if v.get("condition") == ["new"]
                else ("secondhand" if v.get("condition") == ["secondhand"] else None)
            )
            quote = f"Catalog fields: {offer.name}; size {size}; condition {condition}; available {stock}; {offer.priceMinor} minor units {offer.currency}. Description: {description}"
            item = Evidence(
                id="item-" + oid,
                kind="catalog_variant",
                origin="shopify_live",
                speaker=None,
                title=offer.name,
                quote=quote,
                sourceUrl=v.get("url"),
                sellerId=seller_id,
                variantId=vid,
                market=brief.market,
                observedAt=now(),
                senso=None,
            )
            policy_url = next(
                (
                    p["url"]
                    for p in seller.get("links", [])
                    if p.get("type") == "refund_policy" and official_policy(p.get("url"), seller)
                ),
                None,
            )
            lp = v.get("list_price") or {}
            rows.append(
                Listing(
                    offer,
                    item,
                    condition,
                    link,
                    policy_url=policy_url,
                    list_minor=lp.get("amount") if lp.get("currency") == offer.currency else None,
                )
            )

        def priority(row):
            o = row.offer
            comparable = o.currency == brief.currency and o.priceMinor is not None
            return (
                o.available is not True,
                row.condition != "new",
                not comparable,
                comparable and o.priceMinor > brief.jacketCapMinor,
                not bool(row.checkout),
                o.priceMinor if comparable else 0,
                o.id,
            )

        return min(rows, key=priority, default=None)


class Senso:
    namespace = "senso"

    def call(self, method, path, body=None):
        if not (key := os.getenv("SENSO_API_KEY")):
            raise Blocked("Senso credential unavailable.")
        response = request(
            method,
            "https://apiv2.senso.ai/api/v1" + path,
            json=body,
            headers={"X-API-Key": key, "X-Senso-Signals": "off"},
        )

        reasons = {
            401: "Check the server's SENSO_API_KEY (HTTP 401).",
            402: "Check available Senso credits (HTTP 402).",
            403: "Check knowledge-base access for this key (HTTP 403).",
            429: "Senso is rate limiting requests. Refresh later (HTTP 429).",
        }
        if response.status_code in reasons:
            raise Blocked(reasons[response.status_code])
        return response

    def bind(self, binding, text):
        title = "Travel Stylist " + binding
        res = self.call("POST", "/org/kb/raw", {"title": title, "text": binding + "\n" + text})
        if res.status_code == 409:
            duplicate = res.json()
            content = duplicate.get("content_id") or duplicate.get("id")
            node = duplicate.get("kb_node_id")
            if content and node and self.recall(binding, text, content, node):
                return content, node
            raise Blocked("Duplicate document without a verified buyer and passage binding.")
        body = data(res)
        return body["id"], body["kb_node_id"]

    def recall(self, binding, text, content, node):
        status = data(self.call("GET", "/org/kb/nodes/" + node))
        state = status["content"]["processing_status"]
        if state in {"pending", "processing", "queued"}:
            return None
        if state != "complete" or status.get("kb_node_id") != node:
            raise Blocked("Senso indexing or binding unavailable.")
        result = data(
            self.call(
                "POST",
                "/org/search/context",
                {"query": text, "content_ids": [content], "require_scoped_ids": True},
            )
        )
        for hit in result["results"]:
            passage = hit.get("chunk_text", "")
            if (
                hit.get("content_id") == content
                and hit.get("kb_node_id", node) == node
                and isinstance(passage, str)
                and passage.split() == (binding + "\n" + text).split()
            ):
                return SensoRef(
                    contentId=content,
                    kbNodeId=node,
                    versionId=hit.get("version_id"),
                    chunkId=hit.get("content_chunk_id"),
                    chunkIndex=hit.get("chunk_index"),
                )
        raise Blocked("Scoped retrieval did not verify this saved rule.")


class SampleMemory:
    namespace = "sample"

    def bind(self, binding, text):
        return "sample-content-" + binding, "sample-node-" + binding

    def recall(self, binding, text, content, node):
        if (content, node) != self.bind(binding, text):
            raise Blocked("Sample binding mismatch.")
        return SensoRef(
            contentId=content, kbNodeId=node, versionId="sample-v1", chunkId=None, chunkIndex=0
        )


class Jev:
    def judge(self, kind, state):
        if not (key := os.getenv("TYPESAFE_API_KEY") or os.getenv("JEV_API_KEY")):
            raise Blocked("Jev credential unavailable.")
        q = "return_verdict" if kind == "returns" else "formality_verdict"
        question = (
            "Use the catalog evidence, buyer rule and complete seller terms to decide whether this one item "
            "at its current price is returnable in the delivery market. Account for exceptions such as "
            "custom items and markdowns. Mark unresolved applicability or ambiguous exchange-only terms unknown."
            if kind == "returns"
            else "Does this jacket's description establish suitability for the formal event?"
        )
        body = data(
            request(
                "POST",
                "https://api.typesafe.ai/v1/systemone",
                headers={"Authorization": "Bearer " + key},
                json={
                    "model": "jev-latest",
                    "state": json.dumps(state),
                    "questions": {
                        "evidence_suffices": {
                            "type": "noul",
                            "instructions": "Is the supplied evidence sufficient, current, consistent and applicable to this exact requirement? "
                            + question,
                        },
                        q: {
                            "type": "choice",
                            "instructions": question,
                            "criteria": {
                                "meets": "Explicit support.",
                                "fails": "Explicit exclusion.",
                                "unknown": "Ambiguous, conflicting or absent evidence.",
                            },
                        },
                    },
                },
            )
        )
        answer = body["answers"][q]
        choice = answer["choice"]
        probability = answer["probabilities"].get(choice, 0)
        enough = body["answers"]["evidence_suffices"]["noul"]
        verdict = (
            choice
            if choice in ("meets", "fails") and 0.75 <= enough <= 1 and 0.75 <= probability <= 1
            else "unknown"
        )
        return (
            verdict,
            f"{body['model']}: sufficiency {enough}, {choice} probability {probability}, confidence {answer.get('confidence', 'unavailable')}.",
        )


class SampleJudgment:
    def judge(self, kind, state):
        text = state["quote"].lower()
        if kind == "formality":
            verdict = "meets" if "tailored jacket for formal dinners" in text else "unknown"
        else:
            allow = "can be returned" in text or "not final sale" in text
            deny = bool(re.search(r"(?<!not )\bis final sale\b", text))
            verdict = "unknown" if allow == deny else ("meets" if allow else "fails")
        return verdict, {
            "meets": "Supported by the cited passage.",
            "fails": "Excluded by the cited passage.",
            "unknown": "The passage does not resolve this requirement.",
        }[verdict]
