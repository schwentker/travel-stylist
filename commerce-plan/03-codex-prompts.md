# Codex prompt book | v0.1 candidate

Run one named prompt at its gate. **R is the only Codex prompt to use after Gemini returns its critique and before the operator says start.** Everything after R describes future work. Each prompt names its inputs and has its own completion check. Codex owns the files in `/Users/andres/dev/travel-stylist`. The plan documents are under `commerce-plan/`. Use the approved revision once R is complete. Do not paste secrets or live Catalog responses into an external chat.

## R. Revise the plan from Gemini’s critique

**Use GPT-6.2-Astra, XHigh. Paste Gemini’s entire reply after the text below or attach it to the same message.**

> You are the owner of a five-and-a-half-hour travel-commerce build. Work on the plan and prompts only. Read 01-master-plan.md, 02-contract-and-cases.md, 03-codex-prompts.md, 04-gemini-gui-prompt.md and 05-sample-response.json in commerce-plan/. The buyer asks for June travel to Delhi, Istanbul and Barcelona, nine events and ten new items. The critical path is one real jacket purchase handoff, a three-offer comparison where available, scoped Senso memory, a narrow Jev decision and a fresh-session rule-driven change where evidence supports it. The web GUI is primary. Google services are unavailable for this build. An external Gemini chat is advisory and may deliver GUI files as text.
>
> Read the reviewer’s answer as a proposal. For every finding, record accept, modify, reject or unresolved, a reason, a primary source or concrete test, the affected section/prompt and the new dependency or cut. Verify API and credit claims independently. Preserve two distinct proofs for live sourcing and our own sample flip. Identify any contradicting fixtures, false certainty, fixed rank, hidden extra builder, optional work on the critical path, or promise the operator cannot actually verify. For every accepted blocker, make the actual edit to the master plan, contract, sample data, relevant build prompts and handoff instructions. Never let a reviewer’s expansion silently displace the live handoff.
>
> Publish a coherent next revision with a short decision log and any remaining operator-only decision. Keep sections and examples synchronized. Regenerate the self-contained review and GUI packets from the revised text and sample JSON using the labeled section boundaries in their files. Validate referenced IDs, phase order, elapsed time, ownership and examples. Return the revised links, first three kickoff checks, reasons for remaining risks and the model/effort for F. Stop and wait for an explicit start before creating the application, probing accounts or running build prompts.

## F. Prove the risky dependencies and freeze the interface

**Use GPT-6.2-Astra, XHigh. Prerequisite is explicit approval to start the revised plan. Timebox 50 minutes.**

> Build the foundation in a fresh commerce/ subdirectory of /Users/andres/dev/travel-stylist. Use the approved commerce-plan documents. Leave the historical ADK trial outside this application. Provide one local launch command. Create the FastAPI entry point, same-origin static mount, Pydantic wire schema, authored fixtures and a minimal callable example route that exercises the contract. Keep live Shopify data transient. Codex owns shared types. Only the external GUI author will deliver the three files in commerce/web/ during its parallel phase.
>
> Attempt the minimum evidence that could overturn the schedule in the first 25 minutes. (1) For this buyer task only, make one Shopify search through ordinary UCP Catalog access and one exact get_product call. Verify effective size, seller, current price and currency units, availability, policy URL presence and an attributed checkout permalink if supplied. Record field paths, capability/profile version and status. Before the freeze, verify one applicable current seller policy if available and whether the cohort has evidence for a genuine flip. Limit additional lookups to this buying task. (2) Confirm the Senso organization through the server-side key. Ingest one fictional brief or sample policy, poll the correct node and retrieve a scoped passage. (3) Send one narrow Jev Choice and record the actual output field/model. (4) Try the installed local Ollama model on one short schema-bound intent, observe latency and validation. Use guided input if that test fails. Record missing credentials or denied access as blocked and keep the fixture path operable. No automatic account upgrades or model downloads are part of this build.
>
> Freeze the versioned browser contract from C1–C2 in commerce/contracts/. Deliver real local schema files and sanitized application-shaped examples for new, before, indexing, fresh-after, no winner and changed handoff. Start from 05-sample-response.json. Test referential integrity. Check the permanent rule is absent from the initial source and that the post-save example points at its own evidence. Define HTTP statuses and store sample data separately from live data.
>
> Create commerce/handoff/gui-packet.md for an external model with no tools. Assemble the full GUI prompt from commerce-plan/04-gemini-gui-prompt.md, replace its proposed contract and example appendix with the exact frozen contract and concise complete examples, and include the static mount, all browser-facing error/response details and a version or digest. Resolve any duplicated or conflicting old examples. The packet must stand alone when pasted. Emit a short capability receipt with timestamp, live/sample/blocked by provider, secret-free reference, and next test. Stop before B and tell the operator to select GPT-6.2-Astra High. Release U only after the freeze.

