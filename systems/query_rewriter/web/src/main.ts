import { CORPUS, evaluateAll, expandQuery, search } from "./app.js";

const queryInput = document.getElementById("query") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  const expanded = expandQuery(queryInput.value);
  const baseline = search(CORPUS, queryInput.value, false, 3);
  const withExpansion = search(CORPUS, queryInput.value, true, 3);
  output.textContent = `expanded query: ${expanded}\n\nbaseline hits: ${JSON.stringify(baseline)}\nexpanded hits: ${JSON.stringify(withExpansion)}`;
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
