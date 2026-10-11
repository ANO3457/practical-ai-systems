import { compressionRatio, evaluateAll, summarize } from "./app.js";

const textInput = document.getElementById("text") as HTMLTextAreaElement;
const nInput = document.getElementById("n") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  const n = Math.max(1, Number(nInput.value) || 2);
  const summary = summarize(textInput.value, n);
  const ratio = compressionRatio(textInput.value, summary);
  output.textContent = `${summary.join("\n")}\n\ncompression_ratio: ${ratio.toFixed(2)}`;
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
