import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.csv_schema_validator.app import validate_rows

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    case = json.loads((EVAL_DIR / "cases.json").read_text())
    results = validate_rows(case["schema"], case["rows"])
    predicted_valid = [not r["errors"] for r in results]
    correct = [p == g for p, g in zip(predicted_valid, case["gold_valid"])]
    return {
        "cases": len(case["rows"]),
        "row_validity_accuracy": round(mean(correct), 4),
        "scope": "declared-schema type/required checks only; no format or business-rule validation",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
