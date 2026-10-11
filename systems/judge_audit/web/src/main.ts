import { evaluateAll } from "./app.js";

const output = document.getElementById("output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  output.textContent = JSON.stringify(evaluateAll(), null, 2);
});
