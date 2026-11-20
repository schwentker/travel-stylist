"""Time the buyer rehearsal and check the same trips after a real server restart."""

import argparse
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

import httpx
from playwright.sync_api import expect, sync_playwright

from .browser_integration import action


@contextmanager
def running_server(port, db):
    url = f"http://127.0.0.1:{port}"
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "commerce.app:app",
            "--port",
            str(port),
            "--log-level",
            "error",
        ],
        env={**os.environ, "COMMERCE_DB": str(db)},
    )
    try:
        with httpx.Client(base_url=url, trust_env=False) as client:
            for _ in range(100):
                if process.poll() is not None:
                    raise RuntimeError("Uvicorn exited during startup")
                try:
                    if client.get("/").is_success:
                        break
                except httpx.ConnectError:
                    pass
                time.sleep(0.05)
            else:
                raise RuntimeError("Uvicorn startup timed out")
        yield url
    finally:
        process.terminate()
        process.wait(timeout=10)


def cohort(view):
    return sorted(
        (o["sellerId"], o["variantId"], o["priceMinor"], o["currency"])
        for o in view["shortlist"]["offers"]
    )


def journey(page, url, mode):
    start = time.perf_counter()
    page.goto(url)
    page.locator("#mode").select_option(mode)
    new = action(page, "start").json()
    assert new["brief"] is None and new["memory"]["state"] == "none"
    page.locator("#example").press("Enter")
    brief = action(page, "send").json()
    before = action(page, "source").json()
    board = before["shortlist"]
    count = len(board["offers"]) if board else 0
    print(
        mode,
        "providers",
        before["providers"],
        "brief language",
        brief["providers"]["language"],
        "offers",
        count,
        "baseline winner",
        bool(board and board["winnerId"]),
        flush=True,
    )
    if mode == "sample":
        assert board["winnerId"] == "offer-a"
        expect(page.locator("#brief")).to_contain_text("1 of 10 active · 9 open and unpriced")
    saved = action(page, "save").json()
    after = action(page, "reopen").json()
    assert after["sessionId"] != new["sessionId"] and after["tripId"] == new["tripId"]
    expect(page.locator("#transcript li")).to_have_count(1)
    if board:
        assert after["shortlist"]["id"] == board["id"] and cohort(after) == cohort(before)
    if mode == "sample":
        assert saved["memory"]["state"] == "indexing" and after["memory"]["state"] == "ready"
        assert after["shortlist"]["winnerId"] == "offer-b"
        checks = {
            o["id"]: next(c for c in o["checks"] if c["id"] == "returns")
            for o in after["shortlist"]["offers"]
        }
        assert [checks["offer-" + x]["verdict"] for x in "abc"] == ["fails", "meets", "unknown"]
        page.locator('[data-offer="offer-a"]').get_by_role("button", name="Returnability Fails").press(
            "Enter"
        )
        doc = next(d for d in after["evidence"] if d["id"] == "policy-a")
        expect(
            page.locator("#evidence blockquote").get_by_text(doc["quote"], exact=True)
        ).to_be_visible()
        result = action(page, "checkout").json()
        assert result["status"] == "sample" and result["url"] is None
    elif after["shortlist"] and after["shortlist"]["winnerId"]:
        result = action(page, "checkout").json()
        print("Live handoff", result["status"])
        if result["status"] == "ready":
            link = page.locator("#merchant a")
            expect(link).to_have_attribute("href", result["url"])
            with page.expect_popup() as opened:
                link.click()
            opened.value.wait_for_load_state("domcontentloaded")
            opened.value.close()
    else:
        expect(page.locator("#checkout")).to_be_disabled()
        expect(page.locator("#merchant a")).to_have_count(0)
    print(
        mode,
        "save",
        saved["memory"]["state"],
        "fresh recall",
        after["memory"]["state"],
        "elapsed_seconds",
        round(time.perf_counter() - start, 1),
        flush=True,
    )
    return after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live", action="store_true", help="Also source a real cohort and explicitly save a demo rule."
    )
    args = parser.parse_args()
    with TemporaryDirectory() as tmp, sync_playwright() as driver:
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        db = Path(tmp) / "rehearsal.sqlite"
        browser = driver.chromium.launch(executable_path=shutil.which("chromium"))
        buyer = browser.new_context()
        other = browser.new_context()
        with running_server(port, db) as url:
            trips = [
                journey(buyer.new_page(), url, mode)
                for mode in (["sample", "live"] if args.live else ["sample"])
            ]
        with sqlite3.connect(db) as connection:
            bindings = dict(connection.execute("SELECT mode, binding FROM rules"))
        with running_server(port, db) as url:
            for trip in trips:
                mode = trip["mode"]
                payload = {"tripId": trip["tripId"], "mode": mode}
                assert other.request.post(url + "/api/sessions", data=payload).status == 404
                response = buyer.request.post(url + "/api/sessions", data=payload)
                assert response.ok
                view = response.json()
                assert view["brief"] == trip["brief"] and view["shortlist"] is None
                assert view["memory"]["ruleText"] == trip["memory"]["ruleText"]
                assert view["memory"]["state"] != "none"
                if mode == "sample":
                    assert view["memory"]["state"] == "ready"
                if trip["shortlist"] and trip["shortlist"]["offers"]:
                    stale = buyer.request.post(
                        url + "/api/sessions/" + view["sessionId"] + "/handoff",
                        data={
                            "requestId": str(uuid4()),
                            "shortlistId": trip["shortlist"]["id"],
                            "offerId": trip["shortlist"]["offers"][0]["id"],
                        },
                    )
                    assert stale.status == 409 and stale.json()["error"]["code"] == "STALE_SHORTLIST"
                print(
                    mode,
                    "restart memory",
                    view["memory"]["state"],
                    "shortlist cleared; second buyer denied",
                )
            with sqlite3.connect(db) as connection:
                assert bindings == dict(connection.execute("SELECT mode, binding FROM rules"))
                assert len(bindings) == len(trips)
        browser.close()


if __name__ == "__main__":
    main()
