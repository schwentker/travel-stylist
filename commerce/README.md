# Travel Stylist backend

From the repository root with Python 3.12, install `commerce/requirements.txt` and launch:

```sh
python -m uvicorn commerce.app:app --host 127.0.0.1 --port 8000
```

Run a single worker. SQLite holds buyer/trip bindings, briefs, explicit rules and receipts at `commerce/runtime/state.sqlite3` (override with `COMMERCE_DB`). Shortlists and checkout URLs expire after 30 minutes and on restart. The same-origin client must retain its HTTP-only buyer cookie when opening a new conversation. The browser app is served at the root URL. For the walkthrough, see the [judge demo](../README.md#two-minute-judge-demo).

In sample mode, enter the June Delhi/Istanbul/Barcelona brief, source jackets, save “I don’t buy final-sale items”, then reopen the trip. Alder leads before the save and Birch leads after recall. Edit the month, quantities, jacket size, delivery market or currency and cap in text. For a named event use `Delhi formal event: Awards dinner`. A complete Brief JSON replaces all fields. The server displays the resulting brief for review.

Live mode searches Shopify on demand. One search considers up to 40 product groups and spends up to three lookups on seller-specific size matches. A repeat search checks the remaining candidates and then advances through Shopify’s pages. Handoff rechecks the selected variant. Seller-hosted checkout is eligible when the attributed HTTPS link comes from that variant, points to its seller’s domain or verified storefront, and names the variant and quantity one in its buy path. A known saved rule still needs fresh Senso recall and applicable merchant terms.

The web app loads the repository-root `.env` at startup. Exported environment variables take precedence. Set `SENSO_API_KEY` for live preference recall and `TYPESAFE_API_KEY` (or `JEV_API_KEY`) for live formality and returnability judgments. `SHOPIFY_CATALOG_TOKEN` is optional. Restart Uvicorn after editing `.env`. Ollama uses the loopback service with a four-second intent deadline. Guided input works without it. Senso search is scoped to a buyer/mode/artifact binding. To provision the four authored fictional reference documents into a configured Senso organization, use `python -m commerce.documents --buyer <opaque-demo-binding>`. Official live terms stay transient.

Run `python -m unittest discover -s commerce/tests -v` for T01–T08 and `python -m commerce.contracts.verify` for the API freeze. The browser contract and complete examples are in `contracts/v1/`.

### Signed seller clarification probe

With Node 22+, run `node commerce/probes/aesido-ask.mjs "$UCP_PROFILE_URL"` from the repository root. Use the public HTTPS URL for your version 2026-08-25 Ask profile with its matching public JWK in `keys`. The probe reads the private PEM from `~/.config/travel-stylist/ucp-signing.pem` or `UCP_SIGNING_KEY_PATH`.

The probe follows Aesido’s Poppy manifest, checks its UCP Ask service, verifies one available 40R storefront variant, and signs a read-only question about its return terms. A successful run prints the seller’s indicative reply with the variant ID and timestamp.

### Publish at sandboxlabs.ai/travel-stylist

With Docker running, Node 22.19+ and a Cloudflare Workers Paid account with the sandboxlabs.ai zone, run these commands from the repository root:

```sh
npx --yes wrangler@4.166.0 login
./commerce/cloudflare/deploy.sh
```

The Worker serves the frontend under `/travel-stylist/` and forwards API calls to one FastAPI container. Its private database connection uses Durable Object SQLite so trips and preference bindings survive container restarts. Live shortlists expire after 30 minutes or a backend restart. The deployment script picks up configured Senso, Jev and Shopify credentials from the shell or the root `.env` and uploads them as Worker secrets. Sample mode works without provider credentials.

The public Ask profile is a separate Hugo asset. Publish the generated public JSON as `static/travel-stylist/ucp.json` in the sandboxlabsai repository. The Worker routes leave `https://sandboxlabs.ai/travel-stylist/ucp.json` to Pages. Keep the signing PEM in your local private key directory for the signed probe.

### Host FastAPI on Render

To deploy into an existing Render project, create a **Web Service** from the Travel Stylist repo on the `main` branch. Select **Docker**, use `./commerce/Dockerfile` for Dockerfile Path and `./commerce` for Docker Build Context Directory. Set the health check path to `/` and set `COMMERCE_DB=/tmp/travel-stylist.sqlite3` in Environment. Render builds the image from GitHub. The root `render.yaml` provides the same settings when creating a Blueprint.

For Live mode, set `SENSO_API_KEY` and `TYPESAFE_API_KEY` in the Render service’s Environment. `SHOPIFY_CATALOG_TOKEN` is optional. The Free plan can sleep and uses ephemeral disk, so trip and preference bindings can be lost on a restart, spin-down, or redeploy. For durable storage, use a paid service with a persistent disk, for example at `/var/data`, and set `COMMERCE_DB=/var/data/travel-stylist.sqlite3`. Keep the service at one instance.

For the public short URL, set the Sandbox Labs Cloudflare Pages project's `TRAVEL_STYLIST_ORIGIN` variable to the Render service's HTTPS origin if it differs from `https://travel-stylist.onrender.com`. The Pages function forwards the app and API under `/travel-stylist/`. Hugo can serve the optional public UCP profile alongside it.
