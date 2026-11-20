# Phase Q verification · November 20, 2026

**Demo result.** Shopify UCP returned three live seller-specific variants. The app kept checkout on hold. In the labeled sample, a buyer’s explicit no-final-sale rule changed the recommendation from Alder at $180 to Birch at $220. Cedar’s return terms remained Unknown. A fresh conversation reproduced the result with the original three seller/variant IDs, prices and shortlist ID.

The timed Chromium walk-through took **0.5 seconds in sample mode** and **3.3 seconds in live mode**, from initial page load through the last buyer action. These are automated interaction times. A spoken judge rehearsal is scheduled for Phase V.

| Claim | Status | Evidence from Phase Q | Wording for judges |
| --- | --- | --- | --- |
| T01 · Trip and price scope | Sample verified | The June brief produced three cities with three events each, ten items and one active jacket. The browser showed nine open and unpriced slots and identified the editable defaults. | “We price one jacket. The other nine items stay on the shopping list.” |
| T02 · Cause of the change | Sample verified | Alder won the rule-free control, including after deliberately removing a saved rule in an isolated database. Saving changed Alder to Fails, Birch to Meets and Cedar to Unknown. Allowing returns at Alder’s sale price kept Alder first. A failed fetch for a known rule cleared the winner. Stock loss on a synthetic quote invalidated the comparison. | “The return policy explains the extra $40. If Alder accepts the return, it keeps the recommendation.” |
| T03 · Memory and isolation | Sample verified; live storage observed; live recall blocked | Dropping the response after a committed save and retrying produced one rule. Two buyers saving the same text received distinct bindings. After restarting Uvicorn on the same SQLite file, the original sample rule was ready. The live binding survived, live recall stayed unavailable, and the old live shortlist returned HTTP 409. A second browser context received HTTP 404 for both trips. | “A new chat can reuse a current shortlist. After a restart the preference survives and prices require a new search.” |
| T04 · Policy scope and Senso | Sample verified; live Senso blocked | Tests rejected sample evidence for a live offer, wrong seller or variant, wrong market, expired and full-price-only terms. An inclusive 20% markdown threshold excluded the boundary price. Mock Senso responses verified content/node binding, exact passage, returned version/chunk fields and nulls for absent IDs. Missing credentials prevented collection of actual Senso IDs. | “Open Evidence to see which seller, variant and passage support the check.” |
| T05 · Jev verdicts | Sample verified; live Jev blocked | Fixtures covered positive, negated, final-sale, empty and conflicting terms. Below-threshold sufficiency or verdict probability produced Unknown. Inadmissible policy evidence produced zero returnability calls. A simulated timeout retained deterministic checks. | “The sample shows the decision logic. This Cloud run could not verify a live Jev judgment.” |
| T06 · Shopify catalog | Observed live; edge cases sample verified | A fresh browser rendered three Shopify variants after search and exact lookup. Synthetic catalog cases exercised a relaxed size, missing native checkout, external source and stock loss. The browser rendered zero, one and two results. | “Shopify supplied these three live variants. None qualified on this run.” |
| T07 · Checkout | Sample verified; real destination unrun | The sample produced a null URL. Synthetic price changes required renewed confirmation. A revalidated seller/variant URL kept its attribution and opened a reserved test merchant in a new tab. Wrong variants, missing links and stale sets held checkout. The actual live board had no winner. | “Checkout stops here today. A verified qualifying live quote is required to open a merchant.” |
| T08 · Currency, price and access | Sample verified; guided language observed | USD 0 and missing price had distinct results. Mixed currency held the budget check. Grouped amounts and yen, euro and dollar inputs used the corresponding minor units. Simulated 401, 429 and 503 responses exposed the catalog failure. The actual live brief used guided input. | “The subtotal is for one unit in the displayed currency. Shipping and tax remain undetermined.” |
| T09 · Buyer interface | Sample verified | Keyboard actions opened exact source text and returned focus. At 390 px a long citation fit the viewport. Missing photos, all-Unknown results, repeated search, expired sets and a superseded session rendered safely. Network failure preserved the draft. Status messages use a polite live region. Screen-reader audio was unrun. | “Select a check to inspect its source. You can keep typing if a request fails.” |

Four repairs landed during verification. Catalog evidence must match the offer’s origin and identity. A withdrawn or amended Senso passage cannot activate a saved rule through a substring match. Quote changes affecting eligibility invalidate the original comparison. Guided caps recognize currency symbols and thousands separators.

## Reproduce

Use Python 3.12, the project dependencies, Playwright and Chromium. Each browser run creates isolated buyer state. The optional live runs perform a real catalog search and an explicit demo preference save when the providers are configured.

```sh
python -m unittest discover -s commerce/tests -q
python -m commerce.contracts.verify
python -m commerce.tests.browser_integration
python -m commerce.tests.rehearse --live
```

Seventeen backend tests and the frozen v1 contract with ten example responses passed. The browser suites passed. The rehearsal command starts two separate Uvicorn processes in succession, retains the buyer cookie and database, and checks that the old shortlist cannot be handed off after restart.

**Release decision.** The Codex GUI fallback puts Q and repairs in the same time slot. Skip X and Deepgram. Reserve the final 30 minutes for **Phase V with GPT-6.2-Astra, XHigh**. Live Senso recall, live Jev decisions and a qualifying real merchant handoff remain open.
