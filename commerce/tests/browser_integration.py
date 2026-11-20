"""Phase I browser checks. Run as a module. --live performs one additional real sourcing action."""

import argparse
import shutil
import socket
import threading
import time
from contextlib import contextmanager
from copy import deepcopy
from urllib.parse import urlsplit
from unittest.mock import patch

import uvicorn
from playwright.sync_api import expect, sync_playwright

from commerce.app import app
from commerce.contracts.models import Brief
from commerce.providers import SampleCatalog, SampleJudgment
from commerce.workflow import Workflow


@contextmanager
def serve(workflow):
    with socket.socket() as sock, patch.object(app.state, "workflow", workflow):
        sock.bind(("127.0.0.1", 0))
        server = uvicorn.Server(uvicorn.Config(app, log_level="error"))
        thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
        thread.start()
        try:
            for _ in range(100):
                if server.started:
                    break
                time.sleep(0.05)
            assert server.started
            yield f"http://127.0.0.1:{sock.getsockname()[1]}"
        finally:
            server.should_exit = True
            thread.join(10)


def action(page, button):
    with page.expect_response(
        lambda r: "/api/" in r.url and r.request.method == "POST", timeout=60000
    ) as received:
        page.locator("#" + button).press("Enter")
    response = received.value
    expect(page.locator("#start")).to_be_enabled(timeout=60000)
    return response


def begin(page, url, mode):
    page.goto(url)
    page.locator("#mode").select_option(mode)
    assert action(page, "start").ok
    page.locator("#example").press("Enter")
    assert action(page, "send").ok
    return action(page, "source").json()


def inspect_requests(page, url, errors):
    def inspect(req):
        if req.resource_type not in {"xhr", "fetch"}:
            return
        if urlsplit(req.url).netloc != urlsplit(url).netloc or not urlsplit(req.url).path.startswith(
            "/api/"
        ):
            errors.append("unexpected browser API host or route")
        if {"authorization", "x-api-key"} & req.headers.keys():
            errors.append("browser sent a provider credential header")
        body = req.post_data_json or {}
        expected = (
            {"tripId", "mode"}
            if req.url.endswith("/api/sessions")
            else {"requestId", "action", "text"}
            if req.url.endswith("/turns")
            else {"requestId", "offerId", "shortlistId"}
        )
        if set(body) != expected:
            errors.append("unexpected browser payload fields")

    page.on("request", inspect)
    page.on("pageerror", lambda exc: errors.append(str(exc)))


def sample_flow(page, url, service):
    before = begin(page, url, "sample")
    board = before["shortlist"]
    assert board["winnerId"] == "offer-a"
    expect(page.locator("#brief")).to_contain_text("1 of 10 active")
    assert action(page, "save").json()["memory"]["state"] == "indexing"
    expect(page.locator("#checkout")).to_be_disabled()
    page.locator("#transcript").evaluate("(el) => el.replaceChildren()")
    after = action(page, "reopen").json()
    assert after["tripId"] == before["tripId"] and after["sessionId"] != before["sessionId"]
    assert after["shortlist"]["id"] == board["id"] and after["shortlist"]["winnerId"] == "offer-b"
    expect(page.locator("#transcript li")).to_have_count(1)
    expect(page.locator("#shortlist")).to_contain_text(
        "Previously Alder Sample Shop · Now Birch Sample Shop"
    )
    page.set_viewport_size({"width": 390, "height": 844})
    check = page.locator('[data-offer="offer-a"]').get_by_role("button", name="Returnability Fails")
    check.press("Enter")
    expect(page.locator("#evidence-title")).to_be_focused()
    doc = next(e for e in after["evidence"] if e["id"] == "policy-a")
    expect(page.locator("#evidence blockquote").get_by_text(doc["quote"], exact=True)).to_have_count(1)
    expect(page.locator("#evidence")).to_contain_text(doc["variantId"])
    page.get_by_role("button", name="Back to selection").press("Enter")
    expect(check).to_be_focused()
    assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
    assert action(page, "checkout").json()["status"] == "sample"
    expect(page.locator("#merchant a")).to_have_count(0)
    with service.lock:
        service.sets[after["tripId"]].expires = 0
    expired = action(page, "checkout")
    assert expired.status == 409 and expired.json()["error"]["code"] == "STALE_SHORTLIST"
    expect(page.locator("#checkout")).to_be_disabled()
    assert action(page, "refresh").json()["shortlist"] is None
    new_board = action(page, "source").json()["shortlist"]
    assert new_board["id"] != board["id"] and new_board["continuity"] == "new_search"
    print(
        "PASS sample browser, fresh recall, exact evidence, keyboard return, phone layout, expired set and recovery"
    )


