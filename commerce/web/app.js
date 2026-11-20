const get = id => document.getElementById(id);
const draft = get("draft");
const mode = get("mode");
const sampleBrief = "I'm going to Delhi, Istanbul and Barcelona in June. Three events per city. Two new jackets, two pairs of trousers, two pairs of shoes, two shirts and two hats.";
const rule = "I don’t buy final-sale items.";
const verdictLabel = { meets: "Meets", fails: "Fails", unknown: "Unknown" };
const originLabel = { buyer: "Buyer", merchant: "Merchant", shopify_live: "Live Shopify", sample: "Sample fixture" };
const serviceLabel = { catalog: "Catalog", senso: "Senso", jev: "Jev", language: "Language" };

let view = null;
let selection = null;
let busy = false;
let generation = 0;
let stale = false;

function element(tag, content, className) {
  const node = document.createElement(tag);
  if (content !== undefined) node.textContent = content;
  if (className) node.className = className;
  return node;
}

function facts(entries) {
  const list = element("dl", undefined, "facts");
  for (const [label, value] of entries) {
    if (value === null || value === undefined) continue;
    const row = element("div");
    row.append(element("dt", label), element("dd", value));
    list.append(row);
  }
  return list;
}

function list(items, className) {
  const node = element("ul", undefined, className);
  node.append(...items.map(item => element("li", item)));
  return node;
}

function money(minor, currency) {
  if (minor === null || !currency) return "Price unavailable";
  try {
    const format = new Intl.NumberFormat(undefined, { style: "currency", currency, currencyDisplay: "code" });
    return format.format(minor / 10 ** format.resolvedOptions().maximumFractionDigits);
  } catch {
    return minor + " minor units · " + currency;
  }
}

function https(value) {
  if (typeof value !== "string" || !/^https:\/\/[^\s\\]+$/i.test(value)) return false;
  try {
    const url = new URL(value);
    return url.protocol === "https:" && !!url.hostname && !url.username && !url.password;
  } catch {
    return false;
  }
}

function externalLink(label, url) {
  const link = element("a", label);
  link.setAttribute("href", url);
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  return link;
}

function badge(label, verdict) {
  const node = element("span", label, "badge");
  if (verdict) node.dataset.verdict = verdict;
  return node;
}

function showNote(text) {
  const note = get("checkout-note");
  note.textContent = text;
  note.hidden = !text;
}

function clearCheckout() {
  get("merchant").replaceChildren();
  showNote("");
}

function notice(text = "", retry = null) {
  const node = get("notice");
  node.hidden = !text;
  node.replaceChildren();
  if (text) node.append(element("p", text));
  if (retry) {
    const button = element("button", "Retry");
    button.type = "button";
    button.addEventListener("click", retry);
    node.append(button);
  }
}

function updateControls() {
  for (const id of ["start", "mode"]) get(id).disabled = busy;
  get("reopen").hidden = !view;
  const active = !!view && !busy && mode.value === view.mode;
  get("reopen").disabled = !active;
  get("send").disabled = !active;
  get("source").disabled = !active || !view.brief?.needs.some(need => /^jackets?$/i.test(need.category));
  get("refresh").disabled = !active;
  get("save").disabled = !active || view.memory.state !== "none";
  const held = ["indexing", "unavailable"].includes(view?.memory.state);
  get("checkout").disabled = !active || stale || held || !selection || view.shortlist?.winnerId !== selection;
  for (const radio of document.querySelectorAll('input[name="offer"]')) radio.disabled = !active;
}

