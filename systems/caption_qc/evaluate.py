import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.caption_qc.app import check_caption

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = [
        check_caption(c["caption"], c.get("required_keywords"))["passed"] == c["gold_pass"]
        for c in cases
    ]
    return {
        "cases": len(cases),
        "qc_accuracy": round(mean(correct), 4),
        "scope": "rule-based text checks only; does not inspect the underlying image",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
