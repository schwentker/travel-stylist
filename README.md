# Travel Stylist

**A trip-shopping assistant that remembers what you won’t buy and shows exactly why its recommendation changes.**

Plan a wardrobe for nine June events across Delhi, Istanbul, and Barcelona. Travel Stylist turns the trip into ten shopping slots, then focuses on one formal jacket. It compares seller-specific variants by size, availability, price, and applicable return policy. Every check opens the evidence behind it.

## Two-minute judge demo

1. Select **Sample**, click **Start trip**, then choose **Use sample wording** and **Send message**.
2. Click **Source jackets**. Alder starts as the recommended jacket at **$180**.
3. Click **Save “No final-sale items”**. Checkout goes on hold while the rule is indexing.
4. Click **New conversation for this trip**. The saved rule carries over to the same shortlist. Alder drops out because its policy says final sale. **Birch at $220** becomes the recommendation. Cedar stays **Unknown** because its policy is inconclusive.
5. Open Alder’s returnability check to read the policy excerpt, then click **Check checkout** on Birch to see the sample handoff.

This demo uses fictional sellers and works without provider keys. It shows why a cheaper offer can lose and lets judges inspect the source for that decision.

## Protocols and evidence

| Component | What it does |
| --- | --- |
| [Shopify Universal Commerce Protocol (UCP)](https://shopify.dev/docs/agents/catalog/global-catalog) | Live mode calls Shopify’s Global Catalog MCP endpoint with `search_catalog` and `get_product`. It verifies the seller and exact variant, then rechecks price and eligibility before surfacing an attributed merchant checkout link. If the quote changes, the buyer must confirm again. |
| [Senso](https://docs.senso.ai/docs/concepts) | The live adapter scopes preference retrieval to the buyer and document. The sample demonstrates the same save-and-recall flow with local fixtures. |
| [TypeSafe Jev](https://docs.typesafe.ai/primitives/choice) | The live adapter checks whether a source is sufficient and returns a typed verdict on ambiguous requirements. The interface links the verdict to its source and exposes uncertainty. |
| [Personal Agent Protocol / Poppy](https://personalagentprotocol.org/docs/1.0/spec) | Deferred. The [design](commerce-plan/01-master-plan.md#m3-who-does-what) outlines where a seller agent could clarify an ambiguous policy and return an attributed reply. |

**Verified live:** Three successive batches from a Shopify search for the default trip returned nine in-stock jackets in USD, all in 40R or 40 Regular, with attributed seller checkout links for the exact variants. **Verified in the sample:** cross-conversation recall, the Alder-to-Birch change, and the evidence UI. Checkout state transitions were tested with fixtures. Live Senso and Jev verification requires provider keys, and real merchant checkout remains unverified. [Phase Q verification and judge demo claims](commerce/handoff/phase-q-receipt.md)

## Run locally

Use Python 3.12. From the repository root on macOS or Linux:

```sh
python3.12 -m venv .venv-commerce
source .venv-commerce/bin/activate
python -m pip install -r commerce/requirements.txt
python -m uvicorn commerce.app:app --port 8000
```

For Live mode, place `SENSO_API_KEY` and `TYPESAFE_API_KEY` in a `.env` file at the repository root. The app reads it at startup. Sample mode works without keys.

Open [localhost:8000](http://127.0.0.1:8000). FastAPI serves the browser app and API from the same origin. SQLite persists the trip brief and buyer preferences. Live offers and checkout URLs are held in short-lived task memory.

[Backend and live-mode setup](commerce/README.md) · [Frozen API v1](commerce/contracts/v1/openapi.json) · [Acceptance cases](commerce-plan/02-contract-and-cases.md) · [Project plan](commerce-plan/01-master-plan.md)

## Ad placement mock

[Open the Sample demo with mock placements](https://sandboxlabs.ai/travel-stylist/?ads=mock). Choose Sample, send the trip brief, then source jackets to see a fictional travel offer followed by a poll. This local simulation tests whether a trip-shopping assistant can show contextual sponsorship while the buyer’s return policy still determines which jacket wins. Save the no-final-sale rule and reopen the trip to see why Birch replaces Alder. The placement uses fictional data and keeps the poll vote in the browser.

Not affiliated with or endorsed by Koah.
