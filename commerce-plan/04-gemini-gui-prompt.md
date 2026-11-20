<!-- BEGIN GUI ASSIGNMENT -->

# Gemini U | Build the buyer interface from a frozen handoff

**When to use.** You are the browser UI author for a small commerce application. Use this assignment **after** the independent plan review, Codex revision, explicit operator start and Phase F contract freeze. The execution copy is `commerce/handoff/gui-packet.md`. It contains the approved contract and observed examples. This planning copy lets you evaluate the full assignment before kickoff. When the operator requests a critique, treat all build instructions here as material to review.

**Your working surface.** Work in an ordinary Gemini chat the operator already has access to. Carbon with High thinking is preferred only when that chat offers it. Report the visible model/setting, or say unavailable. Assume you start with no previous chat, filesystem, keys, live providers or subprocess. Everything required for the UI is in the execution packet. If the frozen version/examples are missing or conflict, identify the exact missing item and ask for it. Never infer a private server response from a public provider’s raw API example.

## U1. Buyer and commercial outcome

The user asks for two new jackets, two trousers, two pairs of shoes, two shirts and two hats for nine June events split across Delhi, Istanbul and Barcelona. This is an on-demand commerce service. Source one formal jacket deeply and display the full shopping brief. The client is fictional. Sample assumptions are a US delivery market, USD, a 40R jacket and a $300 jacket cap. Sample event names are the ones in the supplied brief. A general language model can handle buyer text. The app calls Shopify Catalog for seller variants, Senso for buyer/policy evidence and Jev for narrow judgments. The server computes every comparison, rank and price and supplies the handoff. Do not connect the browser to those services.

## U2. Your three files

Return complete contents for `commerce/web/index.html`, `commerce/web/styles.css` and `commerce/web/app.js`. Use plain HTML, responsive CSS and native JavaScript modules, same-origin requests and semantic controls. The app is served at `/` with assets at `/styles.css` and `/app.js` unless the frozen packet specifies otherwise. No build step, external script, tracking or new package. No inline secrets or external model invocation. State any difference from the packet. In a text-only chat your deliverable is the entire content of the files. The local owner imports and tests them.

Design a credible buying workspace with the buyer’s actual task prominent. On desktop use a narrow trip brief, a wide candidate comparison and a visible evidence panel. On a phone preserve the same reading order, allow choosing an offer/check without horizontal page scrolling, and move focus to Evidence. Use real product photos only when provided in the response. Give a neutral fallback when a photo is missing. Typographic hierarchy, whitespace and a restrained status palette should make the three offers easy to compare. Keep text limited to values, sources, actions, necessary instructions and feedback. Use a system fallback if the chosen readable font is unavailable locally.

## U3. Interaction and truth in the interface

1. Open a new session with an explicit Live or Sample mode. Let the buyer enter/edit the trip wording and send it. Render the server’s cities, events, quantities, market, size and cap. The itinerary is a brief for buying clothes. Compute the total requested from needs. Show “1 of 10 active · 9 open and unpriced” for this brief. Render brief.assumptions as editable demo defaults. Offer the `source_jackets` action on the described trip.
2. For each candidate show seller, item, exact size, unit price/currency, stock and named Meets/Fails/Unknown checks. A buyer can select a check by keyboard. Show its reason and the exact linked buyer or merchant excerpt, origin, source/date and meaningful Senso reference when present. Treat source text as text. Render missing/ambiguous evidence candidly. Label sample evidence even when a provider processed it live. Unit subtotal is one jacket. Format money using its currency exponent. Render nullable Senso references individually. Synthetic IDs remain labeled sample. Show the winner supplied by the server and distinguish unknown/fails even when there is no winner.
3. Support a typed “Remember that I don’t buy final-sale items” and an explicit save control. The control may quote the rule it will save. Keep the initial memory state empty. Wait for `ready`, show `indexing` or `unavailable` honestly, and support refresh. Keep the same request ID for a retry of the same user action. Prevent a late response from replacing a newer trip/session or mode.
4. Place **New conversation for this trip** within easy reach. Call the new-session route with the existing trip and same mode. Clear the visible transcript and retrieve the returned board. Display previous/current recommended item and reason only when the server provides that comparison. Signal `new_search` separately. Never create the flip or compose a pretend seller answer in JavaScript.
5. The purchase button calls the handoff endpoint for this shortlist and exact offer. A `ready` response presents an ordinary HTTPS anchor to open the merchant page, preserving the full URL including attribution. Review unexpected URLs and avoid interpolation into raw HTML. Clear the old anchor on every view, selection or request change. Ignore late responses. Render a ready link only for the current response using target=_blank and rel=noopener noreferrer. A changed quote requires a fresh buyer action on the updated offer. A sample result has a null URL. Support `unavailable` and network errors without losing the draft. The displayed price is the considered unit/subtotal, and tax/shipping may be unknown.
6. Include loading, empty, expired, error, no photo, fewer than three, no eligible candidate, provider unavailable and narrow-screen states. Use visible focus, labels, aria-live for async status, keyboard actions and status text in addition to color. Render supplied seller/product names and source quotes safely with DOM text APIs. No payment form, checkout completion, seller chat, voice, closet or itinerary booking is in this assignment.

## U4. Return to Codex

