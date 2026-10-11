import { EVAL_CASES, evaluateAll, extractFields } from "./app.js";

const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  output.textContent = JSON.stringify(extractFields(EVAL_CASES[0].lines), null, 2);
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
