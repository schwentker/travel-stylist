"""Provision and retrieve only the isolated, authored demo sources."""

import argparse
import hashlib
import json

from .providers import SAMPLE, Blocked, Senso


def provision(db, adapter, buyer, mode, doc):
    # Opaque per-buyer binding includes mode, artifact scope, version and exact text.
    fields = [
        adapter.namespace,
        buyer,
        mode,
        doc["id"],
        doc["origin"],
        doc["market"],
        doc["sellerId"],
        doc["variantId"],
        doc["quote"],
    ]
    binding = hashlib.sha256(json.dumps(fields).encode()).hexdigest()
    db.execute("INSERT OR IGNORE INTO sources(binding) VALUES(?)", (binding,))
    content, node = db.execute("SELECT content,node FROM sources WHERE binding=?", (binding,)).fetchone()
    if not content:
        content, node = adapter.bind(binding, doc["quote"])
        db.execute("UPDATE sources SET content=?,node=? WHERE binding=?", (content, node, binding))
    return binding, content, node


def seed(db, adapter, buyer, mode):
    fixture = json.loads(SAMPLE.read_text())
    documents = [fixture["briefEvidence"]] + [r["policy"] for r in fixture["listings"]]
    for doc in documents:
        provision(db, adapter, buyer, mode, doc)


if __name__ == "__main__":
    from .workflow import Workflow

    parser = argparse.ArgumentParser(
        description="Index the four fictional reference documents in the configured Senso organization."
    )
    parser.add_argument("--buyer", required=True, help="Opaque isolated demo buyer binding")
    args = parser.parse_args()
    try:
        seed(Workflow().connect(), Senso(), args.buyer, "sample")
    except Blocked as exc:
        parser.exit(1, str(exc) + "\n")
