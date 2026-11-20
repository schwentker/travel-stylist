# First message to Gemini | Independently pressure-test the commerce build

In any Gemini chat you already have access to, attach this one file and send “Read the entire attached packet and perform G0 only. Return the critique for Codex. Do not start the build.” You may also paste the file. If the chat splits the input, send it in order in one conversation and wait for the end marker before requesting the review. Choose Carbon and High thinking if that particular chat exposes them. Use its strongest available reasoning setting otherwise. No Google Cloud Agent Studio, API, repo access or paid upgrade is required.

This v0.2 packet is retained for a repeat review if requested. The initial critique and Codex revision are complete.

## G0. Your assignment

Act as a skeptical commerce engineer, buyer and demo judge. You have no inherited context. The material below includes the complete proposed master plan, proposed wire contract, sample response and future Codex/Gemini prompts. Those future prompts are **documents under review**. Your only deliverable now is a detailed critique for the operator to return to Codex. Do not implement, edit files, ingest data, contact sellers, call a paid API or claim to have run tests. A public documentation link may be read if your surface supports it. Otherwise identify which assertions you could not verify. Record the visible model and thinking setting if known.

The builder has 330 elapsed minutes **after** review, revision and explicit start. One Codex operates locally. You may later author three GUI files in chat against a fixed contract. The buyer wants ten new items for nine events in Delhi, Istanbul and Barcelona in June. The live proof is one formal jacket decision with a Shopify merchant handoff. Senso owns retrieved rules/passages, Jev owns narrow typed interpretations, ordinary code owns exact comparisons/prices, and a general language model or labeled guided fallback handles turns. The demo earns its claim only if the remembered rule and the merchant evidence actually determine the result.

## G1. Try to disprove these claims

For each area, identify the concrete failure case, what the buyer would see, the minimum fix and the fastest verification. Cite primarily the supplied official sources, distinguish documented behavior from inference, and report genuine uncertainty. If an area is sound, say which test would demonstrate it. Give the most attention to findings that could invalidate the demo.

1. **Can the buyer tell what was delivered?** Count the cities, events, garments and quantities. Distinguish the other nine open purchase slots from one shoppable jacket. Critique the first screen, 90-second narration and final click. Identify any claim of styling nine complete outfits, total basket price, certain stock or completed purchase that the data does not support.
2. **Does Shopify produce the offer we show?** Trace one search → universal product cluster → seller/variant → effective options → availability → currency/minor units → real seller checkout URL, including attribution. Check exact option relaxation, per-market prices, required platform profile/version/capabilities, limited anonymous traffic, fewer than three offers, missing fields and failed checkout refresh. If you propose Shopify Ask, explain how a Storefront variant GID is obtained and what happens when only a Global UPID exists. Identify which assumptions a 10-minute real probe must settle.
3. **Is “the agent remembered” falsifiable?** Walk the first turn, explicit save, asynchronous indexing, fresh session, scoped retrieval, re-rank and restart. Show what counterfactual run would still pick A. Try duplicate saves, ambiguous “I saw final sale,” a delayed write and the same phrase in another buyer’s docs. Identify everything that could fake the result, including hidden prompts, a pre-seeded rule, an old chat transcript, a new catalog result or a UI-hardcoded winner.
4. **Can each claim be traced to the right seller and rule?** Attack merchant/product/variant/price-condition/market/date bindings. Include a markdown sale, an expired exception, a contradictory general policy and a sample policy returned by a live retrieval service. Say when a direct seller reply is enough to rely on, when more evidence is needed, and how the interface should display unresolved cases.
5. **Is Jev doing a necessary, bounded job?** Inspect the proposed Choice state, criteria, response fields, source binding and confidence handling. Try negation and missing/mixed passages. Separate deterministic operations from interpretation. Evaluate whether the small labeled cases allow a demo routing threshold, and what confidence can establish. Check behavior if Jev or Senso times out mid-rank.
6. **Is the ranking numerically and causally correct?** Manually compute the fixture winner before and after. Change one variable at a time (different size, wrong currency, null price, partial set, price movement at checkout). Specify which checks turn Unknown/Fails and whether a real buyer should see a checkout link. Check displayed unit/subtotal, tax, shipping and currency exponent.
7. **Could the GUI actually be built in a blank, text-only chat?** Check every UI control against a route, JSON field and error case. Look for missing starter files, implicit dependencies, stale results, empty data, status accessibility, mobile handling, unsafe text interpolation and truncated file delivery. Name the smallest missing example or contract change. Separate what the GUI can do before live services work from what requires the actual backend.
8. **Can the calendar work with one local integrator?** Recalculate elapsed minutes, identify a real dependency graph and the critical path. Challenge account access, source-policy preparation time, cold model latency, write collisions, manual transfer/review time and a late/truncated GUI. Give both the two-stream and single-builder schedule with a 30-minute rehearsal buffer. Identify one timebox with a cut trigger.
9. **Does each optional integration earn its time?** Identify what Shopify Ask already handles. Compare that with Poppy’s merchant discovery, signed sessions, conversation and human escalation. A fictional test merchant proves only its own integration. Consider mic failure, stale transcript and a buyer correcting dictated text. Name which optional work you would cut first. These do not gate the core shopping flow.
10. **Where could we mislabel evidence, spend money or keep too much data?** Distinguish non-billable Google access, a locally installed model versus observed inference, provider credentials or quotas, and authentic versus sample sources. Check on-demand Shopify use, minimal persistence, seller data shown to an external coding model, and the provenance of the final demo. A failed external provider must never silently turn into a claimed live result.

