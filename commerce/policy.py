"""Read a complete same-seller Shopify policy body transiently. Fail closed on incomplete scope."""

import re
from html.parser import HTMLParser
from urllib.parse import urlsplit

import httpx

from .providers import Evidence, now


class PolicyBody(HTMLParser):
    def __init__(self, hosted=False, shop_id=None):
        super().__init__()
        self.hosted = hosted
        self.shop_id = shop_id
        self.container = "body" if hosted else "div"
        self.depth = 0
        self.complete = False
        self.referenced = False
        self.parts = []
        self.anchor = None
        self.ui_span = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        marker = "page-policies" if self.hosted else "shopify-policy__body"
        if not self.depth and tag == self.container and marker in attrs.get("class", "").split():
            self.depth = 1
        elif self.depth and tag == self.container:
            self.depth += 1
        if not self.depth:
            return
        if tag == "a":
            self.anchor = []
            self.href = attrs.get("href") or ""
        elif tag in ("iframe", "script", "img"):
            self.referenced = True
        elif self.hosted and tag == "span" and "visually-hidden" in attrs.get("class", "").split():
            self.ui_span = attrs.get("id") in {
                "forwarding-external-new-window-message",
                "forwarding-new-window-message",
                "forwarding-external-message",
                "checkout-context-step-one",
            }

    def handle_endtag(self, tag):
        if tag == "span":
            self.ui_span = False
        if tag == "a" and self.anchor is not None:
            action = " ".join(" ".join(self.anchor).lower().split())
            if not self.is_action_link(action):
                self.referenced = True
            self.anchor = None
        if self.depth and tag == self.container:
            self.depth -= 1
            if self.depth == 0:
                self.complete = True

    def is_action_link(self, label):
        if self.href.lower().startswith(("mailto:", "tel:")) or label in {
            "return form",
            "start your return or exchange",
            "report an issue",
        }:
            return True
        # Hosted policies can link to the buyer's Shopify account to start a return.
        # A separate policy/exclusions page still makes the extracted terms incomplete.
        link = urlsplit(self.href)
        return (
            self.shop_id is not None
            and self.shop_id.isdecimal()
            and link.scheme == "https"
            and link.netloc == "shopify.com"
            and link.path.rstrip("/") == f"/{self.shop_id}/account"
            and re.fullmatch(r"(?:online )?return form(?:\s*\(orders?\s*(?:->|→)\s*returns?\))?", label)
            is not None
        )

    def handle_data(self, text):
        if self.depth and not self.ui_span and text.strip():
            self.parts.append(text.strip())
            if self.anchor is not None:
                self.anchor.append(text.strip())


