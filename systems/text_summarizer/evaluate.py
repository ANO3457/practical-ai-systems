import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.text_summarizer.app import compression_ratio, summarize

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    hits, ratios = [], []
    for case in cases:
        summary = summarize(case["text"], case.get("n", 2))
        hits.append(any(case["key_sentence"] in sent for sent in summary))
        ratios.append(compression_ratio(case["text"], summary))
    return {
        "cases": len(cases),
        "key_sentence_recall": round(mean(hits), 4),
        "avg_compression_ratio": round(mean(ratios), 4),
        "scope": "word-frequency extractive baseline on synthetic text; no model used",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
