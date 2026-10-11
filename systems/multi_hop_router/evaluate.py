import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.multi_hop_router.app import DocQA, answer_multi_hop, load_chunks

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    qa = DocQA(load_chunks())
    correct = [answer_multi_hop(c["question"], qa)["abstained"] == c["gold_abstained"] for c in cases]
    return {
        "cases": len(cases),
        "abstention_accuracy": round(mean(correct), 4),
        "scope": "heuristic sentence/connector split over this project's own bundled synthetic documents",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
