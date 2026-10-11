import json
from pathlib import Path

from systems.retrieval_eval_harness.app import compare_strategies

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    data = json.loads((EVAL_DIR / "cases.json").read_text())
    comparison = compare_strategies(data["corpus"], data["queries"], k=3)
    return {
        "cases": len(data["queries"]),
        "baseline_recall_at_k": comparison["baseline"]["recall_at_k"],
        "baseline_mrr": comparison["baseline"]["mrr"],
        "baseline_ndcg_at_k": comparison["baseline"]["ndcg_at_k"],
        "expanded_recall_at_k": comparison["expanded"]["recall_at_k"],
        "expanded_mrr": comparison["expanded"]["mrr"],
        "expanded_ndcg_at_k": comparison["expanded"]["ndcg_at_k"],
        "scope": "tiny four-document synthetic corpus; binary relevance judgments",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
