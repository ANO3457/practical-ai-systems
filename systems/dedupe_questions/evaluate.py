import json
from pathlib import Path

def prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
from systems.dedupe_questions.app import similarity

EVAL_DIR = Path(__file__).parent / "eval"
THRESHOLD = 0.6


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    tp = fp = fn = 0
    for case in cases:
        predicted = similarity(case["a"], case["b"]) >= THRESHOLD
        expected = case["duplicate"]
        tp += predicted and expected
        fp += predicted and not expected
        fn += (not predicted) and expected
    metrics = prf(tp, fp, fn)
    return {
        "cases": len(cases),
        **{k: round(v, 4) for k, v in metrics.items()},
        "method": f"token jaccard similarity >= {THRESHOLD}",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