Aim for one compact message. If full readable files cannot fit, deliver complete files individually with explicit continuation. At minute 135 the local owner checks completeness. First give the contract version/digest the execution packet supplied. Then return one fenced file per exact path, each complete including imports and handlers, in the order HTML, CSS, JavaScript. Do not abbreviate a file with ellipses or directions to copy a previous answer. If your output limit interrupts you, identify the incomplete path. On continuation reissue that entire file. Finish with a short table of local verification steps and expected outcomes for one happy path, an Unknown, save/indexing, a new conversation, a changed quote and a sample handoff. Distinguish any tests you actually executed from suggested tests. End with `END OF GUI DELIVERY`. Pause for the operator. The next phase is Codex integration on GPT-6.2-Astra, High.

<!-- END GUI ASSIGNMENT -->

---

<!-- BEGIN SHARED CONTRACT -->

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

<!-- END SHARED CONTRACT -->

---

<!-- BEGIN SAMPLE VIEW -->

```json
{
  "schemaVersion": 1,
  "tripId": "trip-1",
  "sessionId": "session-fresh",
  "mode": "sample",
  "reply": "Your saved final-sale rule excludes Alder. Birch is the lowest-priced jacket that meets all your requirements.",
  "providers": {
    "catalog": "sample",
    "senso": "sample",
    "jev": "sample",
    "language": "guided"
  },
  "brief": {
    "month": "June",
    "market": "US",
    "currency": "USD",
    "jacketSize": "40R",
    "jacketCapMinor": 30000,
    "cities": [
      {
        "name": "Delhi",
        "events": [
          {
            "name": "Client dinner",
            "dress": "formal"
          },
          {
            "name": "Gallery visit",
            "dress": "informal"
          },
          {
            "name": "Market walk",
            "dress": "informal"
          }
        ]
      },
      {
        "name": "Istanbul",
        "events": [
          {
            "name": "Evening reception",
            "dress": "formal"
          },
          {
            "name": "Ferry outing",
            "dress": "informal"
          },
          {
            "name": "Lunch with friends",
            "dress": "informal"
          }
        ]
      },
      {
        "name": "Barcelona",
        "events": [
          {
            "name": "Closing dinner",
            "dress": "formal"
          },
          {
            "name": "Museum afternoon",
            "dress": "informal"
          },
          {
            "name": "Tapas with friends",
            "dress": "informal"
          }
        ]
      }
    ],
    "needs": [
      {
        "category": "jackets",
        "quantity": 2
      },
      {
        "category": "trousers",
        "quantity": 2
      },
      {
        "category": "pairs of shoes",
        "quantity": 2
      },
      {
        "category": "shirts",
        "quantity": 2
      },
      {
        "category": "hats",
        "quantity": 2
      }
    ],
    "assumptions": [
      "US delivery market",
      "USD",
      "Jacket size 40R",
      "$300 cap per jacket",
      "Proposed event names"
    ]
  },
  "memory": {
    "state": "ready",
    "ruleText": "I don’t buy final-sale items.",
    "evidenceId": "rule-1"
  },
  "shortlist": {
    "id": "set-1",
    "observedAt": "2026-11-20T18:30:00Z",
    "slot": "formal_jacket",
    "continuity": "same_set",
    "previousWinnerId": "offer-a",
    "winnerId": "offer-b",
    "changeNote": "The same three offers were checked against your saved rule. Alder is final sale and Birch is returnable.",
    "offers": [
      {
        "id": "offer-b",
        "sellerId": "seller-b",
        "seller": "Birch Sample Shop",
        "variantId": "sample-b-navy-40r",
        "name": "Birch tailored jacket",
        "size": "40R",
        "imageUrl": null,
        "market": "US",
        "available": true,
        "priceMinor": 22000,
        "currency": "USD",
        "origin": "sample",
        "outcome": "meets",
        "checks": [
          {
            "id": "condition",
            "label": "New item",
            "verdict": "meets",
            "reason": "The offer lists a new jacket.",
            "evidenceIds": [
              "item-b"
            ]
          },
          {
            "id": "size",
            "label": "Exact size",
            "verdict": "meets",
            "reason": "The selected size is 40R.",
            "evidenceIds": [
              "item-b",
              "brief-1"
            ]
          },
          {
            "id": "stock",
            "label": "Availability",
            "verdict": "meets",
            "reason": "This variant is listed as available.",
            "evidenceIds": [
              "item-b"
            ]
          },
          {
            "id": "price",
            "label": "Jacket budget",
            "verdict": "meets",
            "reason": "The unit price is within the $300 cap.",
            "evidenceIds": [
              "item-b",
              "brief-1"
            ]
          },
          {
            "id": "formality",
            "label": "Formal event",
            "verdict": "meets",
            "reason": "The description specifies tailoring for formal dinners.",
            "evidenceIds": [
              "item-b"
            ]
          },
          {
            "id": "returns",
            "label": "Returnability",
            "verdict": "meets",
            "reason": "The policy includes this exact jacket at this price.",
            "evidenceIds": [
              "policy-b",
              "rule-1"
            ]
          }
        ]
      },
      {
        "id": "offer-c",
        "sellerId": "seller-c",
        "seller": "Cedar Sample Shop",
        "variantId": "sample-c-navy-40r",
        "name": "Cedar evening jacket",
        "size": "40R",
        "imageUrl": null,
        "market": "US",
        "available": true,
        "priceMinor": 24500,
        "currency": "USD",
        "origin": "sample",
        "outcome": "unknown",
        "checks": [
          {
            "id": "condition",
            "label": "New item",
            "verdict": "meets",
            "reason": "The offer lists a new jacket.",
            "evidenceIds": [
              "item-c"
            ]
          },
          {
            "id": "size",
            "label": "Exact size",
            "verdict": "meets",
            "reason": "The selected size is 40R.",
            "evidenceIds": [
              "item-c",
              "brief-1"
            ]
          },
          {
            "id": "stock",
            "label": "Availability",
            "verdict": "meets",
            "reason": "This variant is listed as available.",
            "evidenceIds": [
              "item-c"
            ]
          },
          {
            "id": "price",
            "label": "Jacket budget",
            "verdict": "meets",
            "reason": "The unit price is within the $300 cap.",
            "evidenceIds": [
              "item-c",
              "brief-1"
            ]
          },
          {
            "id": "formality",
            "label": "Formal event",
            "verdict": "meets",
            "reason": "The description specifies tailoring for formal dinners.",
            "evidenceIds": [
              "item-c"
            ]
          },
          {
            "id": "returns",
            "label": "Returnability",
            "verdict": "unknown",
            "reason": "The policy leaves this jacket’s terms unclear.",
            "evidenceIds": [
              "policy-c",
              "rule-1"
            ]
          }
        ]
      },
      {
        "id": "offer-a",
        "sellerId": "seller-a",
        "seller": "Alder Sample Shop",
        "variantId": "sample-a-navy-40r",
        "name": "Alder dinner jacket",
        "size": "40R",
        "imageUrl": null,
        "market": "US",
        "available": true,
        "priceMinor": 18000,
        "currency": "USD",
        "origin": "sample",
        "outcome": "fails",
        "checks": [
          {
            "id": "condition",
            "label": "New item",
            "verdict": "meets",
            "reason": "The offer lists a new jacket.",
            "evidenceIds": [
              "item-a"
            ]
          },
          {
            "id": "size",
            "label": "Exact size",
            "verdict": "meets",
            "reason": "The selected size is 40R.",
            "evidenceIds": [
              "item-a",
              "brief-1"
            ]
          },
          {
            "id": "stock",
            "label": "Availability",
            "verdict": "meets",
            "reason": "This variant is listed as available.",
            "evidenceIds": [
              "item-a"
            ]
          },
          {
            "id": "price",
            "label": "Jacket budget",
            "verdict": "meets",
            "reason": "The unit price is within the $300 cap.",
            "evidenceIds": [
              "item-a",
              "brief-1"
            ]
          },
          {
            "id": "formality",
            "label": "Formal event",
            "verdict": "meets",
            "reason": "The description specifies tailoring for formal dinners.",
            "evidenceIds": [
              "item-a"
            ]
          },
          {
            "id": "returns",
            "label": "Returnability",
            "verdict": "fails",
            "reason": "This exact sale item is final sale.",
            "evidenceIds": [
              "policy-a",
              "rule-1"
            ]
          }
        ]
      }
    ]
  },
  "evidence": [
    {
      "id": "brief-1",
      "kind": "buyer_brief",
      "origin": "sample",
      "speaker": null,
      "title": "Fictional client brief",
      "quote": "For formal events, source one new tailored jacket in 40R, up to USD 300. Ship to the United States.",
      "sourceUrl": null,
      "sellerId": null,
      "variantId": null,
      "market": null,
      "observedAt": "2026-11-20T18:30:00Z",
      "senso": null
    },
    {
      "id": "rule-1",
      "kind": "buyer_rule",
      "origin": "sample",
      "speaker": null,
      "title": "Buyer’s saved rule",
      "quote": "I don’t buy final-sale items.",
      "sourceUrl": null,
      "sellerId": null,
      "variantId": null,
      "market": null,
      "observedAt": "2026-11-20T18:30:00Z",
      "senso": {
        "contentId": "sample-content-rule-1",
        "kbNodeId": "sample-node-rule-1",
        "versionId": "sample-version-1",
        "chunkId": null,
        "chunkIndex": 0
      }
    },
    {
      "id": "item-a",
      "kind": "catalog_variant",
      "origin": "sample",
      "speaker": null,
      "title": "Alder Sample Shop · fictional offer",
      "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 180.",
      "sourceUrl": null,
      "sellerId": "seller-a",
      "variantId": "sample-a-navy-40r",
      "market": "US",
      "observedAt": "2026-11-20T18:30:00Z",
      "senso": null
    },
    {
      "id": "policy-a",
      "kind": "sample_policy",
      "origin": "sample",
      "speaker": null,
      "title": "Alder Sample Shop · sample return policy",
      "quote": "The navy 40R jacket at its current sale price is final sale.",
      "sourceUrl": null,
      "sellerId": "seller-a",
      "variantId": "sample-a-navy-40r",
      "market": "US",
      "observedAt": "2026-11-20T18:30:00Z",
      "senso": null
    },
    {
      "id": "item-b",
      "kind": "catalog_variant",
      "origin": "sample",
      "speaker": null,
      "title": "Birch Sample Shop · fictional offer",
      "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 220.",
      "sourceUrl": null,
      "sellerId": "seller-b",
      "variantId": "sample-b-navy-40r",
      "market": "US",
      "observedAt": "2026-11-20T18:30:00Z",
      "senso": null
    },
    {
      "id": "policy-b",
      "kind": "sample_policy",
      "origin": "sample",
      "speaker": null,
      "title": "Birch Sample Shop · sample return policy",
      "quote": "This navy 40R jacket at the displayed price can be returned within 30 days.",
      "sourceUrl": null,
      "sellerId": "seller-b",
      "variantId": "sample-b-navy-40r",
      "market": "US",
      "observedAt": "2026-11-20T18:30:00Z",
      "senso": {
        "contentId": "sample-content-policy-b",
        "kbNodeId": "sample-node-policy-b",
        "versionId": "sample-version-1",
        "chunkId": "sample-chunk-policy-b",
        "chunkIndex": 0
      }
    },
    {
      "id": "item-c",
      "kind": "catalog_variant",
      "origin": "sample",
      "speaker": null,
      "title": "Cedar Sample Shop · fictional offer",
      "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 245.",
      "sourceUrl": null,
      "sellerId": "seller-c",
      "variantId": "sample-c-navy-40r",
      "market": "US",
      "observedAt": "2026-11-20T18:30:00Z",
      "senso": null
    },
    {
      "id": "policy-c",
      "kind": "sample_policy",
      "origin": "sample",
      "speaker": null,
      "title": "Cedar Sample Shop · sample return policy",
      "quote": "Selected promotions have special terms. Contact us for details.",
      "sourceUrl": null,
      "sellerId": "seller-c",
      "variantId": "sample-c-navy-40r",
      "market": "US",
      "observedAt": "2026-11-20T18:30:00Z",
      "senso": null
    }
  ]
}
```

