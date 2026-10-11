import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.faq_router.app import route

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = [route(c["text"]) == c["intent"] for c in cases]
    return {
        "cases": len(cases),
        "routing_accuracy": round(mean(correct), 4),
        "scope": "fixed keyword-overlap router over five intents plus an unknown fallback",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
