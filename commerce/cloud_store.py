"""SQLite in the Cloudflare Durable Object reached through the container's private intercept."""
import httpx
from fastapi import HTTPException


class QueryResult:
    def __init__(self, payload):
        self.rows = payload["rows"]
        self.rowcount = payload["changes"]

    def fetchone(self):
        return next(iter(self.rows), None)


class CloudStore:
    def __init__(self):
        self.client = httpx.Client(base_url="http://travel-storage.invalid", trust_env=False, timeout=8)

    def execute(self, query, params=()):
        try:
            response = self.client.post("/", json={"query": query, "params": params})
            response.raise_for_status()
            return QueryResult(response.json())
        except httpx.HTTPError as exc:
            raise HTTPException(503, ("STORAGE_UNAVAILABLE", "Trip storage is unavailable.")) from exc

    def executescript(self, schema):
        for statement in schema.split(";"):
            if statement.strip():
                self.execute(statement)