function renderBrief() {
  const container = get("brief");
  const brief = view.brief;
  const indicator = get("active-mode");
  indicator.hidden = false;
  indicator.textContent = view.mode === "sample" ? "Sample" : "Live";
  container.replaceChildren();
  if (!brief) {
    container.append(element("p", "Your itinerary and shopping list will appear here.", "quiet"));
    return;
  }
  const total = brief.needs.reduce((sum, need) => sum + need.quantity, 0);
  const active = Number(brief.needs.some(need => /^jackets?$/i.test(need.category)));
  container.append(
    facts([["Travel month", brief.month], ["Market", brief.market], ["Jacket size", brief.jacketSize],
      ["Jacket cap", money(brief.jacketCapMinor, brief.currency)]]),
    element("h3", "Shopping list"),
    element("p", active + " of " + total + " active · " + (total - active) + " open and unpriced", "quiet"),
    list(brief.needs.map(need => need.quantity + " × " + need.category), "needs-list"),
  );
  if (brief.assumptions.length) {
    container.append(element("h3", "Editable defaults"), list(brief.assumptions, "assumptions-list"));
  }
  for (const city of brief.cities) {
    const section = element("section", undefined, "trip-city");
    section.append(element("h3", city.name), list(city.events.map(event => event.name + " · " + event.dress)));
    container.append(section);
  }
}

function renderMemory() {
  const memory = view.memory;
  const labels = { none: "No preference saved.", indexing: "Indexing · checkout on hold", ready: "Saved preference", unavailable: "Memory unavailable · checkout on hold" };
  const container = get("memory");
  container.replaceChildren(element("p", labels[memory.state], "quiet"));
  if (memory.ruleText) container.append(element("p", memory.ruleText));
  if (memory.evidenceId) {
    const source = element("button", "View saved rule evidence", "text-button");
    source.addEventListener("click", () => showEvidence("Saved preference", "", [memory.evidenceId], source));
    container.append(source);
  }
}

function showEvidence(title, reason, ids, trigger) {
  const container = get("evidence");
  container.replaceChildren(element("h3", title));
  if (reason) container.append(element("p", reason, "quiet"));
  const records = ids.map(id => view.evidence.find(record => record.id === id)).filter(Boolean);
  if (!records.length) container.append(element("p", "No linked source was supplied.", "quiet"));
  else if (records.length < ids.length) container.append(element("p", "Some linked sources are unavailable.", "quiet"));
  for (const record of records) {
    const article = element("article", undefined, "evidence-record");
    const time = element("time", new Date(record.observedAt).toLocaleString());
    time.dateTime = record.observedAt;
    const details = element("p", (originLabel[record.origin] || record.origin) + " · ", "quiet");
    details.append(time);
    article.append(element("h3", record.title), details, element("blockquote", record.quote));
    article.append(facts([["Market", record.market], ["Seller ID", record.sellerId], ["Variant ID", record.variantId], ["Speaker", record.speaker]]));
    if (https(record.sourceUrl)) article.append(externalLink("Open source", record.sourceUrl));
    if (record.senso) {
      const refs = element("details");
      refs.append(element("summary", "Senso references"), facts([
        ["Content", record.senso.contentId], ["KB node", record.senso.kbNodeId], ["Version", record.senso.versionId],
        ["Chunk", record.senso.chunkId], ["Index", record.senso.chunkIndex],
      ]));
      article.append(refs);
    }
    container.append(article);
  }
  const back = element("button", "Back to selection", "text-button");
  back.addEventListener("click", () => trigger.focus());
  container.append(back);
  get("evidence-title").focus();
}

