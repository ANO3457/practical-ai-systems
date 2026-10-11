import { evaluateAll, SemanticCache } from "./app.js";

const cache = new SemanticCache(50, 60_000);
const queryInput = document.getElementById("query") as HTMLInputElement;
const valueInput = document.getElementById("value") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("put")?.addEventListener("click", () => {
  cache.put(queryInput.value, valueInput.value);
  output.textContent = `stored.\n${JSON.stringify(cache.stats(), null, 2)}`;
});

document.getElementById("get")?.addEventListener("click", () => {
  const value = cache.get(queryInput.value);
  output.textContent = `${value === null ? "MISS" : `HIT: ${value}`}\n${JSON.stringify(cache.stats(), null, 2)}`;
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
