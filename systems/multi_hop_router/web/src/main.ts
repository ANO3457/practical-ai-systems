import { answerMultiHop, evaluateAll } from "./app.js";

const questionInput = document.getElementById("question") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  output.textContent = JSON.stringify(answerMultiHop(questionInput.value), null, 2);
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
