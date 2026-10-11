import json
from pathlib import Path

def prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
from systems.prompt_injection_detector.app import scan

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    tp = fp = fn = 0
    for case in cases:
        predicted = scan(case["text"])["flagged"]
        expected = case["malicious"]
        tp += predicted and expected
        fp += predicted and not expected
        fn += (not predicted) and expected
    metrics = prf(tp, fp, fn)
    return {
        "cases": len(cases),
        **{k: round(v, 4) for k, v in metrics.items()},
        "scope": "five hand-written regex heuristics; not trained on real attack traffic",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