function card(offer, winner) {
  const article = element("article", undefined, "offer");
  article.dataset.offer = offer.id;
  article.dataset.selected = String(selection === offer.id);
  const photo = element("div", "No photo supplied", "offer-image");
  if (https(offer.imageUrl)) {
    const image = element("img");
    image.alt = offer.name;
    image.loading = "lazy";
    image.referrerPolicy = "no-referrer";
    image.addEventListener("error", () => { photo.textContent = "Photo unavailable"; }, { once: true });
    photo.replaceChildren(image);
    image.src = offer.imageUrl;
  }
  const body = element("div", undefined, "offer-body");
  const select = element("label", undefined, "offer-select");
  const radio = element("input");
  radio.type = "radio";
  radio.name = "offer";
  radio.checked = selection === offer.id;
  radio.addEventListener("change", () => {
    selection = offer.id;
    clearCheckout();
    if (stale) notice("The displayed trip may be out of date. Refresh before checkout.");
    for (const item of document.querySelectorAll("[data-offer]")) {
      item.dataset.selected = String(item.dataset.offer === selection);
    }
    updateControls();
  });
  select.append(radio, document.createTextNode("Select " + offer.seller));
  const stock = offer.available === null ? "Stock unknown" : offer.available ? "In stock" : "Out of stock";
  body.append(
    badge(offer.id === winner ? "Recommended · Meets" : verdictLabel[offer.outcome], offer.outcome),
    element("h3", offer.name),
    element("p", offer.seller + " · " + originLabel[offer.origin], "quiet"),
    element("p", money(offer.priceMinor, offer.currency), "offer-price"),
    element("p", "Size " + (offer.size ?? "unknown") + " · " + stock, "quiet"),
    select,
  );
  const identity = element("details");
  identity.append(element("summary", "Variant details"), facts([["Seller ID", offer.sellerId], ["Variant ID", offer.variantId], ["Market", offer.market]]));
  body.append(identity);
  const checks = element("ul", undefined, "checks");
  for (const check of offer.checks) {
    const item = element("li");
    const button = element("button");
    button.type = "button";
    button.append(element("span", check.label), badge(verdictLabel[check.verdict], check.verdict));
    button.addEventListener("click", () => showEvidence(offer.seller + " · " + check.label, check.reason, check.evidenceIds, button));
    item.append(button);
    checks.append(item);
  }
  body.append(checks);
  article.append(photo, body);
  return article;
}

function renderShortlist() {
  const container = get("shortlist");
  const summary = get("candidate-summary");
  const board = view.shortlist;
  get("source").textContent = view.mode === "live" && board ? "Search again for jackets" : "Source jackets";
  container.replaceChildren();
  if (!board?.offers.length) {
    summary.textContent = board ? "No matching offers in this search." : "One jacket, compared across sellers.";
    return;
  }
  summary.textContent = board.offers.length + (board.offers.length === 1 ? " offer" : " offers") +
    (board.winnerId ? " · Subtotal for one jacket. Shipping and tax undetermined." : " · No eligible recommendation.");
  if (board.continuity === "new_search") container.append(element("p", "New search · refreshed shortlist", "comparison"));
  const previous = board.offers.find(offer => offer.id === board.previousWinnerId);
  const current = board.offers.find(offer => offer.id === board.winnerId);
  if (previous && current && previous.id !== current.id) {
    container.append(element("p", "Previously " + previous.seller + " · Now " + current.seller, "comparison"));
  }
  if (board.changeNote) container.append(element("p", board.changeNote, "comparison"));
  const grid = element("div", undefined, "card-grid");
  grid.setAttribute("role", "group");
  grid.setAttribute("aria-label", "Select a jacket offer");
  grid.append(...board.offers.map(offer => card(offer, board.winnerId)));
  container.append(grid);
}

function apply(next) {
  view = next;
  selection = next.shortlist?.winnerId ?? null;
  stale = false;
  clearCheckout();
  renderBrief();
  renderMemory();
  renderShortlist();
  get("evidence").replaceChildren(element("p", "Select a jacket check to see its reason and source.", "quiet"));
  get("providers").hidden = false;
  const providers = get("provider-list");
  providers.replaceChildren(...facts(Object.entries(serviceLabel).map(([key, label]) => [label, view.providers[key]])).children);
  providers.className = "facts";
}

function logMessage(who, text) {
  if (!text) return;
  const transcript = get("transcript");
  const row = element("li");
  row.append(element("strong", who), document.createTextNode(text));
  transcript.append(row);
  transcript.scrollTop = transcript.scrollHeight;
}

function requestId() {
  if (crypto.randomUUID) return crypto.randomUUID();
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = Array.from(bytes, byte => byte.toString(16).padStart(2, "0")).join("");
  return [hex.slice(0, 8), hex.slice(8, 12), hex.slice(12, 16), hex.slice(16, 20), hex.slice(20)].join("-");
}