## G2. Return one actionable critique

Use the following sections so Codex can act on the reply without another interview. Aim for detailed findings with a counterexample and exact replacement wording instead of generic best practices. If the output limit is tight, finish the blockers and the handback first. Mark anything omitted.

- **Kickoff verdict.** Choose Ship, Ship with cuts, or Redesign. Name the single assumption most likely to sink the live demonstration and the first step to falsify it.
- **Findings by severity.** Assign stable IDs G-01, G-02 and so on. For each give blocker/major/minor, plan or prompt section, exact claim, failure example, impact, smallest change, owner, test and primary source or “unverified”. Include defensible strengths worth preserving.
- **Worked purchase trace.** Give before/after/unknown for A, B and C, the precise cause of the flip, and the observable evidence for a real live run. Supply a counterexample that should keep the winner unchanged. Explain the fallback when no genuine live flip is available.
- **Dependency and access audit.** Give parallel and serial schedules in elapsed minutes, including transfer and integration. List what the operator must already have, what Codex can discover at kickoff, and what a text-only Gemini could never directly verify. Call out hidden producers of required files.
- **Exact edits for Codex.** Include an indexed patch list with document, section, replacement text and acceptance test. Audit G0, R, F, B, U, I, Q, X and V where relevant. Propose the smallest changes that repair the plan within 330 minutes.
- **Final handback.** List essential kickoff probes, optional cuts in order and at most three unresolved questions that truly affect scope. Each open question needs a default that allows progress. End with `END OF GEMINI CRITIQUE`. Stop there.

The appendices that follow are the exact proposal for review. The last line of the complete packet is `END OF REVIEW PACKET`.

---

<!-- BEGIN MASTER PLAN -->

# Travel commerce demo | Master plan v0.2

**Revision complete · November 20, 2026.** Gemini returned its critique and Codex reconciled it with the provider documentation. The next phase is F, using GPT-6.2-Astra at XHigh. Start the 330-minute clock only on the operator’s explicit kickoff. At every subsequent phase boundary, report the result, name the next model and effort even if identical, and wait for the operator to continue. B and U are one explicitly released parallel wave.

## M1. What the buyer sees

The buyer types “I’m going to Delhi, Istanbul and Barcelona in June. I have three events in each city, a mix of formal and informal. I need two new jackets, two pairs of trousers, two pairs of shoes, two shirts and two hats.” The brief shows nine event slots and ten requested purchases. Focus the live sourcing on **one of the two jackets**, for the formal events. The other nine shopping slots remain open. Trying to find ten verified products, dress nine events and prove three external integrations in this window would dilute the buying decision.

| City | Formal event | Two informal events |
| --- | --- | --- |
| Delhi | Client dinner | Gallery visit, market walk |
| Istanbul | Evening reception | Ferry outing, lunch with friends |
| Barcelona | Closing dinner | Museum afternoon, tapas with friends |

These event names, a US delivery market, USD, size 40R and a $300 **per-jacket** cap are demo assumptions in a fictional client brief. The buyer can override them in the text brief before sourcing. The traveler supplied the cities, month, mix, counts and categories. Return policies apply to the buyer’s purchase market. A destination city does not set the shipping country. Keep June without a year until the buyer supplies one.

On a wide screen, **Brief** shows the itinerary, buying requirements and saved rules. **Candidates** compares three seller offers with photos when supplied, exact size, currency, item price and requirement results. **Evidence** opens the specific passage behind a selected result. The shopper sees who said it, when it was retrieved, what it applies to, and why it changed the ranking. On a phone the same sections stack with a link from each result to its evidence. Text works for the whole purchase. Use color and words together for Meets, Fails and Unknown.

## M2. The 90-second demo and its proof

| Demo time | Action | What the audience can verify |
| --- | --- | --- |
| 0–15 s | Submit the trip brief and choose the formal jacket slot. | Nine events and ten needs are visible. One category is being sourced. |
| 15–35 s | Search Shopify on demand. Open one check on the leading jacket. | Up to three distinct, seller-specific variants, availability, price and source. Call out fewer if the live catalog supplies fewer. |
| 35–50 s | The buyer says “Remember that I don’t buy final-sale items” or uses the equivalent explicit save control. | Show saving/indexing and then readiness. A second click is safe. The original brief contained no such rule. |
| 50–75 s | Start a **new conversation for the same trip**. Leave its transcript empty. | Senso supplies the saved buyer rule with a passage ID. Re-evaluate the same in-memory shortlist. Show the previous and current recommendation and the seller policy behind the change. |
| 75–90 s | Select **Continue at merchant** on the qualifying jacket. | Re-read the exact offer. Present the returned, attributed seller checkout link. The buyer can open the merchant page. The demo ends at that page. |

