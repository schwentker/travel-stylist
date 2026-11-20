# Phase F · 2026-11-20 · Cloud

The browser interface is frozen at version 1 against C1–C2 in the uploaded revision. The Cloud checkout of schwentker/travel-stylist at caa02dac707bb4dfbab5869b04eb5dd8e9b091fe holds the foundation, frozen OpenAPI, ten full JSON example files and the stand-alone Gemini packet. All eight uploaded source files match the tracked originals byte for byte.

## Provider probes

| UTC | Provider and reference | Observed result | Next live test |
| --- | --- | --- | --- |
| 19:59:07 | Shopify · UCP-CATALOG-01 | Anonymous JSON-RPC search_catalog returned HTTP 200 with zero products. The returned UCP version was 2026-08-25, with dev.ucp.shopping.catalog.search, dev.ucp.shopping.catalog.lookup and dev.shopify.catalog.global. | On a new authorized sourcing action, try the buyer's size in the search text and verify the effective size on exact lookup if the catalog supplies a variant. |
| 20:03:32 | Senso · BALANCE-01 | One GET /api/v1/org/credits/balance returned HTTP 401, requiring an organization key or valid JWT. Cloud had no provider credential. Organization, balance, isolated ingest, indexing time, content/node/chunk IDs and scoped recall are unverified. | With an authorized server-side key, ingest one fictional buyer-bound source, poll its KB node, search only its content ID with require_scoped_ids, and verify the binding and passage. |
| 20:03:32 | TypeSafe Jev · JUDGMENT-01 | One POST /v1/systemone with model jev-latest, fictional return terms, an evidence_suffices Noul and a return_verdict Choice returned HTTP 403 authentication_error. The service requested an API key. No answer fields, probabilities, confidence or served model were returned. | Repeat the same two-question synthetic probe with a server-side credential and inspect the served model and answers. |
| 19:59:07 | Ollama · INTENT-01 | One structured intent request for llama3.1:8b to loopback port 11434, with a four-second timeout, failed with connection refused in 0.008 s. The Cloud executable was absent. The foundation advertises guided language. | Time one schema-conforming parse on a host already serving the model. |

Shopify used the hosted 2026-08-25 profile and the default representation at the global MCP endpoint. The task was a new, available formal 40R jacket for US delivery, USD 300 maximum (30,000 minor units). The request included both the size text and the catalog size filter. Count: one search, zero get_product calls, zero checkout lookups. Products and capability names were inspected in memory. No live offer or seller payload was saved.

With an empty products array, the following field paths could only be taken from the provider specification. Under product, inspect selected for effective options. Under variants[], inspect id, seller.id, condition, price.amount and price.currency, availability, eligible.native_checkout, seller.links and checkout_url. A later lookup must verify the actual seller/variant, size, availability and policy scope. A checkout claim additionally requires a current attributed HTTPS destination from that variant and buyer confirmation. Live policy coverage, ranking change and checkout remain unverified.

## Foundation checks

- HTTP 200 on GET /, /styles.css and /app.js, with their expected media types. POST /api/sessions returned 200 and a new empty View for both sample and live mode. Mode selection alone performs no provider call.
- GET /api/examples/{name} returned five validated synthetic Views. Backend actions reserved for B returned structured 503, and malformed requests returned structured 422. The three static paths currently hold disposable smoke assets.
- All ten invented responses passed Pydantic and JSON Schema checks. The schema embedded in the GUI packet equals openapi.json. Executing its JavaScript examples reproduced all ten checked-in JSON values. Five malformed or inconsistent checkout responses were rejected. The packet contains only the reserved shop.example test host.
- The before/after board preserves trip, shortlist, seller, variant and unit price. A new session changes Alder at USD 180 to Birch at USD 220 after the saved rule. Cedar remains Unknown. Baseline input contains no saved restriction. Post-save checks resolve to that rule and each offer's own policy. Both indexing and unavailable recall hold the winner. These results verify fictional wire examples. Live recall, backend ranking and browser integration belong to later phases.

## Source boundary and pause

The initial Git 403 and connector 404 cleared on the second access check. Both requested Git commands ran on a fresh Cloud clone of main. The tracked plan contains nine files. Phase F used the approved GUI assignment (04), original sample View (05), revision decisions (07) and all five labeled wire examples (08). The packet preserves the original assignment and replaces the planning appendices with the frozen API and executable examples. The reference validator compares the shipped fixtures against 05 and 08 when run in the checkout.

Backend B is Codex GPT-6.2-Astra with High effort. GUI U is Gemini Carbon with High thinking if available in the operator’s existing chat. Otherwise use the strongest accessible reasoning model there and record its displayed model and setting. Both await operator release. Phase F ended in the Cloud working tree. The remote main branch and Mac checkout received no writes.
