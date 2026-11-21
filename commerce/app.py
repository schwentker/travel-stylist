"""Single-worker commerce application. Launch from the repository root."""

import json
from pathlib import Path
from typing import Literal
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .contracts.models import (
    ApiError,
    ErrorDetail,
    HandoffRequest,
    HandoffResponse,
    SessionRequest,
    TurnRequest,
    View,
)
from .workflow import Workflow

ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "contracts" / "v1" / "examples"
app = FastAPI(
    title="Travel Stylist foundation", version="1", docs_url=None, redoc_url=None, openapi_url=None
)
ERRORS = {status: {"model": ApiError} for status in (404, 409, 422, 503)}


def api_error(status: int, code: str, message: str):
    body = ApiError(error=ErrorDetail(code=code, message=message))
    return JSONResponse(status_code=status, content=body.model_dump())


@app.exception_handler(HTTPException)
async def handle_http_error(request: Request, exc: HTTPException):
    return api_error(exc.status_code, *exc.detail)


@app.exception_handler(RequestValidationError)
async def handle_invalid_request(request: Request, exc: RequestValidationError):
    return api_error(422, "INVALID_INPUT", "Check the request fields and try again.")


def fixture(name: str):
    return json.loads((EXAMPLES / f"{name}.json").read_text())


load_dotenv(ROOT.parent / ".env", override=False)
app.state.workflow = Workflow()


@app.post("/api/sessions", response_model=View, responses=ERRORS)
def start_session(body: SessionRequest, request: Request, response: Response):
    buyer = request.cookies.get("commerce_buyer") or str(uuid4())
    with app.state.workflow.lock:
        view = app.state.workflow.start(buyer, body)
    response.set_cookie(
        "commerce_buyer",
        buyer,
        httponly=True,
        samesite="strict",
        secure=request.url.scheme == "https",
        max_age=31536000,
    )
    return view


@app.get("/api/examples/{name}", response_model=View, include_in_schema=False)
def sample_board(name: Literal["new", "before", "indexing", "fresh-after", "no-winner"]):
    return View.model_validate(fixture(name))


@app.post("/api/sessions/{sessionId}/turns", response_model=View, responses=ERRORS)
def turn(sessionId: str, body: TurnRequest, request: Request):
    with app.state.workflow.lock:
        return app.state.workflow.mutation(request.cookies.get("commerce_buyer"), sessionId, body)


@app.post("/api/sessions/{sessionId}/handoff", response_model=HandoffResponse, responses=ERRORS)
def handoff(sessionId: str, body: HandoffRequest, request: Request):
    with app.state.workflow.lock:
        return app.state.workflow.mutation(
            request.cookies.get("commerce_buyer"), sessionId, body, handoff=True
        )


app.mount("/", StaticFiles(directory=ROOT / "web", html=True), name="static")
