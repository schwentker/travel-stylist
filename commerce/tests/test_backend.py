"""Offline Phase B acceptance cases, driven through the published routes."""

import tempfile
import unittest
from contextlib import nullcontext
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import httpx
from fastapi.testclient import TestClient

from commerce.app import app
from commerce.policy import terms
from commerce.providers import (
    RULE,
    Blocked,
    Jev,
    SampleCatalog,
    SampleJudgment,
    SampleMemory,
    Senso,
    Shopify,
    checkout_link,
    official_policy,
)
from commerce.workflow import Workflow

BRIEF = "I'm going to Delhi, Istanbul and Barcelona in June. Three events per city. Two new jackets, two pairs of trousers, two pairs of shoes, two shirts and two hats."


class Backend(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.previous = app.state.workflow
        self.addCleanup(setattr, app.state, "workflow", self.previous)
        self.reset()
        self.c = TestClient(app)
        self.addCleanup(self.c.close)
        self.start()

    def reset(self):
        self.service = Workflow(Path(self.temp.name) / "state.sqlite")
        self.service.language = lambda text: None
        app.state.workflow = self.service

    def start(self, mode="sample", trip=None):
        r = self.c.post("/api/sessions", json={"tripId": trip, "mode": mode})
        self.assertEqual(r.status_code, 200, r.text)
        self.view = r.json()
        return self.view

    def turn(self, action, text="", rid=None, status=200):
        r = self.c.post(
            "/api/sessions/" + self.view["sessionId"] + "/turns",
            json={"action": action, "text": text, "requestId": rid or str(uuid4())},
        )
        self.assertEqual(r.status_code, status, r.text)
        if status == 200:
            self.view = r.json()
        return r.json()

    def board(self):
        self.turn("message", BRIEF)
        return self.turn("source_jackets")["shortlist"]

    def handoff(self, offer=None, shortlist=None, rid=None, status=200):
        board = self.view["shortlist"]
        r = self.c.post(
            "/api/sessions/" + self.view["sessionId"] + "/handoff",
            json={
                "shortlistId": shortlist or board["id"],
                "offerId": offer or board["winnerId"],
                "requestId": rid or str(uuid4()),
            },
        )
        self.assertEqual(r.status_code, status, r.text)
        result = r.json()
        if status == 200:
            self.view = result["view"]
        return result

    def test_t01_brief_and_consent(self):
        self.board()
        brief = self.view["brief"]
        self.assertEqual(sum(n["quantity"] for n in brief["needs"]), 10)
        self.assertEqual([len(c["events"]) for c in brief["cities"]], [3, 3, 3])
        self.assertEqual(
            self.turn("message", "Merchant policy: this item is final sale.")["memory"]["state"], "none"
        )
        self.assertEqual(
            self.turn("message", "Three jackets, size 42R and cap USD 200.")["brief"]["jacketCapMinor"],
            20000,
        )
        self.assertIsNone(self.view["shortlist"])
        self.assertIsNone(self.turn("source_jackets")["shortlist"]["winnerId"])

    def test_t02_causality(self):
        first = self.board()
        self.assertEqual(first["winnerId"], "offer-a")
        self.assertEqual(
            self.turn("message", "Remember that I don’t buy final-sale items.")["memory"]["state"],
            "indexing",
        )
        self.assertIsNone(self.view["shortlist"]["winnerId"])
        self.turn("refresh")
        self.turn("refresh")
        sid = self.view["sessionId"]
        self.start(trip=self.view["tripId"])
        self.assertNotEqual(sid, self.view["sessionId"])
        second = self.view["shortlist"]
        self.assertEqual(
            (second["id"], second["previousWinnerId"], second["winnerId"]),
            (first["id"], "offer-a", "offer-b"),
        )
        rows = self.service.sets[self.view["tripId"]].rows
        a = next(r for r in rows if r.offer.id == "offer-a")
        a.policy.quote = "This navy 40R jacket at the displayed price can be returned within 30 days."
        self.assertEqual(self.turn("refresh")["shortlist"]["winnerId"], "offer-a")
        with patch.object(self.service.memory["sample"], "recall", side_effect=Blocked("offline")):
            held = self.start(trip=self.view["tripId"])
            self.assertIsNone(held["shortlist"]["winnerId"])
            self.assertEqual(held["memory"]["state"], "unavailable")
        self.assertEqual(self.handoff("offer-c")["status"], "unavailable")

    def test_rule_removed_in_isolated_control(self):
        first = self.board()
        self.turn("save_rule", RULE)
        self.assertEqual(self.turn("refresh")["shortlist"]["winnerId"], "offer-b")
        self.service.db.execute("DELETE FROM rules WHERE mode='sample'")
        view = self.start(trip=self.view["tripId"])
        self.assertEqual(view["memory"]["state"], "none")
        self.assertEqual(view["shortlist"]["id"], first["id"])
        self.assertEqual(view["shortlist"]["winnerId"], "offer-a")

    def test_t03_isolation_receipts_restart(self):
        first = self.board()
        rid = str(uuid4())
        self.turn("save_rule", RULE, rid)
        self.turn("save_rule", RULE, rid)
        self.turn("save_rule", RULE)
        self.turn("message", BRIEF, rid, status=409)
        session, trip = self.view["sessionId"], self.view["tripId"]
        other = TestClient(app)
        self.assertEqual(
            other.post("/api/sessions", json={"mode": "sample", "tripId": trip}).status_code, 404
        )
        self.assertEqual(
            other.post(
                "/api/sessions/" + session + "/turns",
                json={"action": "refresh", "text": "", "requestId": str(uuid4())},
            ).status_code,
            404,
        )
        original = self.c
        self.c = other
        self.start()
        self.turn("save_rule", RULE)
        self.c = original
        bindings = self.service.db.execute("SELECT DISTINCT binding FROM rules").fetchall()
        self.assertEqual(len(bindings), 2)
        self.service.db.close()
        self.reset()
        v = self.start(trip=trip)
        self.assertIsNone(v["shortlist"])
        self.assertEqual(v["memory"]["state"], "ready")
        self.assertEqual(
            self.handoff("offer-a", first["id"], status=409)["error"]["code"], "STALE_SHORTLIST"
        )
        r = self.c.post(
            "/api/sessions/" + session + "/turns",
            json={"action": "source_jackets", "text": "", "requestId": str(uuid4())},
        )
        self.assertEqual(r.status_code, 409)

    def test_t04_policy_scope_exceptions(self):
        self.board()
        self.turn("save_rule", RULE)
        b = next(r for r in self.service.sets[self.view["tripId"]].rows if r.offer.id == "offer-b")
        original = b.policy.model_copy()
        for changes in [
            {"sellerId": "other"},
            {"market": "JP"},
            {"variantId": "other"},
            {"kind": "merchant_reply"},
            {"quote": "Under this expired policy, this jacket can be returned."},
            {"quote": "Full-price items only. This jacket can be returned."},
            {"quote": ""},
        ]:
            b.policy = original.model_copy(update=changes)
            self.assertIsNone(self.turn("refresh")["shortlist"]["winnerId"])
        b.policy = original.model_copy(
            update={
                "quote": "All items can be returned. Items discounted by 20% or more are final sale."
            }
        )
        for list_minor, expected in [(None, None), (27500, None), (27499, "offer-b")]:
            b.list_minor = list_minor
            self.assertEqual(self.turn("refresh")["shortlist"]["winnerId"], expected)

    def test_t05_judgment_and_missing_evidence(self):
        self.board()
        self.turn("save_rule", RULE)
        rows = self.service.sets[self.view["tripId"]].rows
        for r in rows:
            r.policy = None
        with patch.object(self.service.judge["sample"], "judge", wraps=SampleJudgment().judge) as judge:
            self.turn("refresh")
            self.assertFalse(any(call.args[0] == "returns" for call in judge.call_args_list))
        b = rows[0]
        b.policy = SampleCatalog().search(None)[0].policy
        for text, expected in [
            ("This jacket is not final sale.", "meets"),
            ("This jacket is final sale.", "fails"),
            ("This jacket can be returned. This jacket is final sale.", "unknown"),
            ("Ask the seller.", "unknown"),
        ]:
            b.policy.quote = text
            o = next(o for o in self.turn("refresh")["shortlist"]["offers"] if o["id"] == b.offer.id)
            self.assertEqual(o["checks"][-1]["verdict"], expected)
        with patch.object(self.service.judge["sample"], "judge", side_effect=Blocked("timeout")):
            self.assertEqual(self.turn("refresh")["providers"]["jev"], "unavailable")
            self.assertTrue(
                all(o["checks"][0]["verdict"] == "meets" for o in self.view["shortlist"]["offers"])
            )

    def live(self):
        self.start("live")
        self.service.judge["live"] = SampleJudgment()
        rows = SampleCatalog().search(None)
        target = next(r for r in rows if r.offer.id == "offer-b")
        target.offer.origin = "shopify_live"
        target.item.origin = "shopify_live"
        target.policy = None
        target.checkout = "https://seller.example/buy/40r?_gsid=fake"
        adapter = self.service.catalog["live"]
        self.addCleanup(patch.stopall)
        patch.object(
            adapter, "search_batch", side_effect=lambda brief, continuation: ([deepcopy(target)], None)
        ).start()
        patch.object(adapter, "lookup", side_effect=lambda *args: deepcopy(target)).start()
        self.board()
        return target

    def test_live_offer_requires_matching_catalog_evidence(self):
        self.live()
        row = self.service.sets[self.view["tripId"]].rows[0]
        item = row.item
        for fields in (
            {"origin": "sample"},
            {"kind": "merchant_reply"},
            {"sellerId": "other"},
            {"variantId": "other"},
            {"market": "JP"},
        ):
            with (
                self.subTest(fields=fields),
                patch.object(self.service.judge["live"], "judge", wraps=SampleJudgment().judge) as judge,
            ):
                row.item = item.model_copy(update=fields)
                board = self.turn("refresh")["shortlist"]
                self.assertIsNone(board["winnerId"])
                self.assertEqual(board["offers"][0]["outcome"], "unknown")
                self.assertNotIn(item.id, [doc["id"] for doc in self.view["evidence"]])
                self.assertIsNone(self.handoff(row.offer.id)["url"])
                judge.assert_not_called()

    def test_sample_policy_cannot_approve_live_offer(self):
        self.live()
        row = self.service.sets[self.view["tripId"]].rows[0]
        policy = next(r.policy for r in SampleCatalog().search(None) if r.offer.id == row.offer.id)
        row.policy_url = "https://seller.example/policies/refund"
        row.policy = policy.model_copy(update={"sourceUrl": row.policy_url})
        with patch.dict(self.service.memory, {"live": SampleMemory()}):
            self.turn("save_rule", RULE)
            with patch.object(
                self.service.judge["live"], "judge", wraps=SampleJudgment().judge
            ) as judge:
                view = self.turn("refresh")
                self.assertEqual(view["memory"]["state"], "ready")
                self.assertIsNone(view["shortlist"]["winnerId"])
                self.assertNotIn(policy.id, [doc["id"] for doc in view["evidence"]])
                self.assertFalse(any(call.args[0] == "returns" for call in judge.call_args_list))

    def test_stock_loss_invalidates_before_after_comparison(self):
        target = self.live()
        self.assertEqual(self.view["shortlist"]["winnerId"], target.offer.id)
        target.offer.available = False
        self.assertEqual(self.handoff()["status"], "unavailable")
        with patch.dict(self.service.memory, {"live": SampleMemory()}):
            self.turn("save_rule", RULE)
            board = self.start("live", trip=self.view["tripId"])["shortlist"]
            self.assertIsNone(board["previousWinnerId"])
            self.assertIsNone(board["changeNote"])

    def test_t06_live_lookup(self):
        adapter = Shopify()
        self.service.catalog["live"] = adapter
        self.start("live")
        self.turn("message", BRIEF)
        sv = "gid://shopify/Shop/1"
        vid = "gid://shopify/ProductVariant/2"
        variant = {
            "seller": {"id": sv, "name": "Synthetic", "domain": "seller.example"},
            "id": vid,
            "options": [{"name": "Size", "label": "40R"}],
            "price": {"amount": 17000, "currency": "USD"},
            "title": "New jacket",
            "description": {"plain": "New tailored jacket for formal dinners."},
            "condition": ["new"],
            "availability": {"available": True},
            "checkout_url": "https://seller.example/buy/2:1?_gsid=demo",
        }
        self.service.judge["live"] = SampleJudgment()

        def simulate(name, body):
            if name == "search_catalog":
                return {"products": [{"variants": [variant] * 4}]}
            return {"product": {"selected": variant["options"], "variants": [variant]}}

        with patch.object(adapter, "call", side_effect=simulate) as call:
            self.assertIsNotNone(self.turn("source_jackets")["shortlist"]["winnerId"])
            self.assertEqual(call.call_count, 2)
            for field, value in [
                ("options", [{"name": "Size", "label": "42R"}]),
                ("availability", {"available": False}),
                ("checkout_url", "https://seller.example/buy/3:1?_gsid=demo"),
                ("source", "external"),
            ]:
                with patch.dict(variant, {field: value}):
                    self.assertIsNone(self.turn("source_jackets")["shortlist"]["winnerId"])
        with patch.object(adapter, "call", return_value={"products": []}):
            self.assertEqual(self.turn("source_jackets")["shortlist"]["offers"], [])

    def test_search_selects_advertised_size_and_rechecks_pinned_variant(self):
        self.start("live")
        self.turn("message", BRIEF)
        self.service.judge["live"] = SampleJudgment()
        adapter = self.service.catalog["live"]
        seller = {
            "id": "gid://shopify/Shop/7",
            "name": "Synthetic",
            "domain": "s.myshopify.com",
            "url": "https://shop.example",
        }
        shop_policy = "https://checkout.shopify.com/7/policies/12.html"
        seller["links"] = [{"type": "refund_policy", "url": shop_policy}]
        regular = [{"name": "Size", "label": "40 Regular"}]
        small = [{"name": "Size", "label": "S"}]
        url = "https://shop.example/buy/23:1?attribution/utm_source=catalog&_gsid=abc%2Fdef"
        variant = {
            "id": "gid://shopify/ProductVariant/23",
            "seller": seller,
            "options": regular,
            "eligible": {"native_checkout": False},
            "checkout_url": url,
            "title": "Jacket",
            "description": {"plain": "New tailored jacket for formal dinners."},
            "condition": ["new"],
            "price": {"amount": 21000, "currency": "USD"},
            "availability": {"available": True},
        }
        group = "gid://shopify/p/group"
        listing = {
            "id": group,
            "variants": [dict(variant, options=small, id="gid://shopify/ProductVariant/22")],
            "options": [{"name": "Size", "values": [{"label": "40 Regular"}]}],
        }
        calls = []

        def simulate(name, req):
            calls.append(req)
            if name == "search_catalog":
                return {
                    "products": [{"variants": [dict(variant, options=small)]}] * 3 + [listing],
                    "pagination": {"has_next_page": True, "cursor": "next"},
                }
            self.assertIn(req["id"], (group, variant["id"]))
            self.assertEqual(req["selected"], regular)
            return {
                "product": {
                    "id": group,
                    "selected": regular,
                    "variants": [dict(variant, seller=dict(seller, id="gid://shopify/Shop/8")), variant],
                }
            }

        with patch.object(adapter, "call", side_effect=simulate):
            board = self.turn("source_jackets")["shortlist"]
            self.assertTrue(board["winnerId"])
            self.assertEqual(board["offers"][0]["variantId"], variant["id"])
            self.assertEqual(self.handoff()["url"], url)
            self.assertEqual([r.get("id") for r in calls], [None, group, variant["id"]])
            self.turn("source_jackets")
            self.assertEqual(calls[3]["pagination"]["cursor"], "next")
            grant = '<body class="page-policies">All items shipped to the United States can be returned within 30 days.</body>'

            def policy_response(*args, **kwargs):
                return nullcontext(
                    httpx.Response(200, text=grant, headers={"content-type": "text/html"})
                )

            with (
                patch.dict(self.service.memory, {"live": SampleMemory()}),
                patch("commerce.policy.httpx.stream", side_effect=policy_response),
            ):
                self.turn("save_rule", RULE)
                fresh = self.start("live", trip=self.view["tripId"])
                self.assertEqual(fresh["memory"]["state"], "ready")
                self.assertTrue(fresh["shortlist"]["winnerId"])
                self.assertEqual(self.handoff()["url"], url)
        self.assertTrue(official_policy(shop_policy, seller))
        self.assertFalse(official_policy(shop_policy.replace("/7/", "/8/"), seller))
        for bad in [
            url.replace("shop.example", "unrelated.example"),
            url.replace(":1?", ":2?"),
            url.replace("/23:", "/22:"),
            url.split("?")[0],
            url.replace("https:", "http:"),
        ]:
            self.assertIsNone(checkout_link(dict(variant, checkout_url=bad)))

    def test_hosted_policy_requires_market_scope_and_complete_terms(self):
        row = SampleCatalog().search(None)[0]
        row.policy_url = "https://checkout.shopify.com/7/policies/12.html"
        grant = "All items shipped to the United States can be returned within 30 days."
        form = '<a href="/returns">Return form</a>'
        for body, applicable in [
            (grant + form, True),
            ("All items can be returned. Our address is in the United States.", False),
            (grant + '<a href="/sale">Sale exclusions</a>', False),
        ]:
            html = '<body class="page-policies">' + body + "</body>"
            response = httpx.Response(200, text=html, headers={"content-type": "text/html"})
            with patch("commerce.policy.httpx.stream", return_value=nullcontext(response)):
                doc = terms(row)
            self.assertEqual(doc is not None, applicable)
            if doc:
                self.assertIn(grant, doc.quote)
                self.assertEqual(doc.variantId, row.offer.variantId)

    def test_t07_handoff(self):
        self.board()
        self.assertEqual(self.handoff()["status"], "sample")
        target = self.live()
        original = str(uuid4())
        self.assertEqual(self.handoff(rid=original)["url"], target.checkout)
        target.offer.priceMinor += 300
        rid = str(uuid4())
        for _ in range(2):
            res = self.handoff(rid=rid)
            self.assertEqual((res["status"], res["url"]), ("changed", None))
        self.assertEqual(self.handoff(rid=original)["status"], "changed")
        self.assertEqual(self.handoff()["status"], "ready")
        target.checkout = None
        self.assertEqual(self.handoff()["status"], "unavailable")
        self.handoff("unknown", status=404)
        self.service.sets[self.view["tripId"]].expires = 0
        self.assertEqual(self.handoff("offer-b", status=409)["error"]["code"], "STALE_SHORTLIST")

    def test_t08_price_and_provider_failures(self):
        self.board()
        row = next(r for r in self.service.sets[self.view["tripId"]].rows if r.offer.id == "offer-a")
        for price, currency, expected in [
            (0, "USD", "meets"),
            (None, "USD", "unknown"),
            (0, "JPY", "unknown"),
        ]:
            row.offer.priceMinor = price
            row.offer.currency = currency
            o = next(o for o in self.turn("refresh")["shortlist"]["offers"] if o["id"] == "offer-a")
            self.assertEqual(next(c["verdict"] for c in o["checks"] if c["id"] == "price"), expected)
        updated = self.turn("message", "Set cap JPY 22000.")["brief"]
        self.assertEqual((updated["jacketCapMinor"], updated["currency"]), (22000, "JPY"))
        self.start("live")
        self.turn("message", BRIEF)
        for status in [401, 429, 503]:
            with patch("commerce.providers.request", return_value=httpx.Response(status)):
                v = self.turn("source_jackets")
                self.assertEqual(v["providers"]["catalog"], "unavailable")
        with patch.dict("os.environ", {"SENSO_API_KEY": ""}):
            self.turn("save_rule", RULE)
        self.assertEqual(self.view["memory"]["state"], "unavailable")
        self.assertIn("credential unavailable", self.view["reply"])

    def test_cap_symbols_and_grouped_amounts(self):
        self.board()
        for cap, expected in [
            ("¥22,000", ("JPY", 22000)),
            ("€220.50", ("EUR", 22050)),
            ("GBP 1,200.25", ("GBP", 120025)),
            ("CAD $1,200", ("CAD", 120000)),
        ]:
            brief = self.turn("message", "Set cap " + cap + ".")["brief"]
            self.assertEqual((brief["currency"], brief["jacketCapMinor"]), expected)
        for cap in ("JPY 20.50", "USD 12,00", "GBP €30"):
            self.turn("message", "Set cap " + cap + ".", status=422)

    def test_scoped_senso(self):
        adapter = Senso()
        ref = {"content_id": "c", "kb_node_id": "n", "chunk_text": "binding\n" + RULE}
        responses = [
            httpx.Response(202, json={"id": "c", "kb_node_id": "n"}),
            httpx.Response(200, json={"kb_node_id": "n", "content": {"processing_status": "complete"}}),
            httpx.Response(200, json={"results": [ref]}),
        ]
        with patch.object(adapter, "call", side_effect=responses) as call:
            self.assertEqual(adapter.bind("binding", RULE), ("c", "n"))
            found = adapter.recall("binding", RULE, "c", "n")
            self.assertEqual((found.contentId, found.kbNodeId), ("c", "n"))
            self.assertIsNone(found.versionId)
            self.assertIsNone(found.chunkId)
            self.assertIsNone(found.chunkIndex)
            self.assertEqual(call.call_args.args[2]["content_ids"], ["c"])
            self.assertTrue(call.call_args.args[2]["require_scoped_ids"])
        for passage in ("binding\nWithdrawn: " + RULE, "binding\n" + RULE + " That rule is cancelled."):
            hit = dict(ref, chunk_text=passage)
            response = httpx.Response(200, json={"results": [hit]})
            with (
                patch.object(adapter, "call", side_effect=[responses[1], response]),
                self.assertRaises(Blocked),
            ):
                adapter.recall("binding", RULE, "c", "n")
        exact = dict(ref, version_id="v7", content_chunk_id="chunk-42", chunk_index=2)
        hit = httpx.Response(200, json={"results": [exact]})
        with patch.object(adapter, "call", side_effect=[responses[1], hit]):
            found = adapter.recall("binding", RULE, "c", "n")
            self.assertEqual((found.versionId, found.chunkId, found.chunkIndex), ("v7", "chunk-42", 2))
        for field in ("content_id", "kb_node_id"):
            wrong = httpx.Response(200, json={"results": [dict(ref, **{field: "other"})]})
            with (
                patch.object(adapter, "call", side_effect=[responses[1], wrong]),
                self.assertRaises(Blocked),
            ):
                adapter.recall("binding", RULE, "c", "n")
        for status in [402, 409]:
            with (
                patch.object(adapter, "call", return_value=httpx.Response(status, json={})),
                self.assertRaises(Blocked),
            ):
                adapter.bind("binding", RULE)
        with patch.object(
            adapter,
            "call",
            return_value=httpx.Response(200, json={"content": {"processing_status": "processing"}}),
        ):
            self.assertIsNone(adapter.recall("binding", RULE, "c", "n"))

    def test_jev_thresholds(self):
        for enough, probability, expected in [
            (0.75, 0.75, "meets"),
            (0.74, 0.99, "unknown"),
            (0.99, 0.74, "unknown"),
        ]:
            answer = {
                "model": "test",
                "answers": {
                    "evidence_suffices": {"noul": enough},
                    "return_verdict": {
                        "choice": "meets",
                        "probabilities": {"meets": probability},
                        "confidence": 0.99,
                    },
                },
            }
            with (
                patch.dict("os.environ", {"JEV_API_KEY": "synthetic"}),
                patch("commerce.providers.request", return_value=httpx.Response(200, json=answer)),
            ):
                self.assertEqual(Jev().judge("returns", {"quote": "synthetic"})[0], expected)

    def test_invalid_language_response_keeps_guided_input(self):
        from commerce.language import parse

        self.start("live")
        self.service.language = parse
        with patch("commerce.language.generate", side_effect=ValueError("invalid model output")):
            view = self.turn("message", BRIEF)
        self.assertEqual(view["providers"]["language"], "guided")
        self.assertEqual(view["brief"]["month"], "June")

    def test_duplicate_content_requires_exact_binding(self):
        adapter = Senso()
        conflict = httpx.Response(409, json={"content_id": "doc", "kb_node_id": "node"})
        node = httpx.Response(
            200, json={"kb_node_id": "node", "content": {"processing_status": "complete"}}
        )
        for marker in ("ours", "other"):
            hit = httpx.Response(
                200,
                json={
                    "results": [
                        {"content_id": "doc", "kb_node_id": "node", "chunk_text": marker + "\n" + RULE}
                    ]
                },
            )
            with patch.object(adapter, "call", side_effect=[conflict, node, hit]):
                if marker == "other":
                    with self.assertRaises(Blocked):
                        adapter.bind("ours", RULE)
                else:
                    self.assertEqual(adapter.bind("ours", RULE), ("doc", "node"))
