import { band, evaluateAll, gradeLevel } from "./app.js";

const textInput = document.getElementById("text") as HTMLTextAreaElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  const grade = gradeLevel(textInput.value);
  output.textContent = `grade_level: ${grade}\nband: ${band(grade)}`;
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
