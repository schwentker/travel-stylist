"""Phase I browser checks. Run as a module. --live performs one additional real sourcing action."""

import argparse
import shutil
import socket
import threading
import time
from contextlib import contextmanager
from copy import deepcopy
from unittest.mock import patch
from urllib.parse import urlsplit

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
        if expected == {"requestId", "offerId", "shortlistId"} and "override" in body:
            expected.add("override")
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


def sparse_boards(page, url, service):
    rows = SampleCatalog().search(None)
    for row in rows:
        row.offer.imageUrl = None
        row.item.quote = "Fictional catalog detail. " * 100
    with (
        patch.object(service.catalog["sample"], "search", side_effect=[[], rows[:1], rows[:2]]),
        patch.object(
            service.judge["sample"], "judge", return_value=("unknown", "Insufficient evidence.")
        ),
    ):
        empty = begin(page, url, "sample")
        assert empty["shortlist"]["offers"] == []
        expect(page.locator(".offer")).to_have_count(0)
        for count in (1, 2):
            board = action(page, "source").json()["shortlist"]
            assert board["winnerId"] is None and board["continuity"] == "new_search"
            expect(page.locator(".offer")).to_have_count(count)
            expect(page.get_by_text("No photo supplied", exact=True)).to_have_count(count)
            expect(page.locator("#checkout")).to_be_disabled()
        page.set_viewport_size({"width": 390, "height": 844})
        page.get_by_role("button", name="Formality Unknown").first.press("Enter")
        expect(page.locator("#evidence blockquote")).to_have_text(rows[0].item.quote.strip())
        assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
        draft = "Why is this jacket marked unknown?"
        page.locator("#draft").fill(draft)
        page.route("**/turns", lambda route: route.abort(), times=1)
        page.locator("#send").press("Enter")
        expect(page.locator("#notice")).to_contain_text("Try again")
        expect(page.locator("#draft")).to_have_value(draft)

        # Simulate a committed save whose HTTP response was lost.
        def lose_save_response(route):
            assert route.fetch().ok
            route.abort()

        page.route("**/turns", lose_save_response, times=1)
        page.locator("#save").press("Enter")
        retry = page.get_by_role("button", name="Retry", exact=True)
        expect(retry).to_be_visible()
        with page.expect_response(lambda r: r.url.endswith("/turns")) as received:
            retry.press("Enter")
        assert received.value.json()["memory"]["state"] == "ready"
        expect(page.locator("#save")).to_be_disabled()
        buyer = page.context.cookies(url)[0]["value"]
        with service.lock:
            assert (
                service.db.execute("SELECT COUNT(*) FROM rules WHERE buyer=?", (buyer,)).fetchone()[0]
                == 1
            )
        # A second conversation supersedes the first session while its tab is still open.
        newer = page.context.request.post(
            url + "/api/sessions", data={"mode": "sample", "tripId": empty["tripId"]}
        )
        assert newer.ok and action(page, "refresh").status == 409
        expect(page.locator("#draft")).to_have_value(draft)
        expect(page.locator("#checkout")).to_be_disabled()
    print(
        "PASS 0/1/2 offers, all Unknown, missing photos, long mobile citation, retained draft and superseded session"
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
        patch.object(catalog, "search_batch", side_effect=lambda *_: (deepcopy(rows), None)),
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
            Brief.model_validate(view["brief"]),
            winner.offer.sellerId,
            winner.offer.variantId,
            winner.offer.size,
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


def synthetic_override(page, url, service):
    row = SampleCatalog().search(None)[0]
    row.offer.origin = row.item.origin = "shopify_live"
    row.item.quote = "A navy jacket with brass buttons."
    row.offer.priceMinor = 31000
    row.policy = None
    row.checkout = "https://merchant.example/buy/jacket"
    catalog = service.catalog["live"]
    with (
        patch.object(service, "language", return_value=None),
        patch.dict(service.judge, {"live": SampleJudgment()}),
        patch.object(catalog, "search_batch", side_effect=lambda *_: ([deepcopy(row)], None)),
        patch.object(catalog, "lookup", side_effect=lambda *_: deepcopy(row)),
    ):
        view = begin(page, url, "live")
        assert view["shortlist"]["winnerId"] is None
        review = page.get_by_role("button", name="Review checkout override")
        expect(review).to_be_hidden()
        expect(page.get_by_role("radio")).not_to_be_checked()
        inline = page.get_by_role("button", name="Override formality", exact=True)
        inline.click()
        dialog = page.get_by_role("dialog")
        expect(dialog.get_by_role("checkbox", name="Formality", exact=False)).to_be_checked()
        expect(dialog.get_by_role("button", name="Accept checks and verify checkout")).to_be_disabled()
        expect(dialog).to_contain_text("Formality · Unknown")
        dialog.get_by_role("button", name="Cancel").click()
        expect(page.locator("#merchant a")).to_have_count(0)
        review.click()
        for box in dialog.get_by_role("checkbox").all():
            box.check()
        with page.expect_response(lambda r: r.url.endswith("/handoff")) as response:
            dialog.get_by_role("button", name="Accept checks and verify checkout").click()
        assert response.value.json()["status"] == "override_ready"
        expect(page.get_by_role("link", name="Open merchant checkout")).to_have_attribute(
            "href", row.checkout
        )
        expect(page.get_by_role("radio")).to_be_checked()
        expect(page.locator("#candidate-summary")).to_contain_text("No eligible recommendation")
        action(page, "refresh")
        expect(page.locator("#merchant a")).to_have_count(0)
    print("PASS buyer override confirmation, non-winner handoff and link clearance")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    service = Workflow(":memory:")
    errors = []
    with serve(service) as url, sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=shutil.which("chromium"))
        flows = (
            [sample_flow, sparse_boards]
            + ([live_flow] if args.live else [])
            + [synthetic_checkout, synthetic_override]
            + [sponsored_mock_flow]
        )
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


