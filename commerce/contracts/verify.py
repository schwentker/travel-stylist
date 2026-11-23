"""Run with python -m commerce.contracts.verify from the repository root."""
import json
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import TypeAdapter

from commerce.app import app
from commerce.contracts.models import ApiError, HandoffResponse, View


BASE = Path(__file__).parent / "v1"


def validate_view(view):
    evidence = {e.id: e for e in view.evidence}
    assert len(evidence) == len(view.evidence)
    if view.memory.evidenceId is not None:
        doc = evidence[view.memory.evidenceId]
        assert doc.kind == "buyer_rule" and view.memory.ruleText == doc.quote
    if view.memory.state == "ready":
        assert view.memory.evidenceId is not None
    if view.shortlist is None:
        return
    board = view.shortlist
    offers = {o.id: o for o in board.offers}
    assert len(offers) == len(board.offers)
    if board.winnerId is not None:
        assert offers[board.winnerId].outcome == "meets"
        assert view.memory.state not in {"indexing", "unavailable"}
    if board.previousWinnerId is not None and board.continuity == "same_set":
        assert board.previousWinnerId in offers
    for o in board.offers:
        ids = [c.id for c in o.checks]
        assert len(set(ids)) == len(ids)
        for c in o.checks:
            assert set(c.evidenceIds) <= evidence.keys() and (c.verdict == "unknown" or c.evidenceIds)
            for eid in c.evidenceIds:
                doc = evidence[eid]
                assert doc.sellerId in {None, o.sellerId} and doc.variantId in {None, o.variantId}
                assert doc.market in {None, o.market}
                if c.id == "returns" and c.verdict != "unknown":
                    assert view.memory.evidenceId in c.evidenceIds
        if o.outcome == "meets":
            assert o.checks and all(c.verdict == "meets" for c in o.checks)


def main():
    schema = (BASE / "openapi.json").read_bytes()
    assert app.openapi() == json.loads(schema), "Frozen OpenAPI differs from the application"
    fixtures = {p.stem: json.loads(p.read_text()) for p in (BASE / "examples").glob("*.json")}
    expected = {"new","before","indexing","fresh-after","no-winner","ready","changed","unavailable","sample","api-error"}
    assert set(fixtures) == expected
    for name, raw in fixtures.items():
        if name == "api-error":
            assert ApiError.model_validate(raw).error.code == "STALE_SHORTLIST"
        elif name in {"ready", "changed", "unavailable", "sample"}:
            obj = TypeAdapter(HandoffResponse).validate_python(raw)
            assert obj.status == name
            if name == "ready":
                assert urlsplit(obj.url).hostname.endswith(".example")
            else:
                assert obj.url is None
            validate_view(obj.view)
        else:
            validate_view(View.model_validate(raw))
    new, before, indexing, after, held = (fixtures[k] for k in ("new","before","indexing","fresh-after","no-winner"))
    assert new["brief"] is new["shortlist"] is None and new["evidence"] == []
    assert before["memory"] == new["memory"] and "final-sale" not in json.dumps(before).lower()
    assert all(d["kind"] not in {"buyer_rule","sample_policy","merchant_policy"} for d in before["evidence"])
    assert all(c["id"] != "returns" for o in before["shortlist"]["offers"] for c in o["checks"])
    assert indexing["memory"]["state"] == "indexing" and indexing["memory"]["evidenceId"] is None
    assert held["memory"]["state"] == "unavailable" and held["shortlist"]["winnerId"] is None
    assert before["tripId"] == after["tripId"] and before["sessionId"] != after["sessionId"]
    boards = [f["shortlist"] for f in [before,indexing,after,held]]
    fields = ("id","sellerId","variantId","size","market","available","priceMinor","currency")
    snapshots = [sorted(tuple(o[k] for k in fields) for o in board["offers"]) for board in boards]
    assert all(s == snapshots[0] for s in snapshots) and len({b["id"] for b in boards}) == 1
    a, b, c = sorted(after["shortlist"]["offers"], key=lambda offer: offer["id"])
    assert [a["outcome"],b["outcome"],c["outcome"]] == ["fails","meets","unknown"]
    assert before["shortlist"]["winnerId"] == after["shortlist"]["previousWinnerId"] == a["id"]
    assert after["shortlist"]["winnerId"] == b["id"]
    assert len(after["brief"]["cities"]) == 3 and sum(len(c["events"]) for c in after["brief"]["cities"]) == 9
    assert sum(n["quantity"] for n in after["brief"]["needs"]) == 10
    rule = after["memory"]["evidenceId"]
    for o in (a,b,c):
        ids = next(check for check in o["checks"] if check["id"] == "returns")["evidenceIds"]
        assert rule in ids and any(e["kind"] == "sample_policy" and e["id"] in ids and e["variantId"] == o["variantId"] for e in after["evidence"])
    print("PASS: frozen OpenAPI, 10 synthetic envelopes, board continuity, buyer rule and seller evidence.")


if __name__ == "__main__":
    main()