## B. Build the commerce workflow while Gemini builds the GUI

**Use GPT-6.2-Astra, High. Start after F. Read the frozen schema, examples, and F capability receipt.**

> Implement server logic, provider adapters and focused regression tests under commerce/. Do not edit the three files assigned to U. Deliver a functioning API through the normal routes, with independently injected sample/live providers for tests and explicit evidence origin. Begin by running the buyer flow against the authored fixtures, then substitute live providers where F proved access. Avoid compiling a standing product list. Keep requested sample and live runs explicit.
>
> Implement the buyer turn, exact trip changes, on-demand jacket sourcing, evidence view data, explicit save, fresh session and verified handoff from C1–C4. Keep the purchase category and slot counts intact. When a parsed brief provides the cities and counts but omits event names or market, show the disclosed editable demo brief defaults. Use validated constrained local-model output where available. The server resolves IDs, totals, eligibility, URL and durable actions. Text that mentions a final-sale **merchant policy** is never permission to save a **buyer preference**.
>
> For Shopify, use returned IDs, verify exact effective selections and seller, retain required attribution, and abide by the documented representations and data-use terms. Cross-check seller, currency, price and availability when the buyer proceeds to checkout. Respond with changed/unavailable on mismatch and keep the buyer in control. No payment or order call.
>
> For Senso, provision the baseline fictional brief and a few clearly labeled sample policies. Before saving, allowlist only active client docs for the given buyer and valid policy docs for the seller. Write the explicitly requested rule under a stable buyer binding. Handle 202, duplicate content, timeout and 402. Verify an actual scoped retrieval in a distinct new conversation, including source references and exact quote. Persist pending operations and reconcile retries. If binding is uncertain, hold rather than attach another client’s document. A current official merchant policy, or an attributable response from that seller scoped to the selected item, is needed for a live returnability verdict. Try Storefront Ask only if it resolves the actual missing facts within the timebox.
>
> For Jev, keep a separate question per ambiguous requirement per scoped evidence group. Store the typed result and bind it to evidence the app supplied. Make deterministic checks for size, stock, price and applicable identifiers before ranking. Exercise conflicting, negative and missing evidence. Pick a conservative review threshold on the labeled cases, record it with examples, and leave insufficient evidence Unknown even when a model sounds sure. Retain the prior-rule winner with the same task-scoped set so a double refresh cannot overwrite the comparison. Re-rank with and without the saved rule and apply the exact tie-break in C3. Log fresh provider results separately from fixture behavior. Unit-test T01–T08 through real route handlers with isolated storage, including duplicate/reordered requests and service failures. Return launch command, observed results, remaining obstacles, and interface changes if any. Coordinate any proposed schema change with the GUI author before integration.

## U fallback. Build the GUI locally if Gemini is unavailable

**Use GPT-6.2-Astra, High. Same prerequisites, files and acceptance as U. Follow the single-builder schedule.**

> Use commerce/handoff/gui-packet.md as the complete GUI assignment. Read the frozen routes and actual examples. Deliver the three browser files locally and exercise the flow through the same-origin server. Use the smallest accessible layout that supports the brief, comparison, evidence, explicit save, new conversation and handoff. Preserve all live/sample and error states. Stop when I can take over and report what was actually run.

## I. Review the GUI handback, integrate and verify the local application

**Use GPT-6.2-Astra, High. Requires B and a complete U handback or local fallback.**

