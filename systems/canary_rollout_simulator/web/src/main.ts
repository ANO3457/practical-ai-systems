import { decide, evaluateAll } from "./app.js";

const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  const baseline = { error_rate: 0.01, p95_latency_ms: 200 };
  const canary = { error_rate: 0.05, p95_latency_ms: 210 };
  output.textContent = JSON.stringify(decide(baseline, canary), null, 2);
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
