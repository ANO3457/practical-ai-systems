import { DocQA, CHUNKS, evaluateAll } from "./app.js";

const qa = new DocQA(CHUNKS);
const questionInput = document.getElementById("question") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  const answer = qa.answer(questionInput.value);
  output.textContent = `${answer.text}\n\nsources: ${answer.citations.join(", ") || "none (abstained)"}`;
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
