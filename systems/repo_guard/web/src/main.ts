import { evaluateAll, scan } from "./app.js";

const textInput = document.getElementById("text") as HTMLTextAreaElement;
const shellLike = document.getElementById("shell-like") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  output.textContent = JSON.stringify(scan(textInput.value, shellLike.checked), null, 2);
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
