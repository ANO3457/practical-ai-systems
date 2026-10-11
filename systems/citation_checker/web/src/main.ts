import { checkCitations, evaluateAll, SAMPLE_CHUNKS } from "./app.js";

const textInput = document.getElementById("text") as HTMLTextAreaElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  output.textContent = JSON.stringify(checkCitations(textInput.value, SAMPLE_CHUNKS), null, 2);
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
