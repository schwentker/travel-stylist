# Phase I · Browser integration · November 20, 2026

The three browser files delivered by the Codex GUI fallback run against the FastAPI server on the project branch. The browser suite starts Uvicorn on loopback with isolated SQLite, uses Chromium, and drives the rendered controls. It checks that browser API requests stay on the app origin, carry the expected payload fields, and contain no provider authorization headers.

| Run | Observed outcome |
| --- | --- |
| Sample, desktop | The brief showed one active slot out of ten. Alder led at $180. Saving the final-sale rule showed indexing and disabled checkout. After clearing the rendered transcript, a new session returned the same trip and shortlist, recalled the rule, and recommended Birch at $220. |
| Sample, 390 px phone | Enter opened Alder’s returnability evidence. The policy excerpt matched the API response, and the evidence panel showed the variant ID. Focus moved to Evidence and returned to the triggering check. The page fit the viewport. Sample handoff showed the explanation with no merchant link. |
| Expired shortlist | Expiring the in-memory set while the page remained open produced HTTP 409 on checkout. Refresh cleared the expired offers. An explicit search produced a new set ID. |
| Live Cloud | The browser rendered three Shopify variants. Jev showed unavailable, language showed guided, and the board had no eligible winner. After a save and a fresh session, the UI showed “Memory unavailable · checkout on hold.” Cloud lacked the Senso and Jev credentials. A real merchant destination remains unverified. |
| Synthetic checkout, real handlers | A price change required another confirmation. Revalidation used the chosen seller and variant. The returned HTTPS link retained its encoded attribution and opened a separate tab with an isolated opener. The test intercepted the reserved merchant.example page. Substituting another variant at revalidation held checkout. |
| Synthetic client failures | A mismatched-session response left the current board intact. A ready envelope with a substituted variant produced no link. Changing selection after a transport error removed the old checkout retry. |

Integration changes expose the seller and variant IDs, provide keyboard return from evidence, and disable actions for the old trip when a different mode is selected. Checkout also checks the selected seller, variant, price and currency against the refreshed offer.

## Repeat the checks

Install the optional browser test tools with `python -m pip install playwright` and `python -m playwright install chromium`. Run from the repository root:

```sh
python -m commerce.tests.browser_integration
python -m unittest discover -s commerce/tests -q
python -m commerce.contracts.verify
```

The browser test uses a system Chromium when available. Add `--live` to the browser command to run the buyer flow against the configured providers, including an explicit rule save. The 12 backend tests and frozen v1 contract checks passed in Cloud.

Phase Q is the independent verification and rehearsal gate. Its planned setting is GPT-6.2-Astra with XHigh effort.
