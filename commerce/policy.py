"""Read a complete same-seller Shopify policy body transiently. Fail closed on incomplete scope."""

import re
from html.parser import HTMLParser

import httpx

from .providers import Evidence, now


class PolicyBody(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.complete = False
        self.referenced = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if not self.depth and "shopify-policy__body" in attrs.get("class", "").split():
            self.depth = 1
        elif self.depth and tag == "div":
            self.depth += 1
        if self.depth and tag in ("a", "iframe", "script", "img"):
            self.referenced = True

    def handle_endtag(self, tag):
        if self.depth and tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.complete = True

    def handle_data(self, text):
        if self.depth and text.strip():
            self.parts.append(text.strip())


def terms(row):
    url = row.policy_url
    if not url:
        return None
    # Only the official refund-policy URL from the exact seller lookup reaches this function.
    try:
        with httpx.stream("GET", url, timeout=4, follow_redirects=False) as response:
            if response.status_code != 200 or "html" not in response.headers.get("content-type", ""):
                return None
            content = bytearray()
            for chunk in response.iter_bytes():
                content.extend(chunk)
                if len(content) > 800000:
                    return None
        parser = PolicyBody()
        parser.feed(content.decode("utf-8"))
        parser.close()
    except (httpx.HTTPError, UnicodeError, ValueError):
        return None
    quote = " ".join(parser.parts)
    if not parser.complete or parser.referenced or not 0 < len(quote) <= 10000:
        return None
    market = row.offer.market
    markers = {
        "US": r"United States|U\.S\.|USA",
        "CA": r"Canada",
        "GB": r"United Kingdom",
        "JP": r"Japan",
    }
    if not re.search(markers.get(market, r"(?!)"), quote, re.IGNORECASE):
        return None
    specific = row.offer.name.casefold() in quote.casefold()
    if not specific and not re.search(
        r"\ball (items|orders|products|purchases)\b", quote, re.IGNORECASE
    ):
        return None
    # Effective windows and item exceptions need explicit verification beyond this narrow reader.
    if re.search(r"effective|until|except|selected|certain|exclud|\b20\d{2}\b", quote, re.IGNORECASE):
        return None
    markdown_unknown = (
        row.list_minor is None or row.offer.priceMinor is None or row.list_minor < row.offer.priceMinor
    )
    if markdown_unknown and re.search(
        r"discount|markdown|sale price|sale items|% off", quote, re.IGNORECASE
    ):
        return None
    return Evidence(
        id="terms-" + row.offer.id,
        kind="merchant_policy",
        origin="merchant",
        speaker=None,
        title="Official return policy",
        quote=quote,
        sourceUrl=url,
        sellerId=row.offer.sellerId,
        variantId=row.offer.variantId,
        market=market,
        observedAt=now(),
        senso=None,
    )


def discount_gate(quote, row):
    """An explicit inclusive final-sale threshold overrides a general returns clause."""
    match = re.search(
        r"(?:discounted|marked down) (?:by )?(?:at least (\d{1,3})% |(\d{1,3})% or more )(?:are|is) final sale",
        quote,
        re.IGNORECASE,
    )
    if not match:
        return None
    original, current = row.list_minor, row.offer.priceMinor
    if not isinstance(original, int) or original <= 0 or current is None or current > original:
        return "unknown"
    if 100 * (original - current) >= int(match[1] or match[2]) * original:
        return "fails"
    return None
