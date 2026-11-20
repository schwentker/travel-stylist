# Commerce interface and acceptance cases | v0.2 pre-freeze

This is the boundary between the local server and a browser UI authored in a fresh chat. Examples are application data invented for the demo. The raw responses from Shopify, Senso and Jev are different shapes. Phase F fixes version `1` or issues an explicit replacement before the two builders start. All public names below are case sensitive.

## C1. Browser requests

All requests go to the same origin and return JSON. An opaque session is bound server-side to the demo client and trip. The client cannot select another buyer by changing a request field. Every session starts with an empty transcript. An unsupported input returns an actionable response, or a structured error where appropriate.

| Request | Body | Success |
| --- | --- | --- |
| `POST /api/sessions` | `{"tripId":null,"mode":"sample"}` or `"live"` | New task. Return a View with an assigned trip and session ID, `brief:null` and `shortlist:null`. |
| `POST /api/sessions` | `{"tripId":"trip-1","mode":"sample"}` | Reopen the same buyer’s trip in a **new** session. Reload the trip and retrieve active rules from Senso in live mode. Reuse only an unexpired shortlist for that task and mode. Return the latest View. |
| `POST /api/sessions/{sessionId}/turns` | `{"requestId":"<uuid>","action":"message","text":"<buyer text>"}` | Parse a new brief, answer an evidence question or recognize an explicit save. Return a View. A parsed brief alone can return `shortlist:null`. |
| Same turns endpoint | `{"requestId":"<uuid>","action":"source_jackets","text":""}` | Run one on-demand shortlist for the active formal jacket slot. Return a View. |
| Same turns endpoint | `{"requestId":"<uuid>","action":"save_rule","text":"I don’t buy final-sale items."}` | Explicit button or buyer instruction. Record it once and return a View, possibly with `memory.state="indexing"`. Keep the original winner identifiable as the pre-rule comparison. Hold handoff until the rule can be evaluated. Recompute in a fresh session from newly retrieved evidence. |
| Same turns endpoint | `{"requestId":"<uuid>","action":"refresh","text":""}` | Recheck indexing/retrieval or refresh the current task. Reuse the same cohort while valid. An expired set requires the buyer to search again or explicitly accept a new set. |
| `POST /api/sessions/{sessionId}/handoff` | `{"requestId":"<uuid>","shortlistId":"set-1","offerId":"offer-b"}` | Return `{"status":"changed","url":null,"note":"...","view":<View>}` with exactly one status. Only a ready, current, qualifying live offer gets its actual HTTPS seller URL in `url`. |

The handoff example shows a changed quote. HTTP 200 always includes the current non-null View. Clear a prior checkout link on every new action or view and discard any stale async response. The four statuses are `ready`, `changed`, `unavailable` and `sample`. Error envelope for non-success HTTP status is `{"error":{"code":"STALE_SHORTLIST","message":"Refresh this shortlist."}}`. Handle unknown trip or offer (404), session/offer mismatch or expired shortlist (409), invalid input (422) and unavailable provider (503 when no usable View exists). Retry a timed-out mutation with the same request ID. A duplicate save across sessions coalesces on buyer + normalized rule. A fresh, independent input gets a new ID. Handoff first calls the server and then displays the verified **Open merchant checkout** anchor. A changed quote returns an updated View for buyer review. A sample returns a null URL and a clear sample explanation. Preserve all attribution in the actual returned URL.

## C2. Response shapes

These are wire types in TypeScript notation. Optional provider evidence such as a photo or citation is explicitly nullable. All IDs are opaque strings. The GUI renders the returned model, selection and verdicts. It does no local ranking.

