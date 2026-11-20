"""Optional loopback intent extraction. The model cannot authorize a save."""

import asyncio
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict


class Intent(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    intent: Literal["brief", "evidence", "source_jackets", "other"]
    excerpt: str


async def generate(text):
    async with httpx.AsyncClient(trust_env=False) as client:
        res = await client.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "stream": False,
                "format": Intent.model_json_schema(),
                "prompt": "Classify the buyer message. Return an exact excerpt supporting the intent. Only classify an explicit shopping search as source_jackets. Buyer message: "
                + text,
            },
        )
        res.raise_for_status()
        result = Intent.model_validate_json(res.json()["response"])
        if not result.excerpt.strip() or result.excerpt not in text:
            return None
        return result


def parse(text):
    async def limited():
        return await asyncio.wait_for(generate(text), timeout=4)

    try:
        return asyncio.run(limited())
    except (ValueError, KeyError, TypeError, TimeoutError, httpx.HTTPError):
        return None
