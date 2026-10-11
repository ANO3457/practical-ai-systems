import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.cost_latency_tracker.app import check_budget, summarize

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    scenarios = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = []
    for scenario in scenarios:
        summary = summarize(scenario["requests"])
        decision = check_budget(summary, scenario["max_p95_latency_ms"], scenario["max_cost_usd"])
        correct.append(decision["breached"] == scenario["gold_breached"])
    return {
        "cases": len(scenarios),
        "breach_decision_accuracy": round(mean(correct), 4),
        "scope": "two-threshold guardrail check on synthetic request logs; no statistical significance testing",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
