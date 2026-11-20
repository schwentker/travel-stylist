"""Guided, editable demo brief. JSON accepts the full frozen Brief shape."""

import calendar
import json
import re
from copy import deepcopy
from decimal import Decimal

from .contracts.models import Brief
from .providers import SAMPLE

NUMBERS = dict(
    zip(
        ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
        range(11),
    )
)
CATEGORIES = {
    "jackets": "jackets?",
    "trousers": "trousers?",
    "pairs of shoes": "shoes?",
    "shirts": "shirts?",
    "hats": "hats?",
}
GUIDE = "Describe your June trip to Delhi, Istanbul and Barcelona. Edit quantities, month, jacket size, currency, cap or delivery market in text, or send a complete Brief JSON for other itineraries."


def explicit_save(text):
    normalized = text.strip().lower().replace("’", "'").rstrip(".!")
    return (
        re.fullmatch(
            r"(?:please )?(?:remember(?: that)?|save(?: this rule)?[: ,]*)\s*[“\"]?i (?:don't|do not) buy final[- ]sale items[.”\"]*",
            normalized,
        )
        is not None
    )


def edit(text, previous):
    default = json.loads(SAMPLE.read_text())["brief"]
    if text.lstrip().startswith("{"):
        return Brief.model_validate_json(text).model_dump()
    original = deepcopy(previous or default)
    b = deepcopy(original)
    msg = text.lower()
    if previous is None and not all(city["name"].lower() in msg for city in default["cities"]):
        return None
    if previous is None:
        b["assumptions"] = list(default["assumptions"])
    for month in calendar.month_name[1:]:
        match = re.search(r"\b" + month.lower() + r"(?:\s+(\d{4}))?\b", msg)
        if match:
            b["month"] = match.group().title()
    quantities = {n["category"]: n["quantity"] for n in b["needs"]}
    for name, category in CATEGORIES.items():
        m = re.search(
            r"\b(\d+|" + "|".join(NUMBERS) + r")\s+(?:new\s+)?(?:pairs? of\s+)?" + category + r"\b", msg
        )
        if m:
            quantities[name] = int(NUMBERS.get(m[1], m[1]))
    b["needs"] = [{"category": k, "quantity": v} for k, v in quantities.items() if v > 0]
    for city in b["cities"]:
        m = re.search(
            re.escape(city["name"]) + r"\s+(formal|informal) event(?:\s+(\d+))?\s*[:=]\s*([^.;\n]+)",
            text,
            re.IGNORECASE,
        )
        if m:
            events = [e for e in city["events"] if e["dress"] == m[1].lower()]
            number = int(m[2] or "1")
            if not 1 <= number <= len(events):
                raise ValueError("Unknown event slot.")
            events[number - 1]["name"] = m[3].strip()

    def set_field(field, value, prefix):
        b[field] = value
        b["assumptions"] = [s for s in b["assumptions"] if not s.startswith(prefix)]

    if m := re.search(r"\b(\d{2}[rsl])\b", msg):
        set_field("jacketSize", m[1].upper(), "Jacket size")
    if m := re.search(r"\b(?:ship(?:ping)? to|deliver(?:y)? (?:to|market)|market)\s+([a-z]{2})\b", msg):
        set_field("market", m[1].upper(), "US delivery")
    code = re.search(r"\b(usd|jpy|eur|gbp|cad)\b", msg)
    cap = re.search(r"(?:([$¥€£])|\b(?:usd|jpy|eur|gbp|cad))\s*(\d+(?:[.,]\d+)*)", msg)
    currency = code[1].upper() if code else b["currency"]
    if cap:
        symbol, raw = cap.groups()
        if symbol:
            by_symbol = {
                "¥": "JPY",
                "€": "EUR",
                "£": "GBP",
                "$": currency if currency == "CAD" else "USD",
            }
            if code and currency != by_symbol[symbol]:
                raise ValueError("Currency symbol and code disagree.")
            currency = by_symbol[symbol]
        if not re.fullmatch(r"(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?", raw):
            raise ValueError("Invalid amount grouping.")
        amount = Decimal(raw.replace(",", "")) * (1 if currency == "JPY" else 100)
        if amount != int(amount):
            raise ValueError("Invalid currency precision.")
        set_field("jacketCapMinor", int(amount), "$300")
    elif currency != b["currency"]:
        raise ValueError("Supply a cap in the new currency.")
    if code or cap:
        set_field("currency", currency, "USD")
    if previous is not None and b == original:
        return None
    return Brief.model_validate(b).model_dump()
