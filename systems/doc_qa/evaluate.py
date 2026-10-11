"""Evaluate document Q&A: retrieval recall, citation accuracy, answer hits, abstention."""
from __future__ import annotations

import json
from pathlib import Path

from systems.doc_qa.app import DocQA, from_env, load_chunks

EVAL_DIR = Path(__file__).parent / "eval"


def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def write_results(path: Path, system: str, method: str, metrics: dict, cases: int, notes: str = "") -> dict:
    record = {
        "system": system,
        "method": method,
        "dataset": {"cases": cases, "source": "synthetic, committed in eval/"},
        "metrics": {k: round(v, 4) if isinstance(v, float) else v for k, v in sorted(metrics.items())},
        "notes": notes,
    }
    Path(path).write_text(json.dumps(record, indent=2) + "\n")
    return record


def evaluate(llm=None, write: bool = False) -> dict:
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    qa = DocQA(load_chunks(), llm=llm)
    answerable = [c for c in cases if c["gold"]]
    fact_cases = [c for c in answerable if c["expect"]]
    unanswerable = [c for c in cases if not c["gold"]]
    runs = {c["question"]: qa.answer(c["question"]) for c in cases}
    metrics = {
        "recall_at_3": mean(c["gold"] in runs[c["question"]].retrieved for c in answerable),
        "citation_accuracy": mean(runs[c["question"]].citations[:1] == [c["gold"]] for c in answerable),
        "answer_contains_fact": mean(c["expect"].lower() in runs[c["question"]].text.lower() for c in fact_cases),
        "false_abstention_rate": mean(runs[c["question"]].abstained for c in answerable),
        "correct_abstention_rate": mean(runs[c["question"]].abstained for c in unanswerable),
    }
    method = "model" if llm else "bm25 + extractive sentence (offline baseline)"
    record = {"metrics": metrics, "method": method, "cases": len(cases)}
    if write:
        record = write_results(EVAL_DIR / "results.json", "doc_qa", method, metrics, len(cases))
    return record


if __name__ == "__main__":
    print(json.dumps(evaluate(from_env(), write=True), indent=2))
