import json
from pathlib import Path

def prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
from systems.pii_redactor.app import detect

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    tp = fp = fn = 0
    for case in cases:
        predicted = {f["type"] for f in detect(case["text"])}
        gold = set(case["gold_types"])
        tp += len(predicted & gold)
        fp += len(predicted - gold)
        fn += len(gold - predicted)
    metrics = prf(tp, fp, fn)
    return {
        "cases": len(cases),
        **{k: round(v, 4) for k, v in metrics.items()},
        "scope": "toy regex patterns for email/phone/ssn/credit-card shapes only; not a compliance tool",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
