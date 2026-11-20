"""Version 1 of the same-origin commerce browser contract."""
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from datetime import datetime
from urllib.parse import urlsplit


class WireModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


Identifier = Annotated[str, Field(min_length=1)]
RequestId = Annotated[str, Field(pattern=r"^[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$")]
Instant = Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|\+00:00)$", json_schema_extra={"format": "date-time"})]
Minor = Annotated[int, Field(ge=0)]
Mode = Literal["live", "sample"]
Verdict = Literal["meets", "fails", "unknown"]
ProviderMode = Literal["live", "sample", "unavailable", "unused", "guided"]


class SessionRequest(WireModel):
    tripId: Identifier | None
    mode: Mode


class TurnRequest(WireModel):
    requestId: RequestId
    action: Literal["message", "source_jackets", "save_rule", "refresh"]
    text: str


class OverrideApproval(WireModel):
    priceMinor: Minor
    currency: Identifier
    checks: Annotated[dict[Identifier, Literal["fails", "unknown"]], Field(min_length=1)]


class HandoffRequest(WireModel):
    requestId: RequestId
    shortlistId: Identifier
    offerId: Identifier
    override: OverrideApproval | None = None


class ErrorDetail(WireModel):
    code: str
    message: str


class ApiError(WireModel):
    error: ErrorDetail


class Providers(WireModel):
    catalog: ProviderMode
    senso: ProviderMode
    jev: ProviderMode
    language: ProviderMode


class Event(WireModel):
    name: str
    dress: Literal["formal", "informal"]


class City(WireModel):
    name: str
    events: list[Event]


class Need(WireModel):
    category: str
    quantity: Annotated[int, Field(gt=0)]


class Brief(WireModel):
    month: str
    market: str
    currency: str
    jacketSize: str
    jacketCapMinor: Minor
    assumptions: list[str]
    cities: list[City]
    needs: list[Need]


class Memory(WireModel):
    state: Literal["none", "indexing", "ready", "unavailable"]
    ruleText: str | None
    evidenceId: Identifier | None


class SensoRef(WireModel):
    contentId: Identifier
    kbNodeId: Identifier | None
    versionId: Identifier | None
    chunkId: Identifier | None
    chunkIndex: Annotated[int, Field(ge=0)] | None


class TimedModel(WireModel):
    observedAt: Instant

    @field_validator("observedAt")
    @classmethod
    def valid_utc_date(cls, value: str) -> str:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class Evidence(TimedModel):
    id: Identifier
    kind: Literal["buyer_brief", "buyer_rule", "catalog_variant", "merchant_policy", "merchant_reply", "sample_policy"]
    origin: Literal["buyer", "merchant", "shopify_live", "sample"]
    speaker: Literal["agent", "human"] | None
    title: str
    quote: str
    sourceUrl: str | None
    sellerId: Identifier | None
    variantId: Identifier | None
    market: str | None
    senso: SensoRef | None


class Check(WireModel):
    id: Identifier
    label: str
    verdict: Verdict
    reason: str
    evidenceIds: list[Identifier]


class Offer(WireModel):
    id: Identifier
    sellerId: Identifier
    seller: str
    variantId: Identifier
    name: str
    size: str | None
    imageUrl: str | None
    market: str
    available: bool | None
    priceMinor: Minor | None
    currency: str | None
    origin: Literal["shopify_live", "sample"]
    outcome: Verdict
    checks: list[Check]


class Shortlist(TimedModel):
    id: Identifier
    slot: Literal["formal_jacket"]
    continuity: Literal["first", "same_set", "new_search"]
    previousWinnerId: Identifier | None
    winnerId: Identifier | None
    changeNote: str | None
    offers: Annotated[list[Offer], Field(max_length=3)]


class View(WireModel):
    schemaVersion: Literal[1]
    tripId: Identifier
    sessionId: Identifier
    mode: Mode
    reply: str
    providers: Providers
    brief: Brief | None
    memory: Memory
    shortlist: Shortlist | None
    evidence: list[Evidence]


class HandoffBase(WireModel):
    note: str
    view: View


class Ready(HandoffBase):
    status: Literal["ready"]
    url: Annotated[str, Field(pattern=r"^https://[^\s/?#]+(?:[/?#][^\s]*)?$")]

    @model_validator(mode="after")
    def qualifying_live_offer(self):
        shortlist = self.view.shortlist
        if not urlsplit(self.url).hostname or self.view.mode != "live" or not shortlist:
            raise ValueError("Ready requires a live shortlist and HTTPS checkout host.")
        if self.view.memory.state in {"indexing", "unavailable"} or not any(
            offer.id == shortlist.winnerId and offer.origin == "shopify_live" and offer.outcome == "meets"
            for offer in shortlist.offers
        ):
            raise ValueError("Ready requires a qualifying live winner.")
        return self


def may_override(offer):
    return (
        offer.origin == "shopify_live"
        and offer.available is True
        and offer.priceMinor is not None
        and bool(offer.currency)
        and any(check.id == "checkout" and check.verdict == "meets" for check in offer.checks)
    )


class OverrideReady(HandoffBase):
    status: Literal["override_ready"]
    offerId: Identifier
    url: Annotated[str, Field(pattern=r"^https://[^\s/?#]+(?:[/?#][^\s]*)?$")]

    @model_validator(mode="after")
    def selected_live_offer(self):
        board = self.view.shortlist
        if self.view.mode != "live" or not board or not any(
            offer.id == self.offerId and offer.outcome != "meets" and may_override(offer)
            for offer in board.offers
        ):
            raise ValueError("An override requires a verified selection with unmet checks.")
        return self


class Held(HandoffBase):
    status: Literal["changed", "unavailable", "sample"]
    url: None


HandoffResponse = Annotated[Ready | OverrideReady | Held, Field(discriminator="status")]
