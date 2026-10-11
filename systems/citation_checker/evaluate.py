import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.citation_checker.app import check_citations

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    case = json.loads((EVAL_DIR / "cases.json").read_text())
    report = check_citations(case["answer"], case["chunks"])
    statuses = [r["status"] for r in report["results"]]
    correct = [got == gold for got, gold in zip(statuses, case["gold_statuses"])]
    return {
        "cases": len(case["gold_statuses"]),
        "citation_status_accuracy": round(mean(correct), 4),
        "scope": "lexical overlap over one synthetic answer with four inline citations",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
