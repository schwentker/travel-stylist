# Travel Stylist

Travel Stylist is a planned commerce assistant for buying clothes around a trip. The demo starts with nine June events across Delhi, Istanbul and Barcelona and a brief for ten new items. It takes one formal jacket from discovery through a seller-specific comparison and merchant checkout handoff.

## Project status

The current deliverables are the plan, prompts, interface contract and fictional sample response. The commerce application and its live integrations are planned. The shopper completes payment on the merchant site.

## What the demo shows

1. Enter the trip and see the event schedule and ten purchase slots.
2. Compare up to three jackets using the exact seller, size, availability and price.
3. Save “I don’t buy final-sale items.”
4. Open a fresh conversation for the same trip. Retrieve the rule, check the same shortlist and explain any change using the seller’s evidence.
5. Refresh the selected variant and open the attributed checkout link returned by Shopify.

In the sample, Alder leads at $180 before the rule. Its final-sale policy then disqualifies it, Birch leads at $220, and Cedar stays Unknown. A live run requires evidence about the actual sellers and can produce a different outcome. The interface labels fictional evidence even when a live service processes it.

## Planned architecture

| Component | Responsibility |
| --- | --- |
| Browser | Brief, Candidates and Evidence panels, with text input and explicit save and handoff controls |
| FastAPI | Same-origin HTML, CSS and JavaScript, validated request handling, ranking and checkout revalidation |
| SQLite | Trip, buyer preferences, save receipts and source bindings |
| Shopify UCP Global Catalog | On-demand discovery and exact variant lookup. Current offers stay in short-lived task memory. |
| Senso | Scoped retrieval of buyer rules and applicable policy passages |
| TypeSafe Jev | Typed interpretation of ambiguous requirements from supplied passages |
| Local language model | Optional natural-language intent and explanation, with guided input when unavailable |
| Poppy or Deepgram | Optional seller clarification or push-to-talk after the core is working |

## Planning files

- [Master plan](commerce-plan/01-master-plan.md) covers scope, ownership and the parallel and serial schedules.
- [Review packet](commerce-plan/00-gemini-pressure-test.md) is the standalone assignment for the first Gemini chat.
- [Interface and acceptance cases](commerce-plan/02-contract-and-cases.md) defines routes, payloads and expected failures.
- [Codex prompts](commerce-plan/03-codex-prompts.md) cover revision, foundation, build, integration and rehearsal.
- [Gemini GUI assignment](commerce-plan/04-gemini-gui-prompt.md) describes its three browser files. Use the frozen handoff after the contract is approved.
- [Sample response](commerce-plan/05-sample-response.json) illustrates the result after the final-sale rule is applied.

## Review before kickoff

Send the review packet to Gemini and bring back the full critique. Codex checks the findings against primary sources, revises the plan and prompts, and pauses for the start signal. Freeze the interface and sample responses first. Backend and GUI work can then overlap. Both must be available for browser integration and checkout verification.

## Acceptance

A live claim needs an observed provider result. Verify a fresh conversation, an explicitly saved rule, traceable evidence, exact variant selection and a working merchant link. Check conflicting or missing policy, duplicate saves, changed prices and blocked providers. Keep sample outcomes distinct from live results.

## Publish the planning repository

Use a private repository initially. This sequence assumes the project directory has no Git metadata and GitHub CLI is installed. It stages only this README and the reviewed planning files.

~~~sh
cd /Users/andres/dev/travel-stylist
gh auth status
# If needed, run gh auth login before continuing.
git init -b main
git add README.md commerce-plan/
git diff --cached --stat
git diff --cached
git commit -m "Add travel commerce plan and build prompts"
gh repo create travel-stylist --private --source=. --remote=origin --push
~~~

Configure a Codex Cloud environment against the repository after the push if you want future work to run independently of this laptop. Keep provider credentials out of Git and attach the complete Gemini critique to the revision task when available.