def _check_unit(page, slot, expected_format):
    unit = slot.locator(".sponsored-unit")
    expect(page.locator(".sponsored-unit")).to_have_count(1)
    expect(unit).to_have_attribute("data-format", expected_format)
    expect(unit.locator(".sponsored-label")).to_be_visible()
    expect(unit.locator(".sponsored-label")).to_have_text("Sponsored")
    caption = unit.locator(".sponsored-caption")
    expect(caption).to_be_visible()
    expect(caption).to_contain_text("Not affiliated with or endorsed by Koah")
    expect(unit.locator(".sponsored-hide")).to_be_visible()
    assert slot.evaluate("""el => el.previousElementSibling?.id === "transcript"
        && el.nextElementSibling?.id === "message-form"
        && !el.closest("#shortlist, #evidence, #merchant, #override-dialog, form")""")
    assert unit.locator("button").evaluate_all("""buttons => buttons.every(b =>
        b.getAttribute("type") === "button" && !b.form && !b.closest("form"))""")
    assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
    assert page.locator("#transcript").evaluate("""el =>
        el.clientHeight >= 8 * parseFloat(getComputedStyle(document.documentElement).fontSize)""")
    return unit


def _exercise_card(slot):
    why = slot.locator(".sponsored-why")
    detail = slot.locator("#sponsored-why-text")
    expect(why).to_have_attribute("aria-expanded", "false")
    expect(detail).to_be_hidden()
    why.click()
    expect(why).to_have_attribute("aria-expanded", "true")
    expect(detail).to_be_visible()
    expect(detail).to_contain_text("Never read")
    why.click()
    expect(why).to_have_attribute("aria-expanded", "false")
    expect(detail).to_be_hidden()
    slot.locator(".sponsored-cta").click()
    expect(slot.locator(".sponsored-unit")).to_have_attribute("data-cta-clicked", "true")
    expect(slot.locator(".sponsored-demo-note")).to_be_visible()