> Read the approved plan, frozen GUI packet, provider receipts and the complete Gemini output supplied by the operator. Review every returned browser file before writing it to commerce/web/. Confirm paths, imports and endpoint calls, verify fixtures are limited to the demo/test path, and inspect offers, prices, source URLs and state changes for invented data. If the output is cut off, ask for the named missing file only if it would save time. Otherwise finish that file locally against the frozen interface. Correct defects locally and mark which GUI pieces were used.
>
> Launch the actual server. In a real browser run the buyer journey through the rendered controls, first on sample and then with the available live services. Exercise new conversation for the same trip, an expired set, unavailable Senso, an incorrect variant, handoff in a new tab and a phone viewport. Check keyboard interaction, focus after opening evidence, readable mobile tables/cards, exact quote and link preservation, rejected stale replies and no secrets in browser requests. Ensure the after-state comes from the server even after clearing the browser transcript. Confirm the purchase link belongs to the buyer-selected seller/variant and the page can be opened without submitting payment.
>
> When a live service is blocked, report the exact affected step and the evidence on screen. A working sample proves only the sample path. Return an integration receipt with actual steps, outcomes, URLs/paths to local verification evidence as appropriate, and outstanding defects. Stop before Q and tell the operator to select GPT-6.2-Astra XHigh for the independent audit.

## Q. Challenge the live claim and rehearse the demo

**Use GPT-6.2-Astra, XHigh. Requires the integrated app from I.**

> Act as a skeptical buyer and test lead. Reproduce the 90-second flow from M2 with an empty conversation. Check T01–T09 and the source of each displayed claim. Use a second buyer, a conflicting seller policy and a changed price to test isolation and failure handling. Verify a save survives a process restart while the old live shortlist expires; compare the original cohort only while continuity is proven. Open the attributed seller link of the exact qualifying item without paying. Test sample records against live offers and verify they cannot approve the offer. Cross-check Senso scope and actual IDs, Jev decisions, ranking arithmetic, live provider receipts and the language mode. Reject a full live-pass claim for any component evidenced only by a fixture. 
>
> Fix recoverable core issues within the timebox and rerun the affected normal path. Present a table with observed live, sample verified, blocked/failed or unrun, the evidence and the demo wording for each claim. If the live policy mix yields no genuine change, rehearse the honest live result and the labeled sample flip separately. Decide whether a 25-minute optional slot is genuinely free. Return one choice for X or reserve it for repairs. Keep the 30-minute final rehearsal intact.

## X. One optional experiment

**Use GPT-6.2-Astra, XHigh. Requires a passing core and a free 25-minute slot. Run one option only.**

> **Poppy option.** Implement a buyer-initiated seller clarification in the already working Evidence panel only when there is a usable counterparty and this adds to the normal policy lookup. Read the Personal Agent Protocol 1.0 discovery, signed-out Session and conversation requirements. Verify the merchant’s HTTPS /.well-known/poppy.json, organization domain and advertised Poppy conversation capability. Use a conforming client or maintained signing components for a per-request Poppy-Session. Send only the variant, sale context and policy question. Use fictional Cliffside for a labeled interoperability test. An actual message to a real seller needs buyer authorization. Attribute any reply to the responding seller and speaker, ask for the policy basis, keep unresolved facts Unknown, and make human handoff optional. A discovered manifest alone proves discovery only. Keep a Cliffside reply out of the live Shopify candidate matrix. If no compliant exchange fits the window, leave the feature out and report the tested subset. [Spec](https://personalagentprotocol.org/docs/1.0/spec) · [UCP extension](https://personalagentprotocol.org/docs/1.0/extensions/ucp) · [Demo directory](https://personalagentprotocol.org/docs/demos)
>
> **Deepgram option.** Add a short push-to-talk recording through browser MediaRecorder. Submit the audio to a bounded same-origin server endpoint which calls Deepgram pre-recorded transcription with its server-side key. Respect browser mic permission, supported MIME type and a short duration/size limit. Return editable text to the existing composer. Only the normal Send button submits it. Test permission denial, no key, empty transcript and a buyer editing the jacket quantity before sending. No second conversation system is required. [Speech-to-text](https://developers.deepgram.com/docs/pre-recorded-audio)
>
> For the chosen option, specify the actual files, demonstrate the effect through the GUI, rerun the core sample flow, and remove incomplete controls from the demo. End at minute 300.

## V. Release rehearsal and handoff to the operator

**Use GPT-6.2-Astra, XHigh. Always reserve the final 30 minutes.**

> Start from the documented clean launch procedure. Rehearse once in sample and once in live mode where reachable. Return the command and browser URL, the opening buyer utterance, the exact save instruction, the fresh-session action, the checkout action, and the honest fallback narration if a provider or seller is unavailable. Include a concise matrix for catalog, memory, judgment, language, checkout and any optional feature with observed status and evidence. Identify any partial live result and each fact supplied by the fictional brief. Confirm no purchase was made. Deliver the working project and stop.
