# Travel commerce demo | Master plan v0.1

**Status — proposed for critique, November 20, 2026.** The next action is to give Gemini the single file `00-gemini-pressure-test.md` in an existing chat you can already use. Return its whole critique to Codex. Codex revises the plan and the prompts, reports what changed, and waits for your explicit start. The 330-minute build clock begins at that start.

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

Rehearse two distinct outcomes. **Live** means current Shopify discovery and exact seller link, real Senso retrieval, real Jev decisions, seller-applicable evidence, and a logged language mode. A fully live ranking change additionally needs a genuine eligible alternative and a genuine policy exclusion. **Sample** proves the causal change reproducibly with our own fictional offers and policies. If live offers all have the same policy, show the honest live outcome and run the explicitly labeled sample change separately. A live API call retrieving a fictional document still yields fictional evidence. A qualified live handoff is a separate claim from completing a purchase.

## M3. Who does what

| Component | Responsibility | Observable output |
| --- | --- | --- |
| Shopify UCP Global Catalog | Search only for the buyer’s current task, fetch the selected variant from the selected seller, and refresh it at handoff. | Seller and variant identity, current item price/currency, availability, attributed checkout URL. [Global Catalog](https://shopify.dev/docs/agents/catalog/global-catalog) |
| Senso | Index the fictional brief and clearly marked sample policy documents. At runtime retrieve client rules and scoped seller-policy passages. Use permissioned, attributable, applicable material for a live seller. | Content, version and chunk references with the passage used. [Quickstart](https://docs.senso.ai/docs/quickstart) · [Search scoping](https://docs.senso.ai/docs/concepts) |
| TypeSafe Jev | Given bound evidence, ask a separate typed question for each ambiguous requirement, such as formality or returnability. | Choice, probabilities and confidence associated with the requirement and input evidence IDs. [Choice](https://docs.typesafe.ai/primitives/choice) · [Confidence](https://docs.typesafe.ai/confidence) |
| Application and general language model | The model interprets a buyer message into a validated intent and can explain a decision using its supplied evidence. Ordinary code calls providers, applies explicit comparisons, ranks, calculates prices, saves the authorized rule and controls checkout. | A traceable buying decision. Try the installed local Ollama with `llama3.1:8b` first. A model manifest and executable were found. Generation, speed and schema adherence remain to be tested. A labeled guided text flow covers the same actions if generation is unavailable. [Ollama structured output](https://docs.ollama.com/capabilities/structured-outputs) |
| Personal Agent Protocol, optional | If an actual seller advertises a Poppy conversation service, let the buyer request clarification of an ambiguous policy. Shopify Ask can already answer many ordinary policy questions. | Attributed seller reply in Evidence, with speaker type and source. Cliffside Retail is a fictional protocol test target. [Shopify Ask](https://shopify.dev/docs/agents/ask) · [Poppy conversations](https://personalagentprotocol.org/docs/1.0/spec) · [Cliffside discovery](https://www.cliffside-retail.com/.well-known/poppy.json) |
| Deepgram, optional | Push to talk, release, transcribe, edit the existing text box, then submit through the same handler. | Editable draft with typed fallback. [Speech-to-text guide](https://developers.deepgram.com/docs/pre-recorded-audio) · [Recipes](https://github.com/deepgram/recipes) |

Gemini is a reviewer and optional GUI author using an already accessible chat. No part of the plan needs Google Agent Studio, a Gemini API key, ADK, a cloud deployment or a paid account upgrade. Parallel Decisions and AssemblyAI add no required work to this flow. Product scope is shopping for new items. The existing closet and ADK trial in the project is historical material.

## M4. Implementation and data ownership

Use a new `commerce/` directory under `/Users/andres/dev/travel-stylist`. Use Python, FastAPI, Pydantic, httpx and SQLite, plus same-origin HTML, CSS and browser JavaScript. A single local server serves the GUI and API. The repository root currently contains a prior experiment and no shared commerce application. No shared git workflow is assumed. In regular chat, Gemini returns three complete GUI files as text. Codex writes and tests them locally.

- **Durable.** SQLite holds the fictional client, trip brief, active preference IDs and save receipts, Senso document bindings and the buyer’s explicit decisions. Keep minimal selected references where needed. Keep mock product data authored by us in the sample fixture. Keep keys on the server.
- **Task-scoped.** Hold a small set of live offers and their checkout links transiently in server memory, keyed by client, trip, market and shortlist ID, with a proposed 30-minute expiry. Keep the baseline winner and the applied rule revision with that set. A fresh conversation can compare against the last winner under the earlier rules even if a refresh already displayed the new winner. Retrieve preferences independently. On expiry or process restart, search again, label the new shortlist and suppress a claim that only the saved rule caused any change. Never persist live Catalog dumps or seed Senso with a supplier catalog. [Shopify Catalog usage guidelines](https://shopify.dev/docs/agents/catalog#usage-guidelines)
- **Memory integrity.** Only explicit buyer authorization creates a lasting rule. Persist a pending save with a unique client and rule binding, track the Senso content and node IDs, wait for indexing, then retrieve the scoped passage. Only then mark it recalled. A retry resumes the same operation. Until success, show the pending or unavailable state, carry the expressed restriction forward conservatively, and hold any recommendation dependent on it. Keep a second fictional client in tests to catch cross-client retrieval.
- **Evidence integrity.** Bind each document to its author, source kind, market and applicable seller/offer or explicit seller-wide policy and exceptions. Check effective date and sale conditions. A sale price alone says nothing about return rights. An ambiguous, stale, mismatched or contradictory source yields Unknown. A sample policy can never establish a fact about a live Shopify seller. The interface contract and test cases below define the precedence and the handoff rules.
- **Ownership.** Codex owns server, schemas, sample generation, provider adapters, acceptance tests and integration. The GUI author owns only `commerce/web/index.html`, `styles.css` and `app.js` within that directory. Freeze a single versioned interface and examples before these two streams separate. Codex owns all changes to that interface and sends an updated packet before a GUI author targets a new version.

## M5. Schedule, dependencies and settings

Two working streams means one local Codex session plus one reachable Gemini chat, with the operator relaying files. Parallel work is counted once in elapsed time. All numbers below are elapsed minutes after an explicit start. The review and revision happen beforehand.

| Phase | Minutes | Owner and setting | Prerequisite | Output and stop |
| --- | ---: | --- | --- | --- |
| G0 · Pressure test | Before start | Gemini Carbon with High thinking **if available in an existing chat**. Otherwise use the strongest accessible reasoning model in that chat and record its name and visible setting. | Only the self-contained review packet | Findings, exact replacement text, dependency corrections and verdict. Return them to Codex. |
| R · Revise | Before start | Codex GPT-6.2-Astra, XHigh | Full Gemini reply | Verify claims, revise every affected prompt and the plan, show decisions. **Stop for “start”.** |
| F · Prove access and freeze | 0–50 | Codex GPT-6.2-Astra, XHigh | Explicit start | Small provider probes, one sample board validated, API version fixed, a complete GUI packet. **Pause before B to select Astra High.** |
| B and U · Build in parallel | 50–160 | B is Codex GPT-6.2-Astra, High. U is Gemini in its accessible chat, Carbon High if offered. | F has issued the contracts, sample responses and file ownership | B delivers the backend and live or blocked provider receipts. U returns three browser files. Either can finish first. |
| I · Integrate | 160–235 | Codex GPT-6.2-Astra, High | B results and U files or the Codex GUI fallback | Wire through the browser, verify IDs and evidence, and run the buyer flow. **Pause before Q to select Astra XHigh.** |
| Q · Verify the core | 235–275 | Codex GPT-6.2-Astra, XHigh | Integrated application | Independent fresh-session, live and failure checks, real handoff if eligible, and a timed demo. Decide whether any optional work fits. |
| X · One optional experiment or repairs | 275–300 | Codex GPT-6.2-Astra, XHigh | Core passed and at least 25 minutes remain before the final buffer | Choose at most one. Prefer Poppy if it adds a seller conversation, otherwise Deepgram if ready. Use the time for core repairs when needed. |
| V · Final rehearsal | 300–330 | Codex GPT-6.2-Astra, XHigh | Latest build, including any optional change | Two rehearsals, observed claims and blockers, clean launch instructions. Stop at the merchant handoff. |

**Single-builder fallback.** If Gemini chat is unavailable for U or returns incomplete files, keep one operator and one Codex. Use 0–50 for F, 50–145 for B, 145–200 for the smaller GUI using prompt U, 200–265 for I, 265–300 for Q, and 300–330 for rehearsal and fixes. Drop both extensions. At minute 145 switch to the local GUI if U is blocked or unlikely to deliver by minute 160. If a handback fails at minute 160, spend 160–205 on the local GUI and 205–265 on integration. If Gemini delivers during recovery, reuse only files that reduce the remaining work.

**What can overlap.** After F, the GUI works on sample responses while Codex builds the provider adapters and orchestration. Read-only provider checks in F and independent test cases inside B can overlap. A preference lookup must wait for that preference to be indexed. An offer check needs the exact variant and applicable passage. Integration requires both sides. Final checkout verification needs the current winner. A model setting change is an explicit stop in this chat. A handoff to an external model never happens automatically.

## M6. Cut decisions and release criteria

- At minute 25, record the outcome of a minimal Shopify lookup and the Senso/Jev probes, or the exact obstacle. Before minute 50, check whether any selected offer has applicable official return terms. Record the honest path if the current set cannot demonstrate a live change. Continue the independent GUI and fixture work during service delays. At minute 50 freeze even if a provider is unavailable, with a visible blocked state.
- By minute 160, prioritize one formal jacket, an explicit save and a returned seller link. Contacting a seller, mic input, more categories, visual fit analysis and hand-built carts are all below that line. By minute 235, reserve the remaining time for the full shopper path before considering either extension.
- A live claim has a timestamp, provider and non-sensitive evidence reference. Run a sample case independently of the live pass. Log only minimal verdicts or references tied to this buying task. Sample proof, a provider access probe and an end-to-end live pass are three different results. If access fails, say which piece is missing and retain the useful working portion.
- Success is measured at the browser. Show the input, 9/10 brief, seller-specific comparisons, a retrievable rule after a new chat, supporting passages, an explained change when the evidence supports it and a working merchant purchase handoff. Verify mobile, keyboard operation, error states and a clean restart. Never characterize an opened checkout as a purchased item.

The attached contract provides the exact types, example offer IDs, dependency order and expected failure results. The prompt book assigns these to named phases so the reviewer can propose surgical edits.
