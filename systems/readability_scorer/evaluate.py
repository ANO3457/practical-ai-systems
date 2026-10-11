import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.readability_scorer.app import band, grade_level

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = [band(grade_level(c["text"])) == c["band"] for c in cases]
    return {
        "cases": len(cases),
        "band_accuracy": round(mean(correct), 4),
        "scope": "vowel-run syllable heuristic; a rough proxy, not a validated readability model",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
