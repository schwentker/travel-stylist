"""Single-worker demo runtime. Durable buyer records and transient catalog state."""

import hashlib
import json
import os
import re
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException

from .brief import GUIDE, edit, explicit_save
from .contracts.models import Brief, Check, Evidence, Memory, Providers, Shortlist, View
from .documents import provision, seed
from .language import parse
from .policy import discount_gate, terms
from .providers import (
    RULE,
    Blocked,
    Jev,
    SampleCatalog,
    SampleJudgment,
    SampleMemory,
    SearchContinuation,
    Senso,
    Shopify,
    now,
    size_key,
)


def fail(status, code, message):
    raise HTTPException(status, (code, message))


@dataclass
class Cohort:
    rows: list
    continuity: str
    id: str = field(default_factory=lambda: str(uuid4()))
    observed: str = field(default_factory=now)
    expires: float = field(default_factory=lambda: time.monotonic() + 1800)
    baseline: str | None = None
    baseline_saved: bool = False
    comparison_valid: bool = True
    next_search: SearchContinuation | None = None


class Workflow:
    def __init__(self, database=None):
        self.path = database or os.environ.get("COMMERCE_DB", "commerce/runtime/state.sqlite3")
        self.lock = threading.RLock()
        self.sets = {}
        self.catalog = {"sample": SampleCatalog(), "live": Shopify()}
        self.memory = {"sample": SampleMemory(), "live": Senso()}
        self.judge = {"sample": SampleJudgment(), "live": Jev()}
        self.language = parse
        self.db = None

    def connect(self):
        if self.db is None:
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
            self.db = sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)
            self.db.row_factory = sqlite3.Row
            self.db.executescript("""
              CREATE TABLE IF NOT EXISTS trips(id TEXT PRIMARY KEY, buyer TEXT, mode TEXT, brief TEXT, searched INTEGER DEFAULT 0);
              CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, trip TEXT);
              CREATE TABLE IF NOT EXISTS sources(binding TEXT PRIMARY KEY, content TEXT, node TEXT);
              CREATE TABLE IF NOT EXISTS rules(buyer TEXT, mode TEXT, binding TEXT UNIQUE, content TEXT, node TEXT, PRIMARY KEY(buyer,mode));
              CREATE TABLE IF NOT EXISTS receipts(session TEXT, id TEXT, fingerprint TEXT, outcome TEXT, PRIMARY KEY(session,id));
            """)
        # Prune all expired cohorts even if their original buyer never returns.
        for key in [k for k, v in self.sets.items() if v.expires <= time.monotonic()]:
            del self.sets[key]
        return self.db

    def start(self, buyer, req):
        db = self.connect()
        if req.tripId is None:
            tid = str(uuid4())
            db.execute("INSERT INTO trips(id,buyer,mode) VALUES(?,?,?)", (tid, buyer, req.mode))
        else:
            tid = req.tripId
        trip = db.execute(
            "SELECT * FROM trips WHERE id=? AND buyer=? AND mode=?", (tid, buyer, req.mode)
        ).fetchone()
        if not trip:
            fail(404, "UNKNOWN_TRIP", "Trip not found for this buyer and mode.")
        sid = str(uuid4())
        db.execute("INSERT INTO sessions VALUES(?,?)", (sid, tid))
        return self.view(trip, sid)

    def context(self, buyer, sid):
        db = self.connect()
        trip = db.execute(
            "SELECT trips.* FROM sessions JOIN trips ON trips.id=sessions.trip WHERE sessions.id=? AND buyer=?",
            (sid, buyer),
        ).fetchone()
        if not trip:
            fail(404, "UNKNOWN_SESSION", "Open a new session for this trip.")
        return trip

    def recall(self, trip, providers, pending=False):
        buyer, mode = trip["buyer"], trip["mode"]
        row = self.db.execute("SELECT * FROM rules WHERE buyer=? AND mode=?", (buyer, mode)).fetchone()
        if row is None:
            return Memory(state="none", ruleText=None, evidenceId=None), None, None
        binding = row["binding"]
        try:
            adapter = self.memory[mode]
            content, node = row["content"], row["node"]
            if not content:
                content, node = adapter.bind(binding, RULE)
                self.db.execute(
                    "UPDATE rules SET content=?,node=? WHERE binding=?", (content, node, binding)
                )
            ref = None if pending else adapter.recall(binding, RULE, content, node)
            providers.senso = mode
            if ref is None:
                return (
                    Memory(state="indexing", ruleText=RULE, evidenceId=None),
                    None,
                    "Senso is indexing the saved rule. Refresh trip to check again.",
                )
            doc = Evidence(
                id="rule-" + binding,
                kind="buyer_rule",
                origin="sample" if mode == "sample" else "buyer",
                title="Saved buyer rule",
                quote=RULE,
                sourceUrl=None,
                speaker=None,
                sellerId=None,
                variantId=None,
                market=None,
                observedAt=now(),
                senso=ref,
            )
            return Memory(state="ready", ruleText=RULE, evidenceId=doc.id), doc, None
        except (Blocked, ValueError, KeyError, TypeError) as exc:
            reason = str(exc) if isinstance(exc, Blocked) else "Unexpected provider response."
            providers.senso = "unavailable"
            return (
                Memory(state="unavailable", ruleText=RULE, evidenceId=None),
                None,
                f"Saved-rule recall is on hold. Senso reported: {reason}",
            )

    def assess(self, row, brief, memory, rule, mode, providers, buyer):
        o = row.offer.model_copy(deep=True)
        docs = [row.item]
        checks = []

        def check(key, label, test, reason, ids):
            verdict = "unknown" if test is None else ("meets" if test else "fails")
            checks.append(Check(id=key, label=label, verdict=verdict, reason=reason, evidenceIds=ids))

        source = row.item
        origin = "shopify_live" if mode == "live" else "sample"
        if not (
            source.kind == "catalog_variant"
            and source.origin == o.origin == origin
            and source.sellerId == o.sellerId
            and source.variantId == o.variantId
            and source.market == o.market
        ):
            check(
                "catalog",
                "Catalog evidence",
                None,
                "Missing catalog evidence for this seller, variant and market.",
                [],
            )
            o.checks = checks
            o.outcome = "unknown"
            return o, []

        item = [row.item.id]
        check(
            "condition",
            "Condition",
            None if row.condition is None else row.condition == "new",
            f"Listed condition: {row.condition or 'unknown'}.",
            item,
        )
        check(
            "size",
            "Exact size",
            None if o.size is None else size_key(o.size) == size_key(brief.jacketSize),
            f"Requested {brief.jacketSize}, listed {o.size or 'unknown'}.",
            item,
        )
        check("stock", "Availability", o.available, "Current variant availability.", item)
        comparable = o.priceMinor is not None and o.currency == brief.currency
        check(
            "price",
            "Unit budget",
            o.priceMinor <= brief.jacketCapMinor if comparable else None,
            "Per-jacket cap in the delivery currency.",
            item,
        )
        check(
            "market",
            "Delivery market",
            o.market == brief.market,
            "Offer scoped to " + o.market + ".",
            item,
        )
        if mode == "live":
            check(
                "checkout",
                "Seller checkout",
                bool(row.checkout),
                "Verified attributed checkout for this seller and variant."
                if row.checkout
                else "No verified checkout link for this seller and variant.",
                item,
            )

        def semantic(key, label, doc, ids):
            state = {
                "seller": o.sellerId,
                "variant": o.variantId,
                "market": brief.market,
                "priceMinor": o.priceMinor,
                "currency": o.currency,
                "listPriceMinor": row.list_minor,
                "rule": RULE if key == "returns" else None,
                "quote": doc.quote,
                "evidenceIds": ids,
            }
            if key == "returns":
                state.update(
                    catalogEvidence=row.item.quote,
                    quantity=1,
                    condition=row.condition,
                    selectedSize=o.size,
                    available=o.available,
                )
            if row.list_minor and comparable and 0 <= o.priceMinor <= row.list_minor:
                state["discountNumerator"] = 100 * (row.list_minor - o.priceMinor)
                state["discountDenominator"] = row.list_minor
            try:
                verdict, reason = self.judge[mode].judge(key, state)
                if providers.jev != "unavailable":
                    providers.jev = mode
            except (Blocked, KeyError, ValueError, TypeError):
                providers.jev = "unavailable"
                verdict, reason = "unknown", "Judgment provider unavailable."
            checks.append(Check(id=key, label=label, verdict=verdict, reason=reason, evidenceIds=ids))

        if row.item.quote.strip():
            semantic("formality", "Formality", row.item, item)
        else:
            check("formality", "Formality", None, "No variant description.", [])
        if memory.state != "none":
            policy = row.policy
            valid = (
                policy
                and rule
                and policy.quote.strip()
                and not re.search(
                    r"expired|superseded|previous policy|full[- ]price (?:items )?only|valid until",
                    policy.quote,
                    re.IGNORECASE,
                )
                and (mode == "sample" or (row.policy_url and policy.sourceUrl == row.policy_url))
                and policy.sellerId == o.sellerId
                and policy.variantId == o.variantId
                and policy.market == o.market == brief.market
                and policy.origin == ("sample" if mode == "sample" else "merchant")
                and policy.kind == ("sample_policy" if mode == "sample" else "merchant_policy")
            )
            if valid and mode == "sample":
                try:
                    adapter = self.memory[mode]
                    binding, content, node = provision(
                        self.db, adapter, buyer, mode, policy.model_dump()
                    )
                    ref = adapter.recall(binding, policy.quote, content, node)
                    valid = ref is not None
                    policy = policy.model_copy(update={"senso": ref})
                except (Blocked, ValueError, KeyError, TypeError):
                    valid = False
                    providers.senso = "unavailable"
            if valid:
                docs.append(policy)
                refs = [rule.id, policy.id, row.item.id]
                gated = discount_gate(policy.quote, row)
                if gated:
                    checks.append(
                        Check(
                            id="returns",
                            label="Returnability",
                            verdict=gated,
                            reason="The applicable markdown threshold excludes this price or lacks a comparable list price.",
                            evidenceIds=refs,
                        )
                    )
                else:
                    semantic("returns", "Returnability", policy, refs)
            else:
                check(
                    "returns",
                    "Returnability",
                    None,
                    "Waiting for verified recall of the saved rule."
                    if not rule
                    else row.policy_note
                    or "The official terms do not establish returnability for this variant, market and price.",
                    [],
                )
        o.checks = checks
        verdicts = {c.verdict for c in checks}
        o.outcome = "fails" if "fails" in verdicts else ("unknown" if "unknown" in verdicts else "meets")
        return o, docs

    def view(self, trip, sid, reply=None, pending=False, catalog_failed=False, language="guided"):
        mode = trip["mode"]
        providers = Providers(catalog="unused", senso="unused", jev="unused", language=language)
        memory, rule, memory_note = self.recall(trip, providers, pending)
        docs = [rule] if rule else []
        brief = Brief.model_validate_json(trip["brief"]) if trip["brief"] else None
        if brief:
            docs.append(
                Evidence(
                    id="brief-" + trip["id"],
                    kind="buyer_brief",
                    origin="buyer",
                    title="Current buying brief",
                    quote=f"Brief fields: {brief.month}; delivery {brief.market}; jacket {brief.jacketSize}; cap {brief.jacketCapMinor} minor units {brief.currency}.",
                    sourceUrl=None,
                    sellerId=None,
                    variantId=None,
                    speaker=None,
                    market=brief.market,
                    observedAt=now(),
                    senso=None,
                )
            )
        cohort = self.sets.get(trip["id"])
        board = None
        if cohort and brief:
            providers.catalog = mode
            offers = []
            for row in cohort.rows:
                if mode == "live" and rule and row.policy is None and row.policy_url:
                    row.policy = terms(row)
                offer, source = self.assess(row, brief, memory, rule, mode, providers, trip["buyer"])
                offers.append(offer)
                docs.extend(source)
            eligible = sorted(
                (o for o in offers if o.outcome == "meets"), key=lambda o: (o.priceMinor, o.id)
            )
            winner = eligible[0].id if eligible and memory.state in {"none", "ready"} else None
            if memory.state == "none" and not cohort.baseline_saved:
                cohort.baseline = winner
                cohort.baseline_saved = True
            previous = (
                cohort.baseline
                if memory.state != "none" and cohort.comparison_valid and cohort.baseline_saved
                else None
            )
            if previous:
                # Hold the non-rule checks constant before attributing a change to the rule.
                baseline_candidates = (
                    o for o in offers if all(c.verdict == "meets" for c in o.checks if c.id != "returns")
                )
                control = min(baseline_candidates, key=lambda o: (o.priceMinor, o.id), default=None)
                if control is None or control.id != previous:
                    previous = None
            note = None
            if previous and winner and previous != winner:
                old = next(o for o in offers if o.id == previous)
                verdict = next(c for c in old.checks if c.id == "returns")
                note = f"{old.seller}: {verdict.label} {verdict.verdict}. {eligible[0].seller} now qualifies at the lowest comparable price."
            if memory_note:
                note = memory_note
            board = Shortlist(
                id=cohort.id,
                observedAt=cohort.observed,
                slot="formal_jacket",
                continuity="same_set" if previous else cohort.continuity,
                previousWinnerId=previous,
                winnerId=winner,
                changeNote=note,
                offers=offers,
            )
            reply = (
                reply
                or note
                or (
                    "No matching variants returned."
                    if not offers
                    else (
                        "Review the recommended jacket."
                        if winner
                        else "No jacket meets every mandatory requirement."
                    )
                )
            )
        elif trip["searched"]:
            reply = reply or "Start a new jacket search to get a current shortlist."
        if catalog_failed:
            providers.catalog = "unavailable"
        return View(
            schemaVersion=1,
            tripId=trip["id"],
            sessionId=sid,
            mode=mode,
            reply=reply
            or memory_note
            or (GUIDE if not brief else "Ready to source your formal jacket."),
            providers=providers,
            brief=brief,
            memory=memory,
            shortlist=board,
            evidence=docs,
        )

    def mutation(self, buyer, sid, req, handoff=False):
        trip = self.context(buyer, sid)
        tid = trip["id"]
        fingerprint = hashlib.sha256(req.model_dump_json().encode()).hexdigest()
        receipt = self.db.execute(
            "SELECT * FROM receipts WHERE session=? AND id=?", (sid, req.requestId)
        ).fetchone()
        if receipt and receipt["fingerprint"] != fingerprint:
            fail(409, "REQUEST_MISMATCH", "Use a new request ID for a different action.")
        if (
            self.db.execute(
                "SELECT id FROM sessions WHERE trip=? ORDER BY rowid DESC LIMIT 1", (tid,)
            ).fetchone()[0]
            != sid
        ):
            fail(409, "SESSION_SUPERSEDED", "Use the newest conversation for this trip.")
        if handoff:
            result = self.handoff(trip, sid, req, receipt)
            outcome = result["status"]
            if outcome == "ready":
                outcome = self.quote_receipt(result["view"], req.offerId)
        elif receipt:
            return self.view(trip, sid, "This action was already applied.")
        else:
            result = self.turn(trip, sid, req)
            outcome = "applied"
        self.db.execute(
            "INSERT INTO receipts VALUES(?,?,?,?) ON CONFLICT(session,id) DO UPDATE SET outcome=excluded.outcome",
            (sid, req.requestId, fingerprint, outcome),
        )
        return result

    def turn(self, trip, sid, req):
        tid, mode = trip["id"], trip["mode"]
        action, text = req.action, req.text.strip()
        brief = Brief.model_validate_json(trip["brief"]) if trip["brief"] else None
        if action == "save_rule" or action == "message" and explicit_save(text):
            if (
                not explicit_save(text)
                and text.lower().replace("’", "'").rstrip(".") != "i don't buy final-sale items"
            ):
                fail(422, "UNSUPPORTED_RULE", "Use the explicit no-final-sale rule for this demo.")
            inserted = self.db.execute(
                "INSERT OR IGNORE INTO rules(buyer,mode,binding) VALUES(?,?,?)",
                (trip["buyer"], mode, str(uuid4())),
            ).rowcount
            return self.view(trip, sid, pending=bool(inserted))
        intent = self.language(text) if mode == "live" and action == "message" else None
        language = "live" if intent else "guided"
        if (
            action == "message"
            and brief
            and intent
            and intent.intent == "source_jackets"
            and text.lower().startswith(("find ", "source ", "search for ", "show me "))
            and "jacket" in text.lower()
        ):
            action = "source_jackets"
        if action == "source_jackets":
            if not brief or not any(
                n.category.lower() in {"jacket", "jackets"} and n.quantity for n in brief.needs
            ):
                fail(422, "BRIEF_REQUIRED", "Supply a brief with a jacket slot first.")
            previous = self.sets.pop(tid, None)
            next_search = None
            try:
                if mode == "live":
                    rows, next_search = self.catalog[mode].search_batch(
                        brief, previous.next_search if previous else None
                    )
                else:
                    rows = self.catalog[mode].search(brief)
            except (Blocked, ValueError, KeyError, TypeError) as exc:
                return self.view(
                    trip,
                    sid,
                    str(exc) if isinstance(exc, Blocked) else "Invalid catalog result.",
                    catalog_failed=True,
                )
            if mode == "sample":
                seed(self.db, SampleMemory(), trip["buyer"], mode)
            self.sets[tid] = Cohort(
                rows, "new_search" if trip["searched"] else "first", next_search=next_search
            )
            self.db.execute("UPDATE trips SET searched=1 WHERE id=?", (tid,))
        elif action == "message":
            try:
                updated = edit(text, brief.model_dump() if brief else None)
            except (ValueError, KeyError, TypeError):
                fail(422, "INVALID_BRIEF", "Check the brief fields, quantities and cap.")
            if updated is None:
                view = self.view(trip, sid, language=language)
                if (intent and intent.intent == "evidence") or any(
                    k in text.lower() for k in ["why", "evidence", "policy", "price"]
                ):
                    doc = next(
                        (
                            d
                            for d in view.evidence
                            if d.id in text
                            or (
                                d.kind in {"merchant_policy", "sample_policy"}
                                and d.title.split()[0].lower() in text.lower()
                            )
                        ),
                        None,
                    )
                    view.reply = (
                        f"{doc.title}: {doc.quote}"
                        if doc
                        else "Select a check or send its evidence ID for the exact passage."
                    )
                else:
                    view.reply = GUIDE
                return view
            self.db.execute("UPDATE trips SET brief=? WHERE id=?", (json.dumps(updated), tid))
            self.sets.pop(tid, None)
        return self.view(self.context(trip["buyer"], sid), sid, language=language)

    @staticmethod
    def quote_receipt(view, offer_id):
        offer = next(o for o in view.shortlist.offers if o.id == offer_id)
        fields = [view.shortlist.id, offer.sellerId, offer.variantId, offer.priceMinor, offer.currency]
        return "ready:" + hashlib.sha256(json.dumps(fields).encode()).hexdigest()

    def handoff(self, trip, sid, req, receipt):
        cohort = self.sets.get(trip["id"])
        if not cohort or cohort.id != req.shortlistId:
            fail(409, "STALE_SHORTLIST", "Source jackets again for this trip.")
        row = next((r for r in cohort.rows if r.offer.id == req.offerId), None)
        if row is None:
            if any(r.offer.id == req.offerId for c in self.sets.values() for r in c.rows):
                fail(409, "OFFER_MISMATCH", "Select an offer from this shortlist.")
            fail(404, "UNKNOWN_OFFER", "Offer not in this shortlist.")
        view = self.view(trip, sid)

        def envelope(status, note, url=None):
            return {"status": status, "note": note, "url": url, "view": view}

        if receipt:
            status = receipt["outcome"]
            if status.startswith("ready:"):
                if status != self.quote_receipt(view, req.offerId):
                    return envelope(
                        "changed", "The previously confirmed quote changed. Review and confirm again."
                    )
            else:
                return envelope(
                    status, "Previous attempt. Review the current board before a new action."
                )
        if view.shortlist.winnerId != req.offerId:
            return envelope("unavailable", "A qualifying current recommendation is required.")
        if trip["mode"] == "sample":
            return envelope("sample", "Fictional offer. Sample checkout ends here.")
        try:
            fresh = self.catalog["live"].lookup(
                view.brief, row.offer.sellerId, row.offer.variantId, row.offer.size
            )
        except (Blocked, ValueError, KeyError, TypeError):
            view.providers.catalog = "unavailable"
            return envelope("unavailable", "The exact quote could not be revalidated.")
        if not fresh or (fresh.offer.sellerId, fresh.offer.variantId) != (
            row.offer.sellerId,
            row.offer.variantId,
        ):
            cohort.rows.remove(row)
            cohort.comparison_valid = False
            view = self.view(trip, sid)
            return envelope("unavailable", "The exact seller and variant could not be verified.")
        changed = (fresh.offer.priceMinor, fresh.offer.currency) != (
            row.offer.priceMinor,
            row.offer.currency,
        )
        cohort.rows[cohort.rows.index(row)] = fresh
        if row.comparison_facts() != fresh.comparison_facts():
            cohort.comparison_valid = False
        if row.policy is not None:
            fresh.policy = terms(fresh)
            if fresh.policy is None or fresh.policy.quote != row.policy.quote:
                cohort.comparison_valid = False
        cohort.observed = now()
        view = self.view(trip, sid)
        if view.shortlist.winnerId != req.offerId or not fresh.checkout:
            return envelope("unavailable", "This offer no longer qualifies.")
        if changed:
            return envelope("changed", "Review the updated price before confirming again.")
        return envelope("ready", "Open the verified checkout.", fresh.checkout)