<!-- END SAMPLE VIEW -->

---

<!-- BEGIN WIRE EXAMPLES -->

```json
{
  "description": "Offline synthetic wire examples. Reserved domains and invented identifiers simulate a live-shaped response. Never use these fixtures to issue checkout in the real app.",
  "ready": {
    "status": "ready",
    "url": "https://shop.example/buy/fictional-40r?source=demo",
    "note": "Open the verified checkout.",
    "view": {
      "schemaVersion": 1,
      "tripId": "trip-1",
      "sessionId": "session-fresh",
      "mode": "live",
      "reply": "This synthetic wire example exercises the checkout control.",
      "providers": {
        "catalog": "live",
        "senso": "live",
        "jev": "live",
        "language": "guided"
      },
      "brief": {
        "month": "June",
        "market": "US",
        "currency": "USD",
        "jacketSize": "40R",
        "jacketCapMinor": 30000,
        "cities": [
          {
            "name": "Delhi",
            "events": [
              {
                "name": "Client dinner",
                "dress": "formal"
              },
              {
                "name": "Gallery visit",
                "dress": "informal"
              },
              {
                "name": "Market walk",
                "dress": "informal"
              }
            ]
          },
          {
            "name": "Istanbul",
            "events": [
              {
                "name": "Evening reception",
                "dress": "formal"
              },
              {
                "name": "Ferry outing",
                "dress": "informal"
              },
              {
                "name": "Lunch with friends",
                "dress": "informal"
              }
            ]
          },
          {
            "name": "Barcelona",
            "events": [
              {
                "name": "Closing dinner",
                "dress": "formal"
              },
              {
                "name": "Museum afternoon",
                "dress": "informal"
              },
              {
                "name": "Tapas with friends",
                "dress": "informal"
              }
            ]
          }
        ],
        "needs": [
          {
            "category": "jackets",
            "quantity": 2
          },
          {
            "category": "trousers",
            "quantity": 2
          },
          {
            "category": "pairs of shoes",
            "quantity": 2
          },
          {
            "category": "shirts",
            "quantity": 2
          },
          {
            "category": "hats",
            "quantity": 2
          }
        ],
        "assumptions": [
          "US delivery market",
          "USD",
          "Jacket size 40R",
          "$300 cap per jacket",
          "Proposed event names"
        ]
      },
      "memory": {
        "state": "ready",
        "ruleText": "I don’t buy final-sale items.",
        "evidenceId": "rule-1"
      },
      "shortlist": {
        "id": "set-1",
        "observedAt": "2026-11-20T18:30:00Z",
        "slot": "formal_jacket",
        "continuity": "first",
        "previousWinnerId": null,
        "winnerId": "offer-b",
        "changeNote": null,
        "offers": [
          {
            "id": "offer-b",
            "sellerId": "seller-b",
            "seller": "Birch Sample Shop",
            "variantId": "sample-b-navy-40r",
            "name": "Birch tailored jacket",
            "size": "40R",
            "imageUrl": null,
            "market": "US",
            "available": true,
            "priceMinor": 22000,
            "currency": "USD",
            "origin": "shopify_live",
            "outcome": "meets",
            "checks": [
              {
                "id": "condition",
                "label": "New item",
                "verdict": "meets",
                "reason": "The offer lists a new jacket.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "size",
                "label": "Exact size",
                "verdict": "meets",
                "reason": "The selected size is 40R.",
                "evidenceIds": [
                  "item-b",
                  "brief-1"
                ]
              },
              {
                "id": "stock",
                "label": "Availability",
                "verdict": "meets",
                "reason": "This variant is listed as available.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "price",
                "label": "Jacket budget",
                "verdict": "meets",
                "reason": "The unit price is within the $300 cap.",
                "evidenceIds": [
                  "item-b",
                  "brief-1"
                ]
              },
              {
                "id": "formality",
                "label": "Formal event",
                "verdict": "meets",
                "reason": "The description specifies tailoring for formal dinners.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "returns",
                "label": "Returnability",
                "verdict": "meets",
                "reason": "The policy includes this exact jacket at this price.",
                "evidenceIds": [
                  "policy-b",
                  "rule-1"
                ]
              }
            ]
          }
        ]
      },
      "evidence": [
        {
          "id": "brief-1",
          "kind": "buyer_brief",
          "origin": "buyer",
          "speaker": null,
          "title": "Fictional client brief",
          "quote": "For formal events, source one new tailored jacket in 40R, up to USD 300. Ship to the United States.",
          "sourceUrl": null,
          "sellerId": null,
          "variantId": null,
          "market": null,
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "rule-1",
          "kind": "buyer_rule",
          "origin": "buyer",
          "speaker": null,
          "title": "Buyer’s saved rule",
          "quote": "I don’t buy final-sale items.",
          "sourceUrl": null,
          "sellerId": null,
          "variantId": null,
          "market": null,
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": {
            "contentId": "sample-content-rule-1",
            "kbNodeId": "sample-node-rule-1",
            "versionId": "sample-version-1",
            "chunkId": null,
            "chunkIndex": 0
          }
        },
        {
          "id": "item-b",
          "kind": "catalog_variant",
          "origin": "shopify_live",
          "speaker": null,
          "title": "Birch Sample Shop · fictional offer",
          "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 220.",
          "sourceUrl": null,
          "sellerId": "seller-b",
          "variantId": "sample-b-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "policy-b",
          "kind": "merchant_policy",
          "origin": "merchant",
          "speaker": null,
          "title": "Birch Sample Shop · sample return policy",
          "quote": "This navy 40R jacket at the displayed price can be returned within 30 days.",
          "sourceUrl": "https://shop.example/returns",
          "sellerId": "seller-b",
          "variantId": "sample-b-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        }
      ]
    }
  },
  "changed": {
    "status": "changed",
    "url": null,
    "note": "The price changed to $260. Review the updated offer.",
    "view": {
      "schemaVersion": 1,
      "tripId": "trip-1",
      "sessionId": "session-fresh",
      "mode": "live",
      "reply": "The price changed to $260. Review the updated offer.",
      "providers": {
        "catalog": "live",
        "senso": "live",
        "jev": "live",
        "language": "guided"
      },
      "brief": {
        "month": "June",
        "market": "US",
        "currency": "USD",
        "jacketSize": "40R",
        "jacketCapMinor": 30000,
        "cities": [
          {
            "name": "Delhi",
            "events": [
              {
                "name": "Client dinner",
                "dress": "formal"
              },
              {
                "name": "Gallery visit",
                "dress": "informal"
              },
              {
                "name": "Market walk",
                "dress": "informal"
              }
            ]
          },
          {
            "name": "Istanbul",
            "events": [
              {
                "name": "Evening reception",
                "dress": "formal"
              },
              {
                "name": "Ferry outing",
                "dress": "informal"
              },
              {
                "name": "Lunch with friends",
                "dress": "informal"
              }
            ]
          },
          {
            "name": "Barcelona",
            "events": [
              {
                "name": "Closing dinner",
                "dress": "formal"
              },
              {
                "name": "Museum afternoon",
                "dress": "informal"
              },
              {
                "name": "Tapas with friends",
                "dress": "informal"
              }
            ]
          }
        ],
        "needs": [
          {
            "category": "jackets",
            "quantity": 2
          },
          {
            "category": "trousers",
            "quantity": 2
          },
          {
            "category": "pairs of shoes",
            "quantity": 2
          },
          {
            "category": "shirts",
            "quantity": 2
          },
          {
            "category": "hats",
            "quantity": 2
          }
        ],
        "assumptions": [
          "US delivery market",
          "USD",
          "Jacket size 40R",
          "$300 cap per jacket",
          "Proposed event names"
        ]
      },
      "memory": {
        "state": "ready",
        "ruleText": "I don’t buy final-sale items.",
        "evidenceId": "rule-1"
      },
      "shortlist": {
        "id": "set-1",
        "observedAt": "2026-11-20T18:30:00Z",
        "slot": "formal_jacket",
        "continuity": "first",
        "previousWinnerId": null,
        "winnerId": "offer-b",
        "changeNote": null,
        "offers": [
          {
            "id": "offer-b",
            "sellerId": "seller-b",
            "seller": "Birch Sample Shop",
            "variantId": "sample-b-navy-40r",
            "name": "Birch tailored jacket",
            "size": "40R",
            "imageUrl": null,
            "market": "US",
            "available": true,
            "priceMinor": 26000,
            "currency": "USD",
            "origin": "shopify_live",
            "outcome": "meets",
            "checks": [
              {
                "id": "condition",
                "label": "New item",
                "verdict": "meets",
                "reason": "The offer lists a new jacket.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "size",
                "label": "Exact size",
                "verdict": "meets",
                "reason": "The selected size is 40R.",
                "evidenceIds": [
                  "item-b",
                  "brief-1"
                ]
              },
              {
                "id": "stock",
                "label": "Availability",
                "verdict": "meets",
                "reason": "This variant is listed as available.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "price",
                "label": "Jacket budget",
                "verdict": "meets",
                "reason": "The unit price is within the $300 cap.",
                "evidenceIds": [
                  "item-b",
                  "brief-1"
                ]
              },
              {
                "id": "formality",
                "label": "Formal event",
                "verdict": "meets",
                "reason": "The description specifies tailoring for formal dinners.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "returns",
                "label": "Returnability",
                "verdict": "meets",
                "reason": "The policy includes this exact jacket at this price.",
                "evidenceIds": [
                  "policy-b",
                  "rule-1"
                ]
              }
            ]
          }
        ]
      },
      "evidence": [
        {
          "id": "brief-1",
          "kind": "buyer_brief",
          "origin": "buyer",
          "speaker": null,
          "title": "Fictional client brief",
          "quote": "For formal events, source one new tailored jacket in 40R, up to USD 300. Ship to the United States.",
          "sourceUrl": null,
          "sellerId": null,
          "variantId": null,
          "market": null,
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "rule-1",
          "kind": "buyer_rule",
          "origin": "buyer",
          "speaker": null,
          "title": "Buyer’s saved rule",
          "quote": "I don’t buy final-sale items.",
          "sourceUrl": null,
          "sellerId": null,
          "variantId": null,
          "market": null,
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": {
            "contentId": "sample-content-rule-1",
            "kbNodeId": "sample-node-rule-1",
            "versionId": "sample-version-1",
            "chunkId": null,
            "chunkIndex": 0
          }
        },
        {
          "id": "item-b",
          "kind": "catalog_variant",
          "origin": "shopify_live",
          "speaker": null,
          "title": "Birch Sample Shop · fictional offer",
          "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 260.",
          "sourceUrl": null,
          "sellerId": "seller-b",
          "variantId": "sample-b-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "policy-b",
          "kind": "merchant_policy",
          "origin": "merchant",
          "speaker": null,
          "title": "Birch Sample Shop · sample return policy",
          "quote": "This navy 40R jacket at the displayed price can be returned within 30 days.",
          "sourceUrl": "https://shop.example/returns",
          "sellerId": "seller-b",
          "variantId": "sample-b-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        }
      ]
    }
  },
  "unavailable": {
    "status": "unavailable",
    "url": null,
    "note": "Retrieve the saved rule before continuing.",
    "view": {
      "schemaVersion": 1,
      "tripId": "trip-1",
      "sessionId": "session-fresh",
      "mode": "live",
      "reply": "Retrieve the saved rule before continuing.",
      "providers": {
        "catalog": "live",
        "senso": "unavailable",
        "jev": "live",
        "language": "guided"
      },
      "brief": {
        "month": "June",
        "market": "US",
        "currency": "USD",
        "jacketSize": "40R",
        "jacketCapMinor": 30000,
        "cities": [
          {
            "name": "Delhi",
            "events": [
              {
                "name": "Client dinner",
                "dress": "formal"
              },
              {
                "name": "Gallery visit",
                "dress": "informal"
              },
              {
                "name": "Market walk",
                "dress": "informal"
              }
            ]
          },
          {
            "name": "Istanbul",
            "events": [
              {
                "name": "Evening reception",
                "dress": "formal"
              },
              {
                "name": "Ferry outing",
                "dress": "informal"
              },
              {
                "name": "Lunch with friends",
                "dress": "informal"
              }
            ]
          },
          {
            "name": "Barcelona",
            "events": [
              {
                "name": "Closing dinner",
                "dress": "formal"
              },
              {
                "name": "Museum afternoon",
                "dress": "informal"
              },
              {
                "name": "Tapas with friends",
                "dress": "informal"
              }
            ]
          }
        ],
        "needs": [
          {
            "category": "jackets",
            "quantity": 2
          },
          {
            "category": "trousers",
            "quantity": 2
          },
          {
            "category": "pairs of shoes",
            "quantity": 2
          },
          {
            "category": "shirts",
            "quantity": 2
          },
          {
            "category": "hats",
            "quantity": 2
          }
        ],
        "assumptions": [
          "US delivery market",
          "USD",
          "Jacket size 40R",
          "$300 cap per jacket",
          "Proposed event names"
        ]
      },
      "memory": {
        "state": "unavailable",
        "ruleText": null,
        "evidenceId": null
      },
      "shortlist": {
        "id": "set-1",
        "observedAt": "2026-11-20T18:30:00Z",
        "slot": "formal_jacket",
        "continuity": "first",
        "previousWinnerId": null,
        "winnerId": null,
        "changeNote": null,
        "offers": [
          {
            "id": "offer-b",
            "sellerId": "seller-b",
            "seller": "Birch Sample Shop",
            "variantId": "sample-b-navy-40r",
            "name": "Birch tailored jacket",
            "size": "40R",
            "imageUrl": null,
            "market": "US",
            "available": true,
            "priceMinor": 22000,
            "currency": "USD",
            "origin": "shopify_live",
            "outcome": "unknown",
            "checks": [
              {
                "id": "condition",
                "label": "New item",
                "verdict": "meets",
                "reason": "The offer lists a new jacket.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "size",
                "label": "Exact size",
                "verdict": "meets",
                "reason": "The selected size is 40R.",
                "evidenceIds": [
                  "item-b",
                  "brief-1"
                ]
              },
              {
                "id": "stock",
                "label": "Availability",
                "verdict": "meets",
                "reason": "This variant is listed as available.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "price",
                "label": "Jacket budget",
                "verdict": "meets",
                "reason": "The unit price is within the $300 cap.",
                "evidenceIds": [
                  "item-b",
                  "brief-1"
                ]
              },
              {
                "id": "formality",
                "label": "Formal event",
                "verdict": "meets",
                "reason": "The description specifies tailoring for formal dinners.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "returns",
                "label": "Returnability",
                "verdict": "unknown",
                "reason": "Saved buyer rule could not be retrieved.",
                "evidenceIds": []
              }
            ]
          }
        ]
      },
      "evidence": [
        {
          "id": "brief-1",
          "kind": "buyer_brief",
          "origin": "buyer",
          "speaker": null,
          "title": "Fictional client brief",
          "quote": "For formal events, source one new tailored jacket in 40R, up to USD 300. Ship to the United States.",
          "sourceUrl": null,
          "sellerId": null,
          "variantId": null,
          "market": null,
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "item-b",
          "kind": "catalog_variant",
          "origin": "shopify_live",
          "speaker": null,
          "title": "Birch Sample Shop · fictional offer",
          "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 220.",
          "sourceUrl": null,
          "sellerId": "seller-b",
          "variantId": "sample-b-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "policy-b",
          "kind": "merchant_policy",
          "origin": "merchant",
          "speaker": null,
          "title": "Birch Sample Shop · sample return policy",
          "quote": "This navy 40R jacket at the displayed price can be returned within 30 days.",
          "sourceUrl": "https://shop.example/returns",
          "sellerId": "seller-b",
          "variantId": "sample-b-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        }
      ]
    }
  },
  "sample": {
    "status": "sample",
    "url": null,
    "note": "Sample checkout only.",
    "view": {
      "schemaVersion": 1,
      "tripId": "trip-1",
      "sessionId": "session-fresh",
      "mode": "sample",
      "reply": "Your saved final-sale rule excludes Alder. Birch is the lowest-priced jacket that meets all your requirements.",
      "providers": {
        "catalog": "sample",
        "senso": "sample",
        "jev": "sample",
        "language": "guided"
      },
      "brief": {
        "month": "June",
        "market": "US",
        "currency": "USD",
        "jacketSize": "40R",
        "jacketCapMinor": 30000,
        "cities": [
          {
            "name": "Delhi",
            "events": [
              {
                "name": "Client dinner",
                "dress": "formal"
              },
              {
                "name": "Gallery visit",
                "dress": "informal"
              },
              {
                "name": "Market walk",
                "dress": "informal"
              }
            ]
          },
          {
            "name": "Istanbul",
            "events": [
              {
                "name": "Evening reception",
                "dress": "formal"
              },
              {
                "name": "Ferry outing",
                "dress": "informal"
              },
              {
                "name": "Lunch with friends",
                "dress": "informal"
              }
            ]
          },
          {
            "name": "Barcelona",
            "events": [
              {
                "name": "Closing dinner",
                "dress": "formal"
              },
              {
                "name": "Museum afternoon",
                "dress": "informal"
              },
              {
                "name": "Tapas with friends",
                "dress": "informal"
              }
            ]
          }
        ],
        "needs": [
          {
            "category": "jackets",
            "quantity": 2
          },
          {
            "category": "trousers",
            "quantity": 2
          },
          {
            "category": "pairs of shoes",
            "quantity": 2
          },
          {
            "category": "shirts",
            "quantity": 2
          },
          {
            "category": "hats",
            "quantity": 2
          }
        ],
        "assumptions": [
          "US delivery market",
          "USD",
          "Jacket size 40R",
          "$300 cap per jacket",
          "Proposed event names"
        ]
      },
      "memory": {
        "state": "ready",
        "ruleText": "I don’t buy final-sale items.",
        "evidenceId": "rule-1"
      },
      "shortlist": {
        "id": "set-1",
        "observedAt": "2026-11-20T18:30:00Z",
        "slot": "formal_jacket",
        "continuity": "same_set",
        "previousWinnerId": "offer-a",
        "winnerId": "offer-b",
        "changeNote": "The same three offers were checked against your saved rule. Alder is final sale and Birch is returnable.",
        "offers": [
          {
            "id": "offer-b",
            "sellerId": "seller-b",
            "seller": "Birch Sample Shop",
            "variantId": "sample-b-navy-40r",
            "name": "Birch tailored jacket",
            "size": "40R",
            "imageUrl": null,
            "market": "US",
            "available": true,
            "priceMinor": 22000,
            "currency": "USD",
            "origin": "sample",
            "outcome": "meets",
            "checks": [
              {
                "id": "condition",
                "label": "New item",
                "verdict": "meets",
                "reason": "The offer lists a new jacket.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "size",
                "label": "Exact size",
                "verdict": "meets",
                "reason": "The selected size is 40R.",
                "evidenceIds": [
                  "item-b",
                  "brief-1"
                ]
              },
              {
                "id": "stock",
                "label": "Availability",
                "verdict": "meets",
                "reason": "This variant is listed as available.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "price",
                "label": "Jacket budget",
                "verdict": "meets",
                "reason": "The unit price is within the $300 cap.",
                "evidenceIds": [
                  "item-b",
                  "brief-1"
                ]
              },
              {
                "id": "formality",
                "label": "Formal event",
                "verdict": "meets",
                "reason": "The description specifies tailoring for formal dinners.",
                "evidenceIds": [
                  "item-b"
                ]
              },
              {
                "id": "returns",
                "label": "Returnability",
                "verdict": "meets",
                "reason": "The policy includes this exact jacket at this price.",
                "evidenceIds": [
                  "policy-b",
                  "rule-1"
                ]
              }
            ]
          },
          {
            "id": "offer-c",
            "sellerId": "seller-c",
            "seller": "Cedar Sample Shop",
            "variantId": "sample-c-navy-40r",
            "name": "Cedar evening jacket",
            "size": "40R",
            "imageUrl": null,
            "market": "US",
            "available": true,
            "priceMinor": 24500,
            "currency": "USD",
            "origin": "sample",
            "outcome": "unknown",
            "checks": [
              {
                "id": "condition",
                "label": "New item",
                "verdict": "meets",
                "reason": "The offer lists a new jacket.",
                "evidenceIds": [
                  "item-c"
                ]
              },
              {
                "id": "size",
                "label": "Exact size",
                "verdict": "meets",
                "reason": "The selected size is 40R.",
                "evidenceIds": [
                  "item-c",
                  "brief-1"
                ]
              },
              {
                "id": "stock",
                "label": "Availability",
                "verdict": "meets",
                "reason": "This variant is listed as available.",
                "evidenceIds": [
                  "item-c"
                ]
              },
              {
                "id": "price",
                "label": "Jacket budget",
                "verdict": "meets",
                "reason": "The unit price is within the $300 cap.",
                "evidenceIds": [
                  "item-c",
                  "brief-1"
                ]
              },
              {
                "id": "formality",
                "label": "Formal event",
                "verdict": "meets",
                "reason": "The description specifies tailoring for formal dinners.",
                "evidenceIds": [
                  "item-c"
                ]
              },
              {
                "id": "returns",
                "label": "Returnability",
                "verdict": "unknown",
                "reason": "The policy leaves this jacket’s terms unclear.",
                "evidenceIds": [
                  "policy-c",
                  "rule-1"
                ]
              }
            ]
          },
          {
            "id": "offer-a",
            "sellerId": "seller-a",
            "seller": "Alder Sample Shop",
            "variantId": "sample-a-navy-40r",
            "name": "Alder dinner jacket",
            "size": "40R",
            "imageUrl": null,
            "market": "US",
            "available": true,
            "priceMinor": 18000,
            "currency": "USD",
            "origin": "sample",
            "outcome": "fails",
            "checks": [
              {
                "id": "condition",
                "label": "New item",
                "verdict": "meets",
                "reason": "The offer lists a new jacket.",
                "evidenceIds": [
                  "item-a"
                ]
              },
              {
                "id": "size",
                "label": "Exact size",
                "verdict": "meets",
                "reason": "The selected size is 40R.",
                "evidenceIds": [
                  "item-a",
                  "brief-1"
                ]
              },
              {
                "id": "stock",
                "label": "Availability",
                "verdict": "meets",
                "reason": "This variant is listed as available.",
                "evidenceIds": [
                  "item-a"
                ]
              },
              {
                "id": "price",
                "label": "Jacket budget",
                "verdict": "meets",
                "reason": "The unit price is within the $300 cap.",
                "evidenceIds": [
                  "item-a",
                  "brief-1"
                ]
              },
              {
                "id": "formality",
                "label": "Formal event",
                "verdict": "meets",
                "reason": "The description specifies tailoring for formal dinners.",
                "evidenceIds": [
                  "item-a"
                ]
              },
              {
                "id": "returns",
                "label": "Returnability",
                "verdict": "fails",
                "reason": "This exact sale item is final sale.",
                "evidenceIds": [
                  "policy-a",
                  "rule-1"
                ]
              }
            ]
          }
        ]
      },
      "evidence": [
        {
          "id": "brief-1",
          "kind": "buyer_brief",
          "origin": "sample",
          "speaker": null,
          "title": "Fictional client brief",
          "quote": "For formal events, source one new tailored jacket in 40R, up to USD 300. Ship to the United States.",
          "sourceUrl": null,
          "sellerId": null,
          "variantId": null,
          "market": null,
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "rule-1",
          "kind": "buyer_rule",
          "origin": "sample",
          "speaker": null,
          "title": "Buyer’s saved rule",
          "quote": "I don’t buy final-sale items.",
          "sourceUrl": null,
          "sellerId": null,
          "variantId": null,
          "market": null,
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": {
            "contentId": "sample-content-rule-1",
            "kbNodeId": "sample-node-rule-1",
            "versionId": "sample-version-1",
            "chunkId": null,
            "chunkIndex": 0
          }
        },
        {
          "id": "item-a",
          "kind": "catalog_variant",
          "origin": "sample",
          "speaker": null,
          "title": "Alder Sample Shop · fictional offer",
          "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 180.",
          "sourceUrl": null,
          "sellerId": "seller-a",
          "variantId": "sample-a-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "policy-a",
          "kind": "sample_policy",
          "origin": "sample",
          "speaker": null,
          "title": "Alder Sample Shop · sample return policy",
          "quote": "The navy 40R jacket at its current sale price is final sale.",
          "sourceUrl": null,
          "sellerId": "seller-a",
          "variantId": "sample-a-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "item-b",
          "kind": "catalog_variant",
          "origin": "sample",
          "speaker": null,
          "title": "Birch Sample Shop · fictional offer",
          "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 220.",
          "sourceUrl": null,
          "sellerId": "seller-b",
          "variantId": "sample-b-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "policy-b",
          "kind": "sample_policy",
          "origin": "sample",
          "speaker": null,
          "title": "Birch Sample Shop · sample return policy",
          "quote": "This navy 40R jacket at the displayed price can be returned within 30 days.",
          "sourceUrl": null,
          "sellerId": "seller-b",
          "variantId": "sample-b-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": {
            "contentId": "sample-content-policy-b",
            "kbNodeId": "sample-node-policy-b",
            "versionId": "sample-version-1",
            "chunkId": "sample-chunk-policy-b",
            "chunkIndex": 0
          }
        },
        {
          "id": "item-c",
          "kind": "catalog_variant",
          "origin": "sample",
          "speaker": null,
          "title": "Cedar Sample Shop · fictional offer",
          "quote": "New navy tailored jacket for formal dinners. Size 40R is available at USD 245.",
          "sourceUrl": null,
          "sellerId": "seller-c",
          "variantId": "sample-c-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        },
        {
          "id": "policy-c",
          "kind": "sample_policy",
          "origin": "sample",
          "speaker": null,
          "title": "Cedar Sample Shop · sample return policy",
          "quote": "Selected promotions have special terms. Contact us for details.",
          "sourceUrl": null,
          "sellerId": "seller-c",
          "variantId": "sample-c-navy-40r",
          "market": "US",
          "observedAt": "2026-11-20T18:30:00Z",
          "senso": null
        }
      ]
    }
  },
  "error": {
    "error": {
      "code": "STALE_SHORTLIST",
      "message": "Refresh this shortlist."
    }
  }
}
```

<!-- END WIRE EXAMPLES -->

END OF GUI PACKET
