"""Offline Phase B acceptance cases, driven through the published routes."""

import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import httpx
from fastapi.testclient import TestClient

from commerce.app import app
from commerce.providers import (
    RULE,
    Blocked,
    Jev,
    SampleCatalog,
    SampleJudgment,
    Senso,
    Shopify,
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
        patch.object(adapter, "search", side_effect=lambda brief: [deepcopy(target)]).start()
        patch.object(adapter, "lookup", side_effect=lambda *args: deepcopy(target)).start()
        self.board()
        return target

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
            "checkout_url": "https://seller.example/buy/2?_gsid=demo",
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
                ("eligible", {"native_checkout": False}),
                ("source", "external"),
            ]:
                with patch.dict(variant, {field: value}):
                    self.assertIsNone(self.turn("source_jackets")["shortlist"]["winnerId"])
        with patch.object(adapter, "call", return_value={"products": []}):
            self.assertEqual(self.turn("source_jackets")["shortlist"]["offers"], [])

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
        self.turn("save_rule", RULE)
        self.assertEqual(self.view["memory"]["state"], "unavailable")

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
            self.assertEqual(adapter.recall("binding", RULE, "c", "n").contentId, "c")
            self.assertEqual(call.call_args.args[2]["content_ids"], ["c"])
            self.assertTrue(call.call_args.args[2]["require_scoped_ids"])
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
