import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


from systems.query_rewriter.app import BM25, expand_query

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    data = json.loads((EVAL_DIR / "cases.json").read_text())
    index = BM25(data["corpus"])
    baseline_hits, expanded_hits = [], []
    for query in data["queries"]:
        base = index.search(query["text"], 1)
        baseline_hits.append(bool(base) and base[0][0] == query["gold"])
        expanded = index.search(expand_query(query["text"]), 1)
        expanded_hits.append(bool(expanded) and expanded[0][0] == query["gold"])
    return {
        "cases": len(data["queries"]),
        "recall_at_1_baseline": round(mean(baseline_hits), 4),
        "recall_at_1_expanded": round(mean(expanded_hits), 4),
        "scope": "tiny four-document synthetic corpus; hand-picked synonym list",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
