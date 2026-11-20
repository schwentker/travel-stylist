# Travel Stylist backend

From the repository root with Python 3.12, install `commerce/requirements.txt` and launch:

```sh
python -m uvicorn commerce.app:app --host 127.0.0.1 --port 8000
```

Run a single worker. SQLite holds buyer/trip bindings, briefs, explicit rules and receipts at `commerce/runtime/state.sqlite3` (override with `COMMERCE_DB`). Shortlists and checkout URLs expire after 30 minutes and on restart. The same-origin client must retain its HTTP-only buyer cookie when opening a new conversation. The browser app is served at the root URL. For the walkthrough, see the [judge demo](../README.md#two-minute-judge-demo).

In sample mode, enter the June Delhi/Istanbul/Barcelona brief, source jackets, save “I don’t buy final-sale items”, then reopen the trip. Alder leads before the save and Birch leads after recall. Edit the month, quantities, jacket size, delivery market or currency and cap in text. For a named event use `Delhi formal event: Awards dinner`. A complete Brief JSON replaces all fields. The server displays the resulting brief for review.

Live mode searches Shopify on demand. Optional server settings are `SHOPIFY_CATALOG_TOKEN`, `SENSO_API_KEY` and `TYPESAFE_API_KEY` (or `JEV_API_KEY`). Ollama uses the loopback service with a four-second intent deadline. Guided input works without it. Senso search is scoped to a buyer/mode/artifact binding. To provision the four authored fictional reference documents into a configured Senso organization, use `python -m commerce.documents --buyer <opaque-demo-binding>`. Official live terms stay transient.

Run `python -m unittest discover -s commerce/tests -v` for T01–T08 and `python -m commerce.contracts.verify` for the API freeze. The browser contract and complete examples are in `contracts/v1/`. The Gemini assignment and phase receipts are in `handoff/`.