def live_flow(page, url):
    view = begin(page, url, "live")
    board = view["shortlist"]
    if board:
        assert all(o["origin"] == "shopify_live" for o in board["offers"])
        expect(page.locator(".offer")).to_have_count(len(board["offers"]))
    print(
        "Live provider states",
        view["providers"],
        "offers",
        len(board["offers"]) if board else 0,
        "winner",
        bool(board and board["winnerId"]),
    )
    assert action(page, "save").ok
    fresh = action(page, "reopen").json()
    print(
        "Live fresh memory",
        fresh["memory"]["state"],
        "visible status",
        page.locator("#memory .quiet").inner_text(),
    )
    if fresh["memory"]["state"] in {"unavailable", "indexing"}:
        expect(page.locator("#checkout")).to_be_disabled()
        expect(page.locator("#merchant a")).to_have_count(0)
    elif fresh["shortlist"] and fresh["shortlist"]["winnerId"]:
        result = action(page, "checkout").json()
        print("Live handoff", result["status"])
        if result["status"] == "ready":
            link = page.locator("#merchant a")
            expect(link).to_have_attribute("href", result["url"])
            with page.expect_popup() as popup:
                link.click()
            popup.value.wait_for_load_state("domcontentloaded")
            popup.value.close()


def synthetic_checkout(page, url, service):
    rows = SampleCatalog().search(None)
    for row in rows:
        row.offer.origin = row.item.origin = "shopify_live"
        row.policy = None
        row.checkout = "https://merchant.example/checkout/" + row.offer.variantId + "?src=demo%2Fucp&n=1"
    winner = next(row for row in rows if row.offer.id == "offer-a")
    catalog = service.catalog["live"]
    with (
        patch.object(service, "language", return_value=None),
        patch.dict(service.judge, {"live": SampleJudgment()}),
        patch.object(catalog, "search", side_effect=lambda _: deepcopy(rows)),
        patch.object(catalog, "lookup", side_effect=lambda *args: deepcopy(winner)) as lookup,
    ):
        view = begin(page, url, "live")
        page.locator("#mode").select_option("sample")
        expect(page.locator("#checkout")).to_be_disabled()
        page.locator("#mode").select_option("live")
        winner.offer.priceMinor += 100
        assert action(page, "checkout").json()["status"] == "changed"
        expect(page.locator("#merchant a")).to_have_count(0)
        assert action(page, "checkout").json()["status"] == "ready"
        lookup.assert_called_with(
            Brief.model_validate(view["brief"]), winner.offer.sellerId, winner.offer.variantId
        )
        link = page.locator("#merchant a")
        expect(link).to_have_attribute("href", winner.checkout)
        page.context.route(
            "https://merchant.example/**",
            lambda route: route.fulfill(content_type="text/html", body="<title>Test merchant</title>"),
        )
        with page.expect_popup() as popup:
            link.click()
        expect(popup.value).to_have_title("Test merchant")
        assert popup.value.url == winner.checkout and popup.value.evaluate("window.opener === null")
        popup.value.close()
        # A ready envelope with the same offer ID but another variant must not publish a link.
        forged = deepcopy(view)
        changed_offer = next(o for o in forged["shortlist"]["offers"] if o["id"] == winner.offer.id)
        changed_offer["variantId"] = "unexpected-variant"
        changed_offer["priceMinor"] = winner.offer.priceMinor
        page.route(
            "**/handoff",
            lambda route: route.fulfill(
                json={"status": "ready", "url": winner.checkout, "note": "Synthetic", "view": forged}
            ),
            times=1,
        )
        action(page, "checkout")
        expect(page.locator("#merchant a")).to_have_count(0)
        expect(page.locator("#checkout-note")).to_contain_text("unavailable for this selection")
        action(page, "refresh")
        # A transport retry must be invalidated when the buyer selects another offer.
        page.route("**/handoff", lambda route: route.abort(), times=1)
        page.locator("#checkout").click()
        expect(page.get_by_role("button", name="Retry", exact=True)).to_be_visible()
        page.locator('[data-offer="offer-c"] input').check()
        expect(page.get_by_role("button", name="Retry", exact=True)).to_have_count(0)
        expect(page.locator("#checkout")).to_be_disabled()
        action(page, "refresh")
        wrong = deepcopy(winner)
        wrong.offer.variantId = "different-variant"
        lookup.side_effect = lambda *args: wrong
        assert action(page, "checkout").json()["status"] == "unavailable"
        expect(page.locator("#merchant a")).to_have_count(0)
        # Deliver an old-session View to a current refresh. Its board must never replace the current one.
        prior = page.locator("#shortlist").inner_text()
        old = dict(view, sessionId="earlier-session")
        page.route("**/turns", lambda route: route.fulfill(json=old), times=1)
        action(page, "refresh")
        expect(page.locator("#notice")).to_contain_text("mismatched response")
        assert page.locator("#shortlist").inner_text() == prior
        print(
            "PASS synthetic changed quote, exact lookup, attributed popup, wrong variant and stale response"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    service = Workflow(":memory:")
    errors = []
    with serve(service) as url, sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=shutil.which("chromium"))
        flows = [sample_flow] + ([live_flow] if args.live else []) + [synthetic_checkout]
        for flow in flows:
            page = browser.new_page(viewport={"width": 1440, "height": 950})
            inspect_requests(page, url, errors)
            if flow is live_flow:
                flow(page, url)
            else:
                flow(page, url, service)
            page.context.close()
        browser.close()
    assert not errors, errors
    print("PASS browser request scope and page errors")


if __name__ == "__main__":
    main()
