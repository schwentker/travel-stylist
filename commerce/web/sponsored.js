// In-chat ad placement mock. Loaded only by a dynamic import when ?ads=mock is set.
// Reads a frozen context of primitives built by app.js; never touches view, fetch or storage.
// Matching is a deterministic local stand-in for Koah's server-side intent matching:
// keywords in { question, answer } first, then the trip brief.
import ads from "./sponsored-ads.js";

const flagOn = new URLSearchParams(location.search).get("ads") === "mock";
const turnFor = { message: "brief", source_jackets: "shortlist" };
const caption = "Concept mock of an in-chat ad unit. Fictional advertiser. Not affiliated with or endorsed by Koah.";
const neverRead = "Never read: your saved buying rules, the jacket shortlist, past sessions. This placement uses no cookies.";

let slot = null;
let dismissed = false;
let checkoutSeen = false;
let epoch = 0;
let session = null;
const seen = new Set();

const enabled = () => flagOn && !!slot;

function node(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined) el.textContent = text;
  return el;
}

function button(className, text) {
  const el = node("button", className, text);
  el.type = "button";
  return el;
}

function clear() {
  if (!slot) return;
  slot.replaceChildren();
  slot.hidden = true;
}

function fill(template, brief) {
  return template
    .replace("{month}", brief?.month || "upcoming")
    .replace("{cities}", (brief?.cities || []).join(", "));
}

function briefMatches(match = {}, brief) {
  if (!brief) return false;
  if (match.minCities && brief.cities.length < match.minCities) return false;
  if (match.dressKeywords?.length) {
    const dress = brief.dress.map(d => d.toLowerCase());
    if (!match.dressKeywords.some(k => dress.some(d => d.includes(k.toLowerCase())))) return false;
  }
  return true;
}

function pick(turn, ctx) {
  const text = ((ctx.question || "") + " " + (ctx.answer || "")).toLowerCase();
  const eligible = ads
    .filter(ad => ad.turn === turn)
    .filter(ad => (ad.keywords || []).some(k => text.includes(k)) || briefMatches(ad.match, ctx.brief));
  return eligible.sort((a, b) => b.priority - a.priority)[0] || null;
}

function render(ad, ctx) {
  const unit = node("article", "sponsored-unit");
  unit.dataset.format = ad.format;
  unit.dataset.adId = ad.id;

  const head = node("header", "sponsored-head");
  const why = button("sponsored-why", "Why this ad?");
  why.setAttribute("aria-expanded", "false");
  why.setAttribute("aria-controls", "sponsored-why-text");
  head.append(
    node("span", "sponsored-domain", ad.domain),
    node("span", "sponsored-sponsor", ad.sponsor),
    document.createTextNode(" · "),
    node("span", "sponsored-label", "Sponsored"),
    why,
  );

  const whyText = node("div", "sponsored-why-text");
  whyText.id = "sponsored-why-text";
  whyText.hidden = true;
  whyText.append(node("p", undefined, "Matched on this turn: " + fill(ad.why, ctx.brief) + "."));
  if ((ad.body || "").includes("{month}") && ctx.brief?.month) {
    whyText.append(node("p", undefined, "Used in wording: " + ctx.brief.month + "."));
  }
  whyText.append(node("p", undefined, neverRead));
  why.addEventListener("click", () => {
    const open = why.getAttribute("aria-expanded") === "true";
    why.setAttribute("aria-expanded", String(!open));
    whyText.hidden = open;
  });

  unit.append(head, whyText);

  if (ad.format === "poll") {
    const poll = node("fieldset", "sponsored-poll");
    poll.append(node("legend", "sponsored-title", ad.question));
    const thanks = node("p", "sponsored-poll-thanks", "Thanks. Results are not collected in this demo.");
    thanks.setAttribute("role", "status");
    thanks.hidden = true;
    const options = ad.options.map(label => {
      const option = button("sponsored-poll-option", label);
      option.setAttribute("aria-pressed", "false");
      option.addEventListener("click", () => {
        options.forEach(o => o.setAttribute("aria-pressed", String(o === option)));
        unit.dataset.voted = "true";
        thanks.hidden = false;
      });
      return option;
    });
    poll.append(...options);
    unit.append(poll, thanks);
  } else {
    const note = node("p", "sponsored-demo-note", "Demo only. No advertiser link.");
    note.setAttribute("role", "status");
    note.hidden = true;
    const cta = button("sponsored-cta", ad.cta);
    cta.addEventListener("click", () => {
      unit.dataset.ctaClicked = "true";
      note.hidden = false;
    });
    unit.append(node("h3", "sponsored-title", ad.title), node("p", "sponsored-body", fill(ad.body, ctx.brief)), cta, note);
  }

  const foot = node("footer", "sponsored-foot");
  const hide = button("sponsored-hide", "Hide ad");
  hide.addEventListener("click", () => {
    dismissed = true;
    clear();
    document.getElementById("draft")?.focus();
  });
  foot.append(node("p", "sponsored-caption", caption), hide);
  unit.append(foot);

  slot.replaceChildren(unit);
  slot.hidden = false;
}

export function initSponsored(slotEl) {
  slot = slotEl;
}

export function reset() {
  epoch += 1;
  checkoutSeen = false;
  session = null;
  seen.clear();
  clear();
}

export function onTurn(ctx) {
  try {
    if (!enabled()) return clear();
    if (session && ctx.sessionId !== session) return;
    session = ctx.sessionId;
    if (ctx.action === "handoff") {
      checkoutSeen = true;
      return clear();
    }
    const turn = turnFor[ctx.action];
    if (!turn || dismissed || checkoutSeen) return;
    const key = ctx.sessionId + ":" + ctx.requestId;
    if (seen.has(key)) return;
    seen.add(key);
    const started = epoch;
    const ad = pick(turn, ctx);
    if (started !== epoch) return;
    if (ad) render(ad, ctx);
    else clear();
  } catch (error) {
    console.warn("[sponsored-mock]", error);
  }
}
