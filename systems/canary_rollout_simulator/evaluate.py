import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.canary_rollout_simulator.app import decide

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = [decide(c["baseline"], c["canary"])["decision"] == c["gold_decision"] for c in cases]
    return {
        "cases": len(cases),
        "decision_accuracy": round(mean(correct), 4),
        "scope": "fixed-threshold two-sample comparison; no statistical significance testing",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