def terms(row):
    def unavailable(reason):
        row.policy_note = reason

    row.policy_note = None
    url = row.policy_url
    if not url:
        return unavailable("Shopify did not provide an official return-policy link for this seller.")
    # Only the official refund-policy URL from the exact seller lookup reaches this function.
    try:
        with httpx.stream("GET", url, timeout=4, follow_redirects=False) as response:
            if response.status_code != 200 or "html" not in response.headers.get("content-type", ""):
                return unavailable(
                    f"The official policy could not be read as HTML (HTTP {response.status_code})."
                )
            content = bytearray()
            for chunk in response.iter_bytes():
                content.extend(chunk)
                if len(content) > 800000:
                    return unavailable("The official policy exceeded the reading limit.")
        parser = PolicyBody(
            hosted=urlsplit(url).hostname == "checkout.shopify.com",
            shop_id=row.offer.sellerId.rsplit("/", 1)[-1],
        )
        parser.feed(content.decode("utf-8"))
        parser.close()
    except (httpx.HTTPError, UnicodeError, ValueError):
        return unavailable("The official return policy could not be retrieved.")
    quote = " ".join(parser.parts)
    if not parser.complete or not 0 < len(quote) <= 10000:
        return unavailable("The complete official return-policy text could not be extracted.")
    if parser.referenced:
        return unavailable(
            "The policy references additional material whose exceptions need verification."
        )
    market = row.offer.market
    markers = {
        "US": r"United States|U\.S\.?|(?-i:US)|USA",
        "CA": r"Canada",
        "GB": r"United Kingdom",
        "JP": r"Japan",
    }
    country = markers.get(market, r"(?!)")
    # Require an order/returns scope. A merchant mailing address alone proves nothing about coverage.
    market_scope = (
        rf"\b(?:orders?|purchases?|items?|products?|customers?|returns?)\s+"
        rf"(?:(?:shipped|delivered|placed|purchased)\s+)?(?:in|within|to|from)\s+(?:the\s+)?(?:{country})\b"
        rf"|\b(?:{country})\s+(?:orders?|purchases?|customers?|returns?)\b"
        r"|\ball (?:orders|purchases|items|products) (?:shipped |delivered )?worldwide\b"
    )
    # A direct grant to the buyer in the seller's official policy can apply storewide.
    # Jev must still establish that the exact current purchase satisfies every condition.
    buyer_grant = re.search(
        r"\byou (?:may|can) return your (?:purchase|order|items?|products?)\b",
        quote,
        re.IGNORECASE,
    )
    regional_terms = re.search(
        r"\b(?:domestic|international(?:ly)?|territor(?:y|ies)|residents? of)\b"
        r"|\b(?:orders?|purchases?|returns?|deliveries|shipments?|customers?)\s+"
        r"(?:(?:placed|shipped|delivered)\s+)?(?:within|outside|in|from|to)\s+(?!\d|a week|a month)"
        r"|\b(?:orders?|customers?|addresses|deliveries|countries|regions?) only\b"
        r"|\b(?:valid|available|applicable|applies)(?: only)? (?:in|within|outside)\b"
        r"|\bonly (?:in|within|from|available to)\b",
        quote,
        re.IGNORECASE,
    )
    if not re.search(market_scope, quote, re.IGNORECASE) and (not buyer_grant or regional_terms):
        if re.search(r"\b(?:exchange|store credit)[- ]only\b", quote, re.IGNORECASE):
            return unavailable(
                f"The policy describes exchange-only or credit-only terms. Eligibility for a return on this {market} purchase is unverified."
            )
        return unavailable(
            f"The official terms do not establish a return policy covering the {market} purchase."
        )
    specific = row.offer.name.casefold() in quote.casefold()
    if not (
        specific
        or buyer_grant
        or re.search(
            r"\b(?:all|any) (?:our )?(?:items|orders|products|purchases|(?:unworn and unaltered )?clothing)\b",
            quote,
            re.IGNORECASE,
        )
    ):
        return unavailable(
            "The policy does not establish coverage for this jacket or a storewide purchase."
        )
    # Keep unresolved effective windows on hold. Ordinary exceptions belong in the evidence.
    if re.search(r"effective|until|\b20\d{2}\b", quote, re.IGNORECASE):
        return unavailable("The policy has a date or validity window that needs verification.")
    markdown_unknown = (
        row.list_minor is None or row.offer.priceMinor is None or row.list_minor < row.offer.priceMinor
    )
    if markdown_unknown and re.search(
        r"discount|markdown|sale price|sale items|% off", quote, re.IGNORECASE
    ):
        return unavailable(
            "The policy has sale restrictions, and this variant’s markdown status is unverified."
        )
    return Evidence(
        id="terms-" + row.offer.id,
        kind="merchant_policy",
        origin="merchant",
        speaker=None,
        title="Official return policy",
        quote=quote,
        sourceUrl=url,
        sellerId=row.offer.sellerId,
        variantId=row.offer.variantId,
        market=market,
        observedAt=now(),
        senso=None,
    )


def discount_gate(quote, row):
    """An explicit inclusive final-sale threshold overrides a general returns clause."""
    match = re.search(
        r"(?:discounted|marked down) (?:by )?(?:at least (\d{1,3})% |(\d{1,3})% or more )(?:are|is) final sale",
        quote,
        re.IGNORECASE,
    )
    if not match:
        return None
    original, current = row.list_minor, row.offer.priceMinor
    if not isinstance(original, int) or original <= 0 or current is None or current > original:
        return "unknown"
    if 100 * (original - current) >= int(match[1] or match[2]) * original:
        return "fails"
    return None