```ts
type SessionRequest = { tripId: string | null, mode: "live" | "sample" }
type TurnRequest = { requestId: string, action: "message" | "source_jackets" | "save_rule" | "refresh", text: string }
type HandoffRequest = { requestId: string, shortlistId: string, offerId: string }
type HandoffResponse =
  | { status: "ready", url: string, note: string, view: View }
  | { status: "changed" | "unavailable" | "sample", url: null, note: string, view: View }
type ApiError = { error: { code: string, message: string } }
type Verdict = "meets" | "fails" | "unknown"
type ProviderMode = "live" | "sample" | "unavailable" | "unused" | "guided"
type View = {
  schemaVersion: 1
  tripId: string
  sessionId: string
  mode: "live" | "sample"
  reply: string
  providers: { catalog: ProviderMode, senso: ProviderMode, jev: ProviderMode, language: ProviderMode }
  brief: null | {
    month: string, market: string, currency: string, jacketSize: string, jacketCapMinor: number
    assumptions: string[]
    cities: Array<{ name: string, events: Array<{ name: string, dress: "formal" | "informal" }> }>
    needs: Array<{ category: string, quantity: number }>
  }
  memory: { state: "none" | "indexing" | "ready" | "unavailable", ruleText: string | null, evidenceId: string | null }
  shortlist: null | {
    id: string, observedAt: string, slot: "formal_jacket"
    continuity: "first" | "same_set" | "new_search"
    previousWinnerId: string | null, winnerId: string | null, changeNote: string | null
    offers: Offer[]
  }
  evidence: Evidence[]
}
type Offer = {
  id: string, sellerId: string, seller: string, variantId: string, name: string
  size: string | null, imageUrl: string | null, market: string
  available: boolean | null, priceMinor: number | null, currency: string | null
  origin: "shopify_live" | "sample", outcome: Verdict, checks: Check[]
}
type Check = { id: string, label: string, verdict: Verdict, reason: string, evidenceIds: string[] }
type Evidence = {
  id: string, kind: "buyer_brief" | "buyer_rule" | "catalog_variant" | "merchant_policy" | "merchant_reply" | "sample_policy"
  origin: "buyer" | "merchant" | "shopify_live" | "sample", speaker: "agent" | "human" | null
  title: string, quote: string, sourceUrl: string | null, sellerId: string | null
  variantId: string | null, market: string | null, observedAt: string
  senso: null | { contentId: string, kbNodeId: string | null, versionId: string | null, chunkId: string | null, chunkIndex: number | null }
}
```

`observedAt` is ISO 8601 UTC. `priceMinor` is **per one item** in the stated currency. Format from the currency’s minor unit exponent. The fixture is USD. Only one jacket is being handed off. Keep the cost of the other nine open slots unpriced. The active purchase has quantity one. Format 22000 USD as $220.00 and 22000 JPY as ¥22,000 using the currency exponent. Mark the price check Unknown for missing or noncomparable currency or price. Shipping and tax remain undetermined. A null price is unknown, not zero. `winnerId` can be null and always references an eligible offer in the returned set when populated. No checkout URLs appear in a View before handoff. `evidenceIds` point to evidence in this View. An empty list is valid for a missing-evidence Unknown. A provider marked `live` actually ran for this response or its explicitly identified current task result. A local model invocation qualifies and the seller evidence still carries its own origin. Unavailable provenance and missing fields may be shown in compact, human-readable form. A quote is an exact excerpt or an explicitly labeled rendering of structured fields, never a model-invented quotation.

## C3. What the server must prove

