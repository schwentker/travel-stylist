# Commerce interface and acceptance cases | v0.1 candidate

This is the boundary between the local server and a browser UI authored in a fresh chat. Examples are application data invented for the demo. The raw responses from Shopify, Senso and Jev are different shapes. Phase F fixes version `1` or issues an explicit replacement before the two builders start. All public names below are case sensitive.

## C1. Browser requests

All requests go to the same origin and return JSON. An opaque session is bound server-side to the demo client and trip. The client cannot select another buyer by changing a request field. Every session starts with an empty transcript. An unsupported input returns an actionable response, or a structured error where appropriate.

| Request | Body | Success |
| --- | --- | --- |
| `POST /api/sessions` | `{"tripId":null,"mode":"sample"}` or `"live"` | New task. Return a View with an assigned trip and session ID, `brief:null` and `shortlist:null`. |
| `POST /api/sessions` | `{"tripId":"trip-1","mode":"sample"}` | Reopen the same buyer’s trip in a **new** session. Reload the trip and retrieve active rules from Senso in live mode. Reuse only an unexpired shortlist for that task and mode. Return the latest View. |
| `POST /api/sessions/{sessionId}/turns` | `{"requestId":"<uuid>","action":"message","text":"<buyer text>"}` | Parse a new brief, answer an evidence question or recognize an explicit save. Return a View. A parsed brief alone can return `shortlist:null`. |
| Same turns endpoint | `{"requestId":"<uuid>","action":"source_jackets","text":""}` | Run one on-demand shortlist for the active formal jacket slot. Return a View. |
| Same turns endpoint | `{"requestId":"<uuid>","action":"save_rule","text":"I don’t buy final-sale items."}` | Explicit button or buyer instruction. Record it once and return a View, possibly with `memory.state="indexing"`. The re-ranked view may be shown on this turn and must be reproducible in a fresh session. |
| Same turns endpoint | `{"requestId":"<uuid>","action":"refresh","text":""}` | Recheck indexing/retrieval or refresh the current task. Reuse the same cohort while valid. An expired set requires the buyer to search again or explicitly accept a new set. |
| `POST /api/sessions/{sessionId}/handoff` | `{"requestId":"<uuid>","shortlistId":"set-1","offerId":"offer-b"}` | Return `{"status":"changed","url":null,"note":"...","view":<View>}` with exactly one status. Only a ready, current, qualifying live offer gets its actual HTTPS seller URL in `url`. |

The handoff example shows a changed quote. The four statuses are `ready`, `changed`, `unavailable` and `sample`. Error envelope for non-success HTTP status is `{"error":{"code":"STALE_SHORTLIST","message":"Refresh this shortlist."}}`. Handle unknown trip or offer (404), session/offer mismatch or expired shortlist (409), invalid input (422) and unavailable provider (503 when no usable View exists). Retry a timed-out mutation with the same request ID. A duplicate save across sessions coalesces on buyer + normalized rule. A fresh, independent input gets a new ID. Handoff first calls the server and then displays the verified **Open merchant checkout** anchor. A changed quote returns an updated View for buyer review. A sample returns a null URL and a clear sample explanation. Preserve all attribution in the actual returned URL.

## C2. Response shapes

These are wire types in TypeScript notation. Optional provider evidence such as a photo or citation is explicitly nullable. All IDs are opaque strings. The GUI renders the returned model, selection and verdicts. It does no local ranking.

```ts
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
  senso: null | { contentId: string, versionId: string, chunkId: string, chunkIndex: number }
}
```

`observedAt` is ISO 8601 UTC. `priceMinor` is **per one item** in the stated currency. Format from the currency’s minor unit exponent. The fixture is USD. Only one jacket is being handed off. Keep the cost of the other nine open slots unpriced. Sum quantities in integer minor units within one currency and mark tax and shipping as undetermined. A null price is unknown, not zero. `winnerId` can be null and always references an eligible offer in the returned set when populated. No checkout URLs appear in a View before handoff. `evidenceIds` point to evidence in this View. An empty list is valid for a missing-evidence Unknown. A provider marked `live` actually ran for this response or its explicitly identified current task result. A local model invocation qualifies and the seller evidence still carries its own origin. Unavailable provenance and missing fields may be shown in compact, human-readable form. A quote is an exact excerpt or an explicitly labeled rendering of structured fields, never a model-invented quotation.

## C3. What the server must prove

