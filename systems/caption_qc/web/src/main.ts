import { checkCaption, evaluateAll } from "./app.js";

const captionInput = document.getElementById("caption") as HTMLInputElement;
const keywordsInput = document.getElementById("keywords") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  const keywords = keywordsInput.value.split(",").map((k) => k.trim()).filter(Boolean);
  output.textContent = JSON.stringify(checkCaption(captionInput.value, keywords), null, 2);
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