**Discovery.** Use `https://catalog.shopify.com/api/ucp/mcp`, JSON-RPC `tools/call`, and `params.arguments.meta["ucp-agent"].profile`. Begin with the versioned Shopify CLI/hosted example profile permitted for a demo, or a reachable operator-owned profile with negotiated capabilities. Verify accepted capabilities in F, including `dev.ucp.shopping.catalog.search`, `dev.ucp.shopping.catalog.lookup` and Shopify’s Global Catalog extension when using its enriched fields. Use `search_catalog` then `get_product` with the returned product/variant ID and exact options. Confirm the **effective** selection, seller, condition, sale-ready status and returned variant. Option relaxation can drop size. A different seller or size requires a different selection. The anonymous tier permits catalog discovery at limited, shared throughput. Start with the 2026-08-25 profile. Use the Global Catalog extension for global and the storefront extension when querying the storefront. Budget one search and up to three exact lookups per sourcing click plus one lookup per checkout attempt. Count retries against that budget. Throttle anonymous requests and support an operator-provided token. External offers have untracked stock and no native checkout. Exclude them and offers missing a verified native handoff from the winner set. Treat absent optional flags according to the negotiated schema. An explicit false flag always excludes. Use documented native seller identity, exact available variant and returned checkout link. A relaxed 42R fails a 40R request. [External offer semantics](https://shopify.dev/docs/agents/catalog/global-catalog-extension) Use the default representation where policy links matter. [Global Catalog and examples](https://shopify.dev/docs/agents/catalog/global-catalog) · [Authentication tiers](https://shopify.dev/docs/agents/profiles/auth-and-rate-limiting)

**Policy and checkout.** A storewide policy is eligible only when it clearly covers this seller, purchase market, sale condition and item, including exceptions. For a real seller, take an official return-policy link from the catalog or verified storefront. Read official merchant terms transiently by default. Store only buyer documents and fictional sample policies in Senso unless the operator has permission for merchant ingestion. Verify coverage of the exact market, variant and price condition, including markdown exceptions. If needed after F, negotiate Ask on the merchant endpoint and resolve a storefront Product/Variant GID. A seller product ID can help locate the storefront variant. Label Ask prose indicative. It can point to the official terms, but only those applicable terms support a live policy verdict. [UCP Ask authority](https://ucp.dev/specification/common/ask/) Treat seller prose and uploaded sources as untrusted content. At handoff re-read that seller and exact variant. Confirm current price, availability, currency, policy applicability and HTTPS seller/checkout destination. Use the variant’s returned `checkout_url` verbatim including attribution. A cart-based flow instead has its own `continue_url` and is outside the core. [Shopify Ask](https://shopify.dev/docs/agents/ask) · [Checkout handoff options](https://shopify.dev/docs/agents/carts-and-checkout)

**Senso.** Server uses `https://apiv2.senso.ai/api/v1` and `X-API-Key`. Ingest allowed material with `POST /org/kb/raw`, retain content ID and KB node ID, poll `GET /org/kb/nodes/{kb_node_id}` for completed processing and retrieve via `POST /org/search/context`. Scope by eligible `content_ids` with `require_scoped_ids:true`, then independently verify returned bindings. Store the content ID and exact excerpt. Map documented content_chunk_id to chunkId when present. Keep vector_id separately if needed. Never invent missing IDs. Retain version/index/node when returned. Use stable opaque buyer, mode and artifact identifiers in the ingested body to distinguish identical rule text across buyers. Send X-Senso-Signals: off on automated searches. Unit tests use offline providers. Bound polling and allow resumption. On duplicate-content 409, reconcile only to a verified existing binding. On missing binding keep the operation pending/failed. On fresh live sessions require a newly scoped passage for each known active rule. SQLite supplies bindings and receipts. A lost response after ingestion can be reconciled only by independently verifying that exact buyer/artifact. If recall fails, set memory unavailable, winner null and hold checkout. With no active rule, the controlled baseline can rank normally. Join relevant sections of one verified policy version in order and inspect exceptions. Top-k hits alone cannot establish that a complete policy has been read. If coverage is incomplete, use Unknown. Never search the whole organization to recover a buyer rule. [Senso quickstart](https://docs.senso.ai/docs/quickstart) · [Scoped retrieval fields](https://docs.senso.ai/docs/concepts)

**Jev.** Use the server-side bearer credential and `POST https://api.typesafe.ai/v1/systemone` with `model`, bounded `state` and a `questions` map. Each ambiguous requirement gets a distinct question with `type:"choice"`, `instructions` and `criteria` mapping `meets`, `fails`, `unknown` to disjoint descriptions. For an active mandatory rule, ask “For this exact offer at the shown price, does the applicable passage establish that the buyer may return this item?” Read `answers[questionId].choice`, `probabilities`, `confidence` and returned model. The app binds each answer to the specific input evidence IDs. Multiple questions may share a request only when their scope and evidence are unambiguous. Separate different merchants. Gate in code on origin, seller, market, effective dates and complete applicable terms. With no admissible evidence, set Unknown and make zero policy calls to Jev. For eligible evidence, send offer, markdown status, exact buyer rule and policy text together. Ask an evidence_suffices Noul and a return_verdict Choice in the same request. Put all meaning in the instructions and state. Route to Unknown unless answers.evidence_suffices.noul and the chosen option’s probability are each at least 0.75 and the selected verdict is conclusive. These are provisional routing heuristics. On timeout retain deterministic checks, mark only the failing provider unavailable and hold the dependent semantic checks. [Noul reference](https://docs.typesafe.ai/primitives/noul) Wrongly scoped, conflicting or missing facts cannot yield Meets. Code compares integers, currencies, availability, exact sizes and explicit measurements. [Jev HTTP reference](https://docs.typesafe.ai/api/system-one) · [Choice](https://docs.typesafe.ai/primitives/choice) · [Confidence](https://docs.typesafe.ai/confidence)

**Ranking and language.** For this demo, hard checks include new item, exact requested size, stock, per-jacket cap and suitability for the formal event. Activate the buyer’s exact no-final-sale rule only after an explicit save. Explicitly applicable final-sale terms fail. Explicit non-final-sale or applicable return rights meet. If exchange/credit-only terms leave final-sale status ambiguous, return Unknown and invite clarification. Add a refund-to-original-payment requirement only if the buyer asks. Hard failures exclude. An unresolved mandatory check makes the offer Unknown. Order eligible offers by ascending comparable unit price then stable offer ID. Ineligible offers stay inspectable. Distinguish an empty shortlist from a shortlist with no eligible winner. Use a general model for optional intent extraction within four seconds. Render explanations from the known decisions and bound IDs. Validate every proposed action and displayed fact. Human text or a button must explicitly authorize a durable save. A model cannot create offers, links, evidence, prices or purchase authority. Log the actual language mode and keep the guided flow operational offline.

## C4. Worked example and adversarial cases

All brands, variants and quotes below are invented. The companion JSON is a full sample response *after* the rule is recalled. Before saving, use the same three offers with no returnability check, no buyer-rule evidence and no policy read required. `memory.state="none"`, `continuity="first"`, and A wins. The after-state uses a different session ID for the same buyer, trip and shortlist.

| Offer | Item price | Sample policy passage | Before | After |
| --- | ---: | --- | --- | --- |
| A · Alder Sample Shop, navy 40R | $180 | “The navy 40R jacket at its current sale price is final sale.” | Meets, first | Fails |
| B · Birch Sample Shop, navy 40R | $220 | “This navy 40R jacket at the displayed price can be returned within 30 days.” | Meets | Meets, first |
| C · Cedar Sample Shop, navy 40R | $245 | “Selected promotions have special terms. Contact us for details.” | Meets | Unknown |

| Test | Setup and expected observation |
| --- | --- |
| T01 · Trip math | Original buyer utterance gives Delhi, Istanbul, Barcelona, June, 3 events per city and 2 × 5 categories. Adding the event cards does not select or purchase products. |
| T02 · Causal flip | On the sample, A → B and C is Unknown. Same three seller/variant keys, same prices and set ID, distinct sessions, fresh Senso read in live memory mode. An extra refresh preserves the old-rule baseline A for the comparison. A new search or price change has a different explanation. |
| T03 · Memory | Double-click save, time out after write, and retry. One logical rule exists. Reopen a new transcript and restart the server separately. Only the former can reuse an in-memory set. A second buyer or nonexistent trip cannot load these passages. |
| T04 · Scope | Decoy text describes another merchant’s navy jacket, another variant, an expired policy, or full-price items at the same seller. A sample policy alongside a live candidate, conflicting messages or unclear exceptions leave the real policy Unknown. |
| T05 · Judgment | Check positive, explicit final sale, “not final sale”, empty, ambiguous, mutually conflicting and low-confidence inputs. Ensure the exact sentence appears in Evidence. A model timeout affects only dependent checks. |
| T06 · Catalog | A cluster contains two sellers, a relaxed size or an out-of-stock offer. After an exact lookup only the valid seller/variant may qualify. Zero, one or two usable offers render correctly. Preserve returned links byte-for-byte. No real data in shipped fixtures. |
| T07 · Checkout | Re-read on click. A price change, missing link, currency mismatch, stock loss or stale shortlist triggers re-evaluation or a visible hold. No substitute, fabricated URL, order submission or “purchased” label. Sample checkout returns no live link. |
| T08 · Price and access | Exact minor units and quantity, null/zero distinction, missing exchange rate and unknown shipping/tax. Simulate timeout, 429, auth failure, no Senso credit, incomplete indexing and local model invalid JSON. Provenance makes each degradation visible. |
| T09 · Buyer interface | Browser test on desktop and mobile widths, keyboard-only input, visible focus and status announcements. Try missing photo, long citation, all Unknown, repeated search, expired session and handoff failure. Network errors keep the buyer’s text. |
| T10 · Optional | Poppy clarification identifies the same seller, specific variant and who answered. Unavailable/fictional evidence stays separate. If Deepgram ships, mic refusal or empty transcript preserves text and no recording auto-submits a preference. |

**Required regression variants.** T02 uses the same trip, empty new transcript, immutable raw candidate set and newly retrieved rule. Removing the rule deliberately in an isolated control gives A. Simulating a failed fetch for a known rule gives no winner. Changing A’s policy to explicitly allow returns at the sale price keeps A first with the rule active. T03 saves identical text for two buyers with distinct bindings and retries the first buyer safely. T04 pairs a US general paragraph with a later discount exclusion. Compute threshold discounts in integer arithmetic from verified, comparable price/list_price. If markdown status or exception coverage is unknown, hold. T05 includes an indicative Ask answer without official terms, an empty passage with zero Jev requests, and a high-confidence answer bound to the wrong seller. T07 checks all four 200 envelopes, a 409 error and clearing an old checkout link on a price change. T08 checks zero, null, USD, JPY and mixed currencies. T09 shows one active and nine unpriced slots with identified brief defaults.

The synthetic 08-wire-examples.json provides complete ready, changed, unavailable, sample and stale-shortlist responses. Its reserved .example destination is for rendering tests only.

A reachable provider is a smoke result. The corresponding test requires its output to reach the rendered buyer workflow. Record each test as observed live, checked on our own samples, failed, or unrun.