def _placement_journey(page, url, *, show_units):
    """Capture decisions and transcript lengths from actual responses and rendered turns."""
    slot = page.locator("#sponsored-slot")
    unit = page.locator(".sponsored-unit")
    transcript = page.locator("#transcript li")
    states = []
    page.goto(url)
    page.set_viewport_size({"width": 390, "height": 844})
    expect(slot).to_have_count(1)
    expect(slot).to_be_hidden()
    assert slot.evaluate("el => el.childElementCount") == 0
    page.locator("#mode").select_option("sample")
    for button in ("start", "send", "source", "save", "reopen", "checkout"):
        if button == "send":
            page.locator("#example").press("Enter")
        response = action(page, button)
        assert response.ok, (button, response.status)
        data = response.json()
        view = data["view"] if button == "checkout" else data
        winner = (view["shortlist"] or {}).get("winnerId")
        states.append((button, winner, transcript.count(), page.evaluate("window.formSubmits")))
        if button == "source":
            assert winner == "offer-a"
        elif button in ("reopen", "checkout"):
            assert winner == "offer-b"
        if show_units and button == "send":
            _check_unit(page, slot, "action-card")
            _exercise_card(slot)
        elif show_units and button in ("source", "save"):
            poll = _check_unit(page, slot, "poll")
            if button == "source":
                expect(poll.locator(".sponsored-poll-thanks")).to_be_hidden()
                poll.locator(".sponsored-poll-option").first.click()
            # A save must preserve the voted poll.
            expect(poll).to_have_attribute("data-voted", "true")
            expect(poll.locator(".sponsored-poll-thanks")).to_be_visible()
        else:
            expect(slot).to_be_hidden()
            if button == "start":
                assert slot.evaluate("el => el.childElementCount") == 0
            if not show_units:
                expect(unit).to_have_count(0)
    return states


def _compare_sponsored_runs(page, url):
    from itertools import count
    from uuid import UUID

    results = []
    for flag in ("", "?ads=mock"):
        # Real trips and shortlists get new UUIDs. Give each run the same clean DB
        # and ID sequence so the comparison can retain every field except requestId.
        workflow = Workflow(":memory:")
        serial = count(1)
        requests = []
        modules = []

        def capture(request):
            target = urlsplit(request.url)
            filename = target.path.rsplit("/", 1)[-1]
            if filename.startswith("sponsored") and filename.endswith(".js"):
                modules.append(filename)
            if target.path.startswith("/api/"):
                body = request.post_data_json
                if isinstance(body, dict):
                    body = {k: v for k, v in body.items() if k != "requestId"}
                requests.append((request.method, target.path, target.query, body))

        page.on("request", capture)
        try:
            with (
                patch.object(app.state, "workflow", workflow),
                patch("commerce.workflow.uuid4", side_effect=lambda: UUID(int=next(serial))),
                patch.object(workflow, "language", return_value=None),
            ):
                states = _placement_journey(page, url + "/" + flag, show_units=bool(flag))
                if flag:
                    assert {"sponsored.js", "sponsored-ads.js"} <= set(modules), modules
                else:
                    assert not modules, modules
                assert len(requests) == len(states), requests
                results.append((states, requests))
        finally:
            page.remove_listener("request", capture)
            if workflow.db is not None:
                workflow.db.close()
    assert results[0] == results[1], ("flag changed decisions, transcript or API traffic", results)


