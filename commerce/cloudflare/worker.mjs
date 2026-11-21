import { DurableObject } from "cloudflare:workers";

const prefix = "/travel-stylist";
const databaseHost = "travel-storage.invalid";
const secretNames = ["SENSO_API_KEY", "TYPESAFE_API_KEY", "JEV_API_KEY", "SHOPIFY_CATALOG_TOKEN"];

export class TripDatabase extends DurableObject {
  async fetch(request) {
    if (request.method !== "POST" || new URL(request.url).hostname !== databaseHost) {
      return new Response(null, { status: 404 });
    }
    const { query, params } = await request.json();
    const sql = this.ctx.storage.sql;
    const rows = sql.exec(query, ...params).toArray();
    // The workflow uses rowcount to detect a newly saved preference.
    const changes = sql.exec("SELECT changes() AS count").one().count;
    return Response.json({ rows, changes });
  }
}

export class Stylist extends DurableObject {
  async ready() {
    const container = this.ctx.container;
    const database = this.env.DATABASE.getByName("trips");
    await container.interceptOutboundHttp(databaseHost, database);
    if (!container.running) {
      const env = { COMMERCE_STORAGE: "cloudflare" };
      for (const name of secretNames) {
        if (this.env[name]) env[name] = this.env[name];
      }
      container.start({ image: container.images.base, instance: "lite", enableInternet: true, env });
    }
    await container.setInactivityTimeout(30 * 60 * 1000);
    const port = container.getTcpPort(8000);
    for (let attempt = 0; attempt < 100; attempt++) {
      try {
        const check = await port.fetch("http://container/", { method: "HEAD", signal: AbortSignal.timeout(1000) });
        if (check.ok) return port;
      } catch {
        // Readiness checks can race Uvicorn startup.
      }
      await scheduler.wait(200);
    }
    throw new Error("Travel Stylist did not start");
  }

  async fetch(request) {
    // Readiness probes may be retried. Send the buyer action just once.
    this.starting ??= this.ready().finally(() => { this.starting = undefined; });
    const port = await this.starting;
    return port.fetch(request);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === prefix) {
      url.pathname += "/";
      return Response.redirect(url, 308);
    }
    if (!url.pathname.startsWith(prefix + "/")) return new Response(null, { status: 404 });
    const path = url.pathname.slice(prefix.length);
    if (!path.startsWith("/api/")) {
      url.pathname = path;
      return env.ASSETS.fetch(new Request(url, request));
    }
    const headers = new Headers({ "content-type": request.headers.get("content-type") || "application/json" });
    const buyer = request.headers.get("cookie")?.match(/(?:^|;\s*)(commerce_buyer=[A-Fa-f0-9-]{36})(?:;|$)/);
    if (buyer) headers.set("cookie", buyer[1]);
    const upstream = new Request("http://container" + path + url.search, {
      method: request.method, headers, body: request.body,
    });
    const response = await env.STYLIST.getByName("demo").fetch(upstream);
    const result = new Response(response.body, response);
    result.headers.set("cache-control", "no-store");
    const cookie = result.headers.get("set-cookie");
    if (cookie) result.headers.set("set-cookie", cookie.replace(/Path=\/(?=;|$)/i, "Path=" + prefix + "/") + "; Secure");
    return result;
  },
};