**Discovery.** Use `https://catalog.shopify.com/api/ucp/mcp`, JSON-RPC `tools/call`, and `params.arguments.meta["ucp-agent"].profile`. Begin with the versioned Shopify CLI/hosted example profile permitted for a demo, or a reachable operator-owned profile with negotiated capabilities. Verify accepted capabilities in F, including `dev.ucp.shopping.catalog.search`, `dev.ucp.shopping.catalog.lookup` and Shopify’s Global Catalog extension when using its enriched fields. Use `search_catalog` then `get_product` with the returned product/variant ID and exact options. Confirm the **effective** selection, seller, condition, sale-ready status and returned variant. Option relaxation can drop size. A different seller or size requires a different selection. The anonymous tier permits catalog discovery at limited, shared throughput. Respect rate limits, bounded retries and a small on-demand result count. Use the default representation where policy links matter. [Global Catalog and examples](https://shopify.dev/docs/agents/catalog/global-catalog) · [Authentication tiers](https://shopify.dev/docs/agents/profiles/auth-and-rate-limiting)

**Policy and checkout.** A storewide policy is eligible only when it clearly covers this seller, purchase market, sale condition and item, including exceptions. For a real seller, take an official return-policy link from the catalog or verified storefront. A human-reviewed short excerpt may be added to Senso where permitted. Alternatively, if the store advertises `dev.ucp.common.ask`, ask one product-specific question and retain the attributable response and relevant policy link. `ask_business` takes a store’s Product/Variant GID from Storefront Catalog. A global UPID cannot substitute for it. Defer if the mapping or facts cannot be established. Treat seller prose and uploaded sources as untrusted content. At handoff re-read that seller and exact variant. Confirm current price, availability, currency, policy applicability and HTTPS seller/checkout destination. Use the variant’s returned `checkout_url` verbatim including attribution. A cart-based flow instead has its own `continue_url` and is outside the core. [Shopify Ask](https://shopify.dev/docs/agents/ask) · [Checkout handoff options](https://shopify.dev/docs/agents/carts-and-checkout)

**Senso.** Server uses `https://apiv2.senso.ai/api/v1` and `X-API-Key`. Ingest allowed material with `POST /org/kb/raw`, retain content ID and KB node ID, poll `GET /org/kb/nodes/{kb_node_id}` for completed processing and retrieve via `POST /org/search/context`. Scope by eligible `content_ids` with `require_scoped_ids:true`, then independently verify returned bindings. Store/present the actual content, version, chunk ID/index and passage. Bound polling and allow resumption. On duplicate-content 409, reconcile only to a verified existing binding. On missing binding keep the operation pending/failed. Never search the whole organization to recover a buyer rule. [Senso quickstart](https://docs.senso.ai/docs/quickstart) · [Scoped retrieval fields](https://docs.senso.ai/docs/concepts)

**Jev.** Use the server-side bearer credential and `POST https://api.typesafe.ai/v1/systemone` with `model`, bounded `state` and a `questions` map. Each ambiguous requirement gets a distinct question with `type:"choice"`, `instructions` and `criteria` mapping `meets`, `fails`, `unknown` to disjoint descriptions. For an active mandatory rule, ask “For this exact offer at the shown price, does the applicable passage establish that the buyer may return this item?” Read `answers[questionId].choice`, `probabilities`, `confidence` and returned model. The app binds each answer to the specific input evidence IDs. Multiple questions may share a request only when their scope and evidence are unambiguous. Separate different merchants. A low-confidence choice routes to Unknown under an explicit, tested threshold. Wrongly scoped, conflicting or missing facts cannot yield Meets. Code compares integers, currencies, availability, exact sizes and explicit measurements. [Jev HTTP reference](https://docs.typesafe.ai/api/system-one) · [Choice](https://docs.typesafe.ai/primitives/choice) · [Confidence](https://docs.typesafe.ai/confidence)

**Ranking and language.** For this demo, hard checks include new item, exact requested size, stock, per-jacket cap and suitability for the formal event. Add returnability only when the buyer activates the rule, including mandatory gift/credit-only limitations only if the buyer explicitly specified them. Hard failures exclude. An unresolved mandatory check makes the offer Unknown. Order eligible offers by ascending comparable unit price then stable offer ID. Ineligible offers stay inspectable. Distinguish an empty shortlist from a shortlist with no eligible winner. A general model can map text to proposed actions or explain a known decision using bound IDs. Validate every proposed action and displayed fact. Human text or a button must explicitly authorize a durable save. A model cannot create offers, links, evidence, prices or purchase authority. Log the actual language mode and keep the guided flow operational offline.

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

A reachable provider is a smoke result. The corresponding test requires its output to reach the rendered buyer workflow. Record each test as observed live, checked on our own samples, failed, or unrun.