async function run(path, payload, type) {
  if (busy) return;
  const token = ++generation;
  const starting = type === "session";
  const sid = view?.sessionId;
  const requested = type === "handoff"
    ? view?.shortlist?.offers.find(offer => offer.id === selection && offer.id === payload.offerId)
    : null;
  if (type === "handoff" && (!requested || payload.shortlistId !== view.shortlist.id || mode.value !== view.mode)) return;
  busy = true;
  clearCheckout();
  notice(starting ? "Opening conversation…" : "Updating trip…");
  updateControls();
  try {
    const response = await fetch(path, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload), signal: AbortSignal.timeout(45000),
    });
    const data = await response.json();
    if (!response.ok) {
      const error = new Error(data.error?.message || "Request failed.");
      error.status = response.status;
      error.code = data.error?.code;
      throw error;
    }
    if (token !== generation || sid !== view?.sessionId) return;
    const next = type === "handoff" ? data.view : data;
    if (next?.schemaVersion !== 1 || (starting ? next.mode !== payload.mode || (payload.tripId !== null && next.tripId !== payload.tripId) :
      next.mode !== view.mode || next.sessionId !== sid || next.tripId !== view.tripId)) {
      throw new Error("The service returned a mismatched response.");
    }
    if (starting) get("transcript").replaceChildren();
    if (payload.action === "message") {
      logMessage("You", payload.text);
      if (draft.value.trim() === payload.text) draft.value = "";
    }
    apply(next);
    logMessage("Stylist", next.reply);
    notice("");
    if (type === "handoff") {
      showNote(data.note);
      const offer = next.shortlist?.offers.find(item => item.id === payload.offerId);
      if (data.status === "ready" && next.mode === "live" && next.shortlist?.id === payload.shortlistId &&
          next.shortlist.winnerId === payload.offerId && offer?.origin === "shopify_live" && offer.outcome === "meets" &&
          offer.sellerId === requested.sellerId && offer.variantId === requested.variantId &&
          offer.priceMinor === requested.priceMinor && offer.currency === requested.currency &&
          !["indexing", "unavailable"].includes(next.memory.state) && https(data.url)) {
        const link = externalLink("Open merchant checkout", data.url);
        link.className = "merchant-link";
        get("merchant").append(link);
      } else if (data.status === "ready") {
        showNote("Checkout link unavailable for this selection.");
      }
    }
  } catch (error) {
    if (token !== generation) return;
    stale = !!view;
    const recovery = error.status === 409 ? " Refresh the trip or start a new search." :
      error.status === 404 ? " Open a new conversation or start a trip." : "";
    const message = !error.status && (error instanceof TypeError || error.name === "TimeoutError") ?
      "The service did not respond. Try again." : error.message;
    const retry = !error.status || error.status >= 500 ? () => run(path, payload, type) : null;
    notice(message + recovery + (stale ? " The displayed trip may be out of date." : ""), retry);
  } finally {
    if (token === generation) {
      busy = false;
      updateControls();
    }
  }
}

function turn(action, text = "") {
  if (!view) return;
  return run("/api/sessions/" + encodeURIComponent(view.sessionId) + "/turns",
    { requestId: requestId(), action, text }, "turn");
}

get("session-form").addEventListener("submit", event => {
  event.preventDefault();
  run("/api/sessions", { tripId: null, mode: mode.value }, "session");
});
mode.addEventListener("change", () => {
  clearCheckout();
  if (!view) notice("Choose Start trip to use the selected mode.");
  else {
    notice(mode.value !== view.mode ? "Choose Start trip to use the selected mode." :
      stale ? "The displayed trip may be out of date. Refresh before checkout." : "");
  }
  updateControls();
});
get("reopen").addEventListener("click", () => run("/api/sessions", { tripId: view.tripId, mode: view.mode }, "session"));
get("example").addEventListener("click", () => {
  if (!draft.value || draft.value === sampleBrief || window.confirm("Replace your draft with the sample wording?")) {
    draft.value = sampleBrief;
    draft.focus();
  }
});
get("message-form").addEventListener("submit", event => {
  event.preventDefault();
  if (draft.value.trim()) turn("message", draft.value.trim());
});
get("save").addEventListener("click", () => turn("save_rule", rule));
get("source").addEventListener("click", () => turn("source_jackets"));
get("refresh").addEventListener("click", () => turn("refresh"));
get("checkout").addEventListener("click", () => {
  run("/api/sessions/" + encodeURIComponent(view.sessionId) + "/handoff", {
    requestId: requestId(), shortlistId: view.shortlist.id, offerId: selection,
  }, "handoff");
});
