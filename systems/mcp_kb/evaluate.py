"""Check deterministic retrieval over the bundled synthetic documents."""
import json
from pathlib import Path
from systems.mcp_kb.server import KnowledgeTools

CASES = [(c["query"], c["gold"]) for c in json.loads((Path(__file__).parent / "eval" / "cases.json").read_text())]


def evaluate():
    tools = KnowledgeTools()
    hits = [tools.search(query, limit=3)["results"] for query, _ in CASES]
    recall = sum(any(expected == row["id"] for row in rows) for rows, (_, expected) in zip(hits, CASES)) / len(CASES)
    return {"cases": len(CASES), "recall_at_3": recall, "scope": "synthetic local documents; illustrative MCP JSON-RPC subset"}


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