Rehearse two distinct outcomes. **Live** means current Shopify discovery and exact seller link, real Senso retrieval, real Jev decisions, seller-applicable evidence, and a logged language mode. A fully live ranking change additionally needs a genuine eligible alternative and a genuine policy exclusion. **Sample** proves the causal change reproducibly with our own fictional offers and policies. If live offers all have the same policy, show the honest live outcome and run the explicitly labeled sample change separately. A saved restriction with missing recall puts checkout on hold. Test the baseline with a deliberately rule-free control. A live API call retrieving a fictional document still yields fictional evidence. A qualified live handoff is a separate claim from completing a purchase.

## M3. Who does what

| Component | Responsibility | Observable output |
| --- | --- | --- |
| Shopify UCP Global Catalog | Search only for the buyer’s current task, fetch the selected variant from the selected seller, and refresh it at handoff. | Seller and variant identity, current item price/currency, availability, attributed checkout URL. [Global Catalog](https://shopify.dev/docs/agents/catalog/global-catalog) |
| Senso | Index the fictional brief and clearly marked sample policy documents. At runtime retrieve client rules and scoped seller-policy passages. Use official live policy terms transiently by default. Ingest merchant material only when permitted and explicitly selected. | Content, version and chunk references with the passage used. [Quickstart](https://docs.senso.ai/docs/quickstart) · [Search scoping](https://docs.senso.ai/docs/concepts) |
| TypeSafe Jev | Given bound evidence, ask a separate typed question for each ambiguous requirement, such as formality or returnability. | Choice, probabilities and confidence associated with the requirement and input evidence IDs. [Choice](https://docs.typesafe.ai/primitives/choice) · [Confidence](https://docs.typesafe.ai/confidence) |
| Application and general language model | Use the model for validated intent extraction with a four-second deadline. Render explanations from known checks and evidence IDs. Ordinary code calls providers, applies explicit comparisons, ranks, calculates prices, saves the authorized rule and controls checkout. | A traceable buying decision. Try the installed local Ollama with `llama3.1:8b` first. A model manifest and executable were found. Generation, speed and schema adherence remain to be tested. A labeled guided text flow covers the same actions if generation is unavailable. [Ollama structured output](https://docs.ollama.com/capabilities/structured-outputs) |
| Personal Agent Protocol, deferred | If an actual seller advertises a Poppy conversation service, let the buyer request clarification of an ambiguous policy. Shopify Ask can already answer many ordinary policy questions. | Attributed seller reply in Evidence, with speaker type and source. Cliffside Retail is a fictional protocol test target. [Shopify Ask](https://shopify.dev/docs/agents/ask) · [Poppy conversations](https://personalagentprotocol.org/docs/1.0/spec) · [Cliffside discovery](https://www.cliffside-retail.com/.well-known/poppy.json) |
| Deepgram, optional | Push to talk, release, transcribe, edit the existing text box, then submit through the same handler. | Editable draft with typed fallback. [Speech-to-text guide](https://developers.deepgram.com/docs/pre-recorded-audio) · [Recipes](https://github.com/deepgram/recipes) |

Gemini is a reviewer and optional GUI author using an already accessible chat. No part of the plan needs Google Agent Studio, a Gemini API key, ADK, a cloud deployment or a paid account upgrade. Parallel Decisions and AssemblyAI add no required work to this flow. Product scope is shopping for new items. The existing closet and ADK trial in the project is historical material.

## M4. Implementation and data ownership

Use a new `commerce/` directory at the root of the checked-out travel-stylist repository. Use Python, FastAPI, Pydantic, httpx and SQLite, plus same-origin HTML, CSS and browser JavaScript. A single local server serves the GUI and API. The repository root currently contains a prior experiment and no shared commerce application. No shared git workflow is assumed. In regular chat, Gemini returns three complete GUI files as text. Codex writes and tests them locally.

- **Durable.** SQLite holds the fictional client, trip brief, active preference IDs and save receipts, Senso document bindings and the buyer’s explicit decisions. Keep minimal selected references where needed. Keep mock product data authored by us in the sample fixture. Keep keys on the server.
- **Task-scoped.** Hold a small set of live offers and their checkout links transiently in server memory, keyed by client, trip, market and shortlist ID, with a proposed 30-minute expiry. Keep the baseline winner and the applied rule revision with that set. Keep raw offers immutable and recompute the current verdicts on fresh recall. A fresh conversation can compare against the last winner under the earlier rules even if a refresh already displayed the new winner. Retrieve preferences independently. On expiry or process restart, search again, label the new shortlist and suppress a claim that only the saved rule caused any change. Never persist live Catalog dumps or seed Senso with a supplier catalog. [Shopify Catalog usage guidelines](https://shopify.dev/docs/agents/catalog#usage-guidelines)
- **Memory integrity.** Only explicit buyer authorization creates a lasting rule. Persist a pending save with a unique client and rule binding, track the Senso content and node IDs, wait for indexing, then retrieve the scoped passage. Only a successfully retrieved live passage supports a live recall claim. An active saved rule with unavailable retrieval clears winnerId and holds handoff. A retry resumes the same operation. Until success, show the pending or unavailable state, carry the expressed restriction forward conservatively, and hold any recommendation dependent on it. Keep a second fictional client in tests to catch cross-client retrieval.
- **Evidence integrity.** Bind each document to its author, source kind, market and applicable seller/offer or explicit seller-wide policy and exceptions. Check effective date and sale conditions. A sale price alone says nothing about return rights. An ambiguous, stale, mismatched or contradictory source yields Unknown. A sample policy can never establish a fact about a live Shopify seller. The interface contract and test cases below define the precedence and the handoff rules.
- **Ownership.** Codex owns server, schemas, sample generation, provider adapters, acceptance tests and integration. The GUI author owns only `commerce/web/index.html`, `styles.css` and `app.js` within that directory. Freeze a single versioned interface and examples before these two streams separate. Codex owns all changes to that interface and sends an updated packet before a GUI author targets a new version.

## M5. Schedule, dependencies and settings

Two working streams means one local Codex session plus one reachable Gemini chat, with the operator relaying files. Parallel work is counted once in elapsed time. All numbers below are elapsed minutes after an explicit start. The review and revision happen beforehand.

| Phase | Minutes | Owner and setting | Prerequisite | Output and stop |
| --- | ---: | --- | --- | --- |
| G0 · Pressure test | Before start | Gemini Carbon with High thinking **if available in an existing chat**. Otherwise use the strongest accessible reasoning model in that chat and record its name and visible setting. | Only the self-contained review packet | Findings, exact replacement text, dependency corrections and verdict. Return them to Codex. |
| R · Revise | Before start | Codex GPT-6.2-Astra, XHigh | Full Gemini reply | Verify claims, revise every affected prompt and the plan, show decisions. **Stop for “start”.** |
| F · Prove access and freeze | 0–50 | Codex GPT-6.2-Astra, XHigh | Explicit start | Small provider probes, one sample board validated, API version fixed, a complete GUI packet. **Pause before B to select Astra High.** |
| B and U · Build in parallel | 50–155 | B is Codex GPT-6.2-Astra, High. U is Gemini in its accessible chat, Carbon High if offered. | F has issued the contracts, sample responses and file ownership | B delivers the backend and live or blocked provider receipts. U returns three browser files. Either can finish first. |
| I · Integrate | 155–230 | Codex GPT-6.2-Astra, High | B results and U files or the Codex GUI fallback | Wire through the browser, verify IDs and evidence, and run the buyer flow. **Pause before Q to select Astra XHigh.** |
| Q · Verify the core | 230–275 | Codex GPT-6.2-Astra, XHigh | Integrated application | Independent fresh-session, live and failure checks, real handoff if eligible, and a timed demo. Decide whether any optional work fits. |
| X · One optional experiment or repairs | 275–300 | Codex GPT-6.2-Astra, XHigh | Q completed and time remains before the rehearsal | Default to repairs. Only Deepgram is in scope for this slot if T01–T09 pass with no open core defects and sufficient time remains. Defer Poppy to a later milestone. |
| V · Final rehearsal | 300–330 | Codex GPT-6.2-Astra, XHigh | Latest build, including any optional change | Two rehearsals, observed claims and blockers, clean launch instructions. Stop at the merchant handoff. |

**Single-builder fallback.** If Gemini chat is unavailable for U or returns incomplete files, keep one operator and one Codex. Use 0–50 for F, 50–145 for B, 145–195 for U-local, 195–255 for I, 255–300 for Q and repairs, and 300–330 for V. Skip X. If the parallel run has started, check all three returned files at minute 135. If incomplete, end the external relay, finish B by 155, use 155–195 for U-local, 195–255 for I, 255–300 for Q and repairs, and 300–330 for V. One local builder owns these tasks sequentially. The operator relays the frozen packet and any file corrections during minutes 50–135. A phase pause can exhaust elapsed time. Cut optional scope first and report an overrun if core work can no longer fit.

**What can overlap.** After F, the GUI works on sample responses while Codex builds the provider adapters and orchestration. Read-only provider checks in F and independent test cases inside B can overlap. A preference lookup must wait for that preference to be indexed. An offer check needs the exact variant and applicable passage. Integration requires both sides. Final checkout verification needs the current winner. Every phase ends with a pause in this chat, including phases that reuse the same setting. A handoff to an external model never happens automatically.

**First three kickoff checks.** (1) Within the first 15 minutes, try one buyer-scoped Shopify search and at most three exact lookups. Record whether a native checkout URL and applicable policy exist. (2) In Senso, ingest an isolated synthetic brief and retrieve its scoped passage after indexing. Record IDs and elapsed time. (3) Submit one Jev request containing a sufficiency question and a verdict question. Independently time one local intent parse with a four-second cutoff. Missing access changes the corresponding live claim and allows the other work to proceed.

## M6. Cut decisions and release criteria

- At minute 25, record the outcome of a minimal Shopify lookup and the Senso/Jev probes, or the exact obstacle. Stop searching for a policy split at minute 25. Use only the observed cohort and available official terms. Record the honest path if the current set cannot demonstrate a live change. Continue the contract and fixture work during service delays. Release GUI authoring only after F. At minute 50 freeze even if a provider is unavailable, with a visible blocked state.
- By minute 155, prioritize one formal jacket, an explicit save and a returned seller link. Contacting a seller, mic input, more categories, visual fit analysis and hand-built carts are all below that line. By minute 230, reserve the remaining time for the full shopper path before considering voice.
- A live claim has a timestamp, provider and non-sensitive evidence reference. Run a sample case independently of the live pass. Log only minimal verdicts or references tied to this buying task. Sample proof, a provider access probe and an end-to-end live pass are three different results. If access fails, say which piece is missing and retain the useful working portion.
- Success is measured at the browser. Show the input, 9/10 brief, seller-specific comparisons, a retrievable rule after a new chat, supporting passages, an explained change when the evidence supports it and a working merchant purchase handoff. Verify mobile, keyboard operation, error states and a clean restart. Never characterize an opened checkout as a purchased item.

The attached contract provides the exact types, example offer IDs, dependency order and expected failure results. The prompt book assigns these to named phases so the reviewer can propose surgical edits.

<!-- END MASTER PLAN -->

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

<!-- BEGIN CODEX PROMPTS -->

# Codex prompt book | v0.2 revised

Run one named prompt at its gate. R is complete for this revision. F is next once the operator explicitly starts. At the end of **every phase**, even when settings stay the same, report the outcome, next phase, model and effort, then wait. A single release may start B and U together. Each prompt names its inputs and has its own completion check. Codex owns the files in the current travel-stylist repository. The plan documents are under `commerce-plan/`. Use the approved revision once R is complete. Do not paste secrets or live Catalog responses into an external chat.

## R. Revise the plan from Gemini’s critique

**Use GPT-6.2-Astra, XHigh. Paste Gemini’s entire reply after the text below or attach it to the same message.**

> You are the owner of a five-and-a-half-hour travel-commerce build. Work on the plan and prompts only. Read 01-master-plan.md, 02-contract-and-cases.md, 03-codex-prompts.md, 04-gemini-gui-prompt.md and 05-sample-response.json in commerce-plan/. The buyer asks for June travel to Delhi, Istanbul and Barcelona, nine events and ten new items. The critical path is one real jacket purchase handoff, a three-offer comparison where available, scoped Senso memory, a narrow Jev decision and a fresh-session rule-driven change where evidence supports it. The web GUI is primary. Google services are unavailable for this build. An external Gemini chat is advisory and may deliver GUI files as text.
>
> Read the reviewer’s answer as a proposal. For every finding, record accept, modify, reject or unresolved, a reason, a primary source or concrete test, the affected section/prompt and the new dependency or cut. Verify API and credit claims independently. Preserve two distinct proofs for live sourcing and our own sample flip. Identify any contradicting fixtures, false certainty, fixed rank, hidden extra builder, optional work on the critical path, or promise the operator cannot actually verify. For every accepted blocker, make the actual edit to the master plan, contract, sample data, relevant build prompts and handoff instructions. Never let a reviewer’s expansion silently displace the live handoff.
>
> Publish a coherent next revision with a short decision log and any remaining operator-only decision. Keep sections and examples synchronized. Regenerate the self-contained review and GUI packets from the revised text and sample JSON using the labeled section boundaries in their files. Validate referenced IDs, phase order, elapsed time, ownership and examples. Return the revised links, first three kickoff checks, reasons for remaining risks and the model/effort for F. Stop and wait for an explicit start before creating the application, probing accounts or running build prompts.

## F. Prove the risky dependencies and freeze the interface

**Use GPT-6.2-Astra, XHigh. Prerequisite is explicit approval to start the revised plan. Timebox 50 minutes.**

> Build the foundation in a fresh commerce/ subdirectory of the current travel-stylist repository. Use the approved commerce-plan documents. Read 07-revision-decisions.md and C3–C4 before F. The first three probes are Shopify, Senso and Jev. Use synthetic sample documents with isolated buyer bindings for Senso. Independent probes can overlap. Leave the historical ADK trial outside this application. Provide one local launch command. Register /api/* before the final root static mount. Use minimal temporary static smoke assets during F, then hand the three paths exclusively to U. Verify GET /, /styles.css, /app.js and POST /api/sessions. Create the FastAPI entry point, same-origin static mount, Pydantic wire schema, authored fixtures and a minimal callable example route that exercises the contract. Keep live Shopify data transient. Codex owns shared types. Only the external GUI author will deliver the three files in commerce/web/ during its parallel phase.
>
> Attempt the minimum evidence that could overturn the schedule in the first 25 minutes. (1) For this buyer task only, make one Shopify search through ordinary UCP Catalog access and up to three exact get_product calls. Verify effective size, seller, current price and currency units, availability, policy URL presence and an attributed checkout permalink if supplied. Record field paths, capability/profile version and status. By minute 25 stop searching for a split. Use the separate sample proof when official terms are missing. Verify exact options, native checkout eligibility and the single-action call budget in C3. Limit additional lookups to this buying task. (2) Confirm the Senso organization through the server-side key and inspect /org/credits/balance once if needed. Ingest one fictional brief or sample policy, poll the correct node and retrieve a scoped passage. (3) Send a single Jev request with the sufficiency Noul and verdict Choice and record the actual output field/model. (4) Try one local Ollama intent parse with a four-second deadline. Use deterministic explanations. Use guided input if that test fails. Record missing credentials or denied access as blocked and keep the fixture path operable. No automatic account upgrades or model downloads are part of this build.
>
> Freeze the versioned browser contract from C1–C2 in commerce/contracts/. Deliver real local schema files and sanitized application-shaped examples for new, before, indexing, fresh-after, no winner and all four handoff statuses plus ApiError. Validate the labeled wire examples in 08-wire-examples.json against the frozen schema. Start from 05-sample-response.json. Test referential integrity. Check the permanent rule is absent from the initial source and that the post-save example points at its own evidence. Define HTTP statuses and store sample data separately from live data.
>
> Create commerce/handoff/gui-packet.md for an external model with no tools. Assemble the full GUI prompt from commerce-plan/04-gemini-gui-prompt.md, replace its proposed contract and example appendix with the exact frozen contract and concise complete examples, and include the static mount, all browser-facing error/response details and a version or digest. Use invented IDs and reserved .example checkout hosts in all wire examples. Inspect for copied Catalog payloads, real seller URLs, click IDs, keys or provider IDs. Resolve any duplicated or conflicting old examples. The packet must stand alone when pasted. Emit a short capability receipt with timestamp, live/sample/blocked by provider, secret-free reference, and next test. Stop before B and tell the operator to select GPT-6.2-Astra High. Release U only after the freeze.

## B. Build the commerce workflow while Gemini builds the GUI

**Use GPT-6.2-Astra, High. Start after F. Read the frozen schema, examples, and F capability receipt.**

> Implement server logic, provider adapters and focused regression tests under commerce/. Do not edit the three files assigned to U. Deliver a functioning API through the normal routes, with independently injected sample/live providers for tests and explicit evidence origin. Begin by running the buyer flow against the authored fixtures, then substitute live providers where F proved access. Avoid compiling a standing product list. Keep requested sample and live runs explicit.
>
> Implement the buyer turn, exact trip changes, on-demand jacket sourcing, evidence view data, explicit save, fresh session and verified handoff from C1–C4. Keep the purchase category and slot counts intact. When a parsed brief provides the cities and counts but omits event names or market, show the disclosed editable demo brief defaults. Use validated constrained local-model output where available. The server resolves IDs, totals, eligibility, URL and durable actions. Text that mentions a final-sale **merchant policy** is never permission to save a **buyer preference**.
>
> For Shopify, use returned IDs, verify exact effective selections and seller, retain required attribution, and abide by the documented representations and data-use terms. Cross-check seller, currency, price and availability when the buyer proceeds to checkout. Respond with changed/unavailable on mismatch and keep the buyer in control. No payment or order call.
>
> For Senso, provision the baseline fictional brief and a few clearly labeled sample policies. Before saving, allowlist only active client docs for the given buyer and valid policy docs for the seller. Write the explicitly requested rule under a stable buyer binding. Handle 202, duplicate content, timeout and 402. Verify an actual scoped retrieval in a distinct new conversation, including source references and exact quote. Persist pending operations and reconcile retries. If binding is uncertain, hold rather than attach another client’s document. A current official merchant policy covering the market, item and markdown exceptions is needed for a live returnability verdict. Use Storefront Ask only as a pointer to official terms and only if the timebox permits it.
>
> For Jev, keep a separate question per ambiguous requirement per scoped evidence group. Store the typed result and bind it to evidence the app supplied. Make deterministic checks for size, stock, price and applicable identifiers before ranking. Exercise conflicting, negative and missing evidence. Apply the two 0.75 heuristics in C3 to the Noul and selected Choice probability, report their observed limitations, and leave insufficient evidence Unknown even when a model sounds sure. Use scoped synthetic document bodies and verified 409 reconciliation. Implement the no-rule control separately from the known-rule recall failure. On the latter set winnerId null and disable handoff. Retain the prior-rule winner with the same task-scoped set so a double refresh cannot overwrite the comparison. Re-rank with and without the saved rule and apply the exact tie-break in C3. Log fresh provider results separately from fixture behavior. Unit-test T01–T08 through real route handlers with isolated storage, including duplicate/reordered requests and service failures. Return launch command, observed results, remaining obstacles, and interface changes if any. Coordinate any proposed schema change with the GUI author before integration. Pause and report I, GPT-6.2-Astra High, even if the settings are identical.

## U fallback. Build the GUI locally if Gemini is unavailable

**Use GPT-6.2-Astra, High. Same prerequisites, files and acceptance as U. Follow the single-builder schedule.**

> Use commerce/handoff/gui-packet.md as the complete GUI assignment. Read the frozen routes and actual examples. Deliver the three browser files locally and exercise the flow through the same-origin server. Use the smallest accessible layout that supports the brief, comparison, evidence, explicit save, new conversation and handoff. Preserve all live/sample and error states. At minute 135 switch to the local route if the external handback is incomplete. Follow M5’s recovery schedule. Pause before I and report its model and effort. Stop when integration can take over and report what was actually run.

## I. Review the GUI handback, integrate and verify the local application

**Use GPT-6.2-Astra, High. Requires B and a complete U handback or local fallback.**

> Read the approved plan, frozen GUI packet, provider receipts and the complete Gemini output supplied by the operator. Review every returned browser file before writing it to commerce/web/. Confirm paths, imports and endpoint calls, verify fixtures are limited to the demo/test path, and inspect offers, prices, source URLs and state changes for invented data. If the output is cut off, ask for the named missing file only if it would save time. Otherwise finish that file locally against the frozen interface. Correct defects locally and mark which GUI pieces were used.
>
> Launch the actual server. In a real browser run the buyer journey through the rendered controls, first on sample and then with the available live services. Exercise new conversation for the same trip, an expired set, unavailable Senso, an incorrect variant, handoff in a new tab and a phone viewport. Check keyboard interaction, focus after opening evidence, readable mobile tables/cards, exact quote and link preservation, rejected stale replies and no secrets in browser requests. Ensure the after-state comes from the server even after clearing the browser transcript. Confirm the purchase link belongs to the buyer-selected seller/variant and the page can be opened without submitting payment.
>
> When a live service is blocked, report the exact affected step and the evidence on screen. A working sample proves only the sample path. Return an integration receipt with actual steps, outcomes, URLs/paths to local verification evidence as appropriate, and outstanding defects. Stop before Q and tell the operator to select GPT-6.2-Astra XHigh for the independent audit.

## Q. Challenge the live claim and rehearse the demo

**Use GPT-6.2-Astra, XHigh. Requires the integrated app from I.**

> Act as a skeptical buyer and test lead. Reproduce the 90-second flow from M2 with an empty conversation. Run the three causal tests in C4 including the unchanged-winner case, and inspect T01–T09 and the source of each displayed claim. Use a second buyer, a conflicting seller policy and a changed price to test isolation and failure handling. Verify a save survives a process restart while the old live shortlist expires; compare the original cohort only while continuity is proven. Open the attributed seller link of the exact qualifying item without paying. Test sample records against live offers and verify they cannot approve the offer. Cross-check Senso scope and actual IDs, Jev decisions, ranking arithmetic, live provider receipts and the language mode. Reject a full live-pass claim for any component evidenced only by a fixture.
>
> Fix recoverable core issues within the timebox and rerun the affected normal path. Present a table with observed live, sample verified, blocked/failed or unrun, the evidence and the demo wording for each claim. If the live policy mix yields no genuine change, rehearse the honest live result and the labeled sample flip separately. At minute 275 use X for repairs by default. Release Deepgram only if all core checks pass, the key is ready and a full 25 minutes remain. Report the next model and effort and pause. Keep the 30-minute final rehearsal intact.

## X. One optional experiment

**Use GPT-6.2-Astra, XHigh. Use the available 25-minute slot after Q. Use it for repairs by default. Deepgram is the only optional build in this release. Poppy discovery and signed conversation belong to a later milestone.**

>
> **Deepgram option.** Add a short push-to-talk recording through browser MediaRecorder. Submit the audio to a bounded same-origin server endpoint which calls Deepgram pre-recorded transcription with its server-side key. Respect browser mic permission, supported MIME type and a short duration/size limit. Return editable text to the existing composer. Only the normal Send button submits it. Test permission denial, no key, empty transcript and a buyer editing the jacket quantity before sending. No second conversation system is required. [Speech-to-text](https://developers.deepgram.com/docs/pre-recorded-audio)
>
> For the chosen work, specify the actual files, demonstrate the effect through the GUI, rerun the core sample flow, and remove incomplete controls from the demo. End at minute 300. Pause before V and report GPT-6.2-Astra, XHigh.

## V. Release rehearsal and handoff to the operator

**Use GPT-6.2-Astra, XHigh. Always reserve the final 30 minutes.**

> Start from the documented clean launch procedure. Rehearse once in sample and once in live mode where reachable. Return the command and browser URL, the opening buyer utterance, the exact save instruction, the fresh-session action, the checkout action, and the honest fallback narration if a provider or seller is unavailable. Include a concise matrix for catalog, memory, judgment, language, checkout and any optional feature with observed status and evidence. Identify any partial live result and each fact supplied by the fictional brief. Confirm no purchase was made. Report the model and effort used and that V is the final phase. Deliver the working project and stop.

<!-- END CODEX PROMPTS -->

---

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

---

<!-- BEGIN REVISION DECISIONS -->

# Revision decisions · November 20, 2026

**Ship with cuts.** The first release proves one jacket purchase handoff. In the first 25 minutes establish whether the actual task yields a qualifying native variant and official policy terms. If the observed live cohort cannot demonstrate a policy-driven change, report its actual result and show the causal change using the fictional cohort. If all live offers become Unknown, withhold the post-rule handoff. A previously verified pre-rule checkout demonstrates only that earlier state.

Gemini returned 13 findings from public documentation and desk review. Its model and effort were unavailable. Codex checked the following claims against primary materials. Provider access, latency, policy availability and the actual seller link remain Phase F observations.

| Finding and disposition | Decision and verification |
| --- | --- |
| G-01 · Modify | A stable content ID plus exact text identifies the retrieved document and passage. Map the documented `content_chunk_id` when present. Keep optional IDs nullable. A vector ID has a different meaning. Scope synthetic ingestion by opaque buyer/mode/artifact and verify same-buyer duplicate handling versus different-buyer separation in T03. [Senso quickstart](https://docs.senso.ai/docs/quickstart) |
| G-02 · Accept | Use official terms covering the item and sales conditions for a live policy verdict. An indicative Ask response can surface a lead. T04 must leave Ask-only evidence Unknown. Resolve a Storefront ID if using Ask. [UCP Ask](https://ucp.dev/specification/common/ask/) · [Shopify Ask](https://shopify.dev/docs/agents/ask) |
| G-03 · Modify | Shopify’s global and storefront extensions apply to their respective endpoints. External discovery has availability restrictions and Shopify is the default source. Limit the actions, verify the effective size, and exclude external and non-purchasable variants from the winner. T06 covers both an external result and a relaxed size. [Shopify Global Catalog](https://shopify.dev/docs/agents/catalog/global-catalog) · [External offers](https://shopify.dev/docs/agents/catalog/global-catalog-extension) |
| G-04 · Accept | C2 defines a discriminated handoff response, request shapes and errors. The URL exists only for ready. T07 verifies a stale anchor disappears and a price change needs a new action. |
| G-05 · Modify | Scope and reconcile sources before spending a Jev call. Use a Noul plus Choice and initial 0.75 routing floors. Scores cannot establish seller facts. Verify negation, conflicts, no evidence and provider failures in T05. [Jev Choice](https://docs.typesafe.ai/primitives/choice) · [Noul](https://docs.typesafe.ai/primitives/noul) · [Confidence](https://docs.typesafe.ai/confidence) |
| G-06 · Modify | An intentionally rule-free *test* should select A. A failed fetch for a known active rule should leave winnerId null. Fresh sessions must read Senso and recompute from the same cohort. A modified policy explicitly allowing the sale item should keep A first despite successful recall. T02–T03 cover all three. [Senso scoped search](https://docs.senso.ai/docs/concepts) |
| G-07 · Modify | Bind policies by origin, document version, seller, market, effective period and sale condition. A ranked subset of chunks can omit later exceptions regardless of its size. Require complete relevant terms or mark Unknown. T04 includes an excluded markdown and unknown sale status. [Shopify price and list price](https://shopify.dev/docs/agents/catalog/global-catalog) |
| G-08 · Modify | Use a four-second intent deadline, deterministic explanations, minute-25 policy cutoff and minute-135 GUI check. Use complete readable file delivery with a recovery schedule. A hard line limit cannot guarantee a complete chat response. Verify elapsed time and handback completeness at F/U. |
| G-09 · Accept | Include synthetic non-null and nullable Senso metadata, complete handoff examples and a one-unit subtotal. T07–T08 check $220 for one USD jacket, JPY formatting, a null price and mixed currencies. |
| G-10 · Modify | Defer Poppy because 25 minutes is insufficient to budget discovery, signing, conversation and GUI verification responsibly. The claimed Cliffside 0.4 mismatch conflicts with the publisher’s v1.0 listing and the v1.0 manifest observed in the previous review. Deepgram is optional only after all core checks pass. [Poppy demo directory](https://personalagentprotocol.org/docs/demos) · [Deepgram](https://developers.deepgram.com/docs/pre-recorded-audio) |
| G-11 · Accept | Identify the fictional US market, currency, 40R size, price cap and event names. Show one active slot and nine open slots for the original brief. Verify edited totals and disclosed defaults in T01/T09. |
| G-12 · Modify | Provider-free unit tests and synthetic GUI examples keep development inexpensive and shareable. Suppress Senso testing signals on automated searches. Signals suppression does not waive usage charges. Probe status and credit errors in F, record redacted results locally. [Senso concepts](https://docs.senso.ai/docs/concepts) · [Errors](https://docs.senso.ai/docs/errors) |
| G-13 · Accept | Verified all six original files. Use repository-relative paths. Register API routes before the catch-all static mount. F checks all three assets and a POST route. [Starlette route priority](https://starlette.dev/routing/) |

## Operating defaults

Use shared anonymous Shopify Catalog access unless an authorized token is already configured. Keep live merchant terms transient unless permitted ingestion is explicitly chosen. Prepare the GUI handoff for Gemini and use the single-builder schedule when necessary. These defaults allow kickoff without an account upgrade. Senso and Jev credentials affect what can be demonstrated live.

**Current gate.** Phase R is complete. Pause for the operator. Phase F uses **GPT-6.2-Astra · XHigh**. Every subsequent pause names the next phase, model and effort.

<!-- END REVISION DECISIONS -->

END OF REVIEW PACKET
