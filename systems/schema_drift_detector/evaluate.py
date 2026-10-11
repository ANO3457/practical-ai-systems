import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.schema_drift_detector.app import detect_drift

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = [detect_drift(c["schema"], c["records"]) == c["gold"] for c in cases]
    return {
        "cases": len(cases),
        "exact_report_match": round(mean(correct), 4),
        "scope": "declared-schema diff only; no semantic or value-range drift detection",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