def _sponsored_module_failures(page, url, service):
    from playwright.sync_api import TimeoutError as BrowserTimeout

    faults = ((404, "text/plain", ""), (500, "text/plain", ""),
              (200, "text/html", "<!doctype html><title>Fallback</title>"),
              (200, "text/javascript", "export default [;"))
    # The final slot could be hidden even if an earlier turn briefly displayed it.
    page.add_init_script("""window.sponsoredSlotExposed = false;
        new MutationObserver(records => {
            const slot = document.getElementById("sponsored-slot");
            if (slot && (!slot.hidden || records.some(record =>
                record.target === slot && record.type === "attributes" &&
                record.attributeName === "hidden" && record.oldValue === null))) {
                window.sponsoredSlotExposed = true;
            }
        }).observe(document, {subtree: true, childList: true, attributes: true,
            attributeFilter: ["hidden"], attributeOldValue: true});""")
    failures = []
    for module in ("sponsored.js", "sponsored-ads.js"):
        pattern = "**/" + module
        for status, mime, body in faults:
            page.context.clear_cookies()
            intercepted = []

            def fail_module(route):
                intercepted.append(route.request.url)
                route.fulfill(status=status, content_type=mime, body=body)

            page.route(pattern, fail_module)
            try:
                sample_flow(page, url + "/?ads=mock", service)
                expect(page.locator("#sponsored-slot")).to_have_count(1)
                expect(page.locator("#sponsored-slot")).to_be_hidden()
                assert not page.evaluate("window.sponsoredSlotExposed"), "slot became visible"
                assert intercepted, "fault injection did not reach the target"
            except (BrowserTimeout, AssertionError) as exc:
                failures.append(f"Part A isolation blocker: {module} {status} {mime}: {exc}")
            finally:
                page.unroute(pattern, fail_module)
    assert not failures, "\n".join(failures)


def _checkout_and_dismissal(page, url):
    page.context.clear_cookies()
    begin(page, url + "/?ads=mock", "sample")
    slot = page.locator("#sponsored-slot")
    expect(slot.locator(".sponsored-unit")).to_have_attribute("data-format", "poll")
    # A question about an existing jacket retains the shortlist and allows checkout.
    page.locator("#draft").fill("Why is this jacket recommended?")
    assert action(page, "send").ok
    expect(slot.locator(".sponsored-unit")).to_have_attribute("data-format", "action-card")
    assert action(page, "checkout").json()["status"] == "sample"
    expect(slot).to_be_hidden()
    assert action(page, "source").ok
    expect(slot).to_be_hidden()

    assert action(page, "reopen").ok
    expect(slot).to_be_hidden()
    assert action(page, "source").ok
    submits = page.evaluate("window.formSubmits")
    slot.locator(".sponsored-hide").click()
    assert page.evaluate("window.formSubmits") == submits
    expect(slot).to_be_hidden()
    expect(page.locator("#draft")).to_be_focused()
    assert action(page, "reopen").ok
    page.locator("#example").press("Enter")
    assert action(page, "send").ok
    expect(slot).to_be_hidden()
    assert action(page, "source").ok
    expect(slot).to_be_hidden()


def sponsored_mock_flow(page, url, service):
    # Includes canceled submissions, all resource types, and popups opened by controls.
    page.add_init_script("""window.formSubmits = 0;
        document.addEventListener("submit", () => window.formSubmits++, true);""")
    foreign = []
    origin = urlsplit(url)

    def inspect_origin(request):
        target = urlsplit(request.url)
        if (target.scheme, target.netloc) != (origin.scheme, origin.netloc):
            foreign.append(request.url)

    page.context.on("request", inspect_origin)
    _compare_sponsored_runs(page, url)
    _sponsored_module_failures(page, url, service)
    _checkout_and_dismissal(page, url)
    # Switching mode must hide a visible Sample placement before Live starts.
    page.context.clear_cookies()
    page.goto(url + "/?ads=mock")
    page.locator("#mode").select_option("sample")
    assert action(page, "start").ok
    page.locator("#example").press("Enter")
    assert action(page, "send").ok
    slot = page.locator("#sponsored-slot")
    expect(slot).to_be_visible()
    page.locator("#mode").select_option("live")
    expect(slot).to_be_hidden()
    assert action(page, "start").ok
    expect(slot).to_be_hidden()
    with patch.object(service, "language", return_value=None):
        page.locator("#example").press("Enter")
        assert action(page, "send").ok
    expect(slot).to_be_hidden()
    with patch.object(service.catalog["live"], "search_batch", return_value=([], None)):
        assert action(page, "source").ok
    expect(slot).to_be_hidden()
    assert not foreign, foreign
    print("PASS sponsored separation, controls, dismissal, checkout, Live gating and module failures")


if __name__ == "__main__":
    main()
