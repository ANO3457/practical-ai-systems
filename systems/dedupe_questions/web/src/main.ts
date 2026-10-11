import { evaluateAll, similarity } from "./app.js";

const qa = document.getElementById("qa") as HTMLInputElement;
const qb = document.getElementById("qb") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  const score = similarity(qa.value, qb.value);
  output.textContent = `similarity: ${score.toFixed(2)}\n${score >= 0.6 ? "duplicate" : "not duplicate"}`;
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
