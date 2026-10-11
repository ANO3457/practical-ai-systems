import { dispatch, evaluateAll, KnowledgeTools } from "./app.js";

const tools = new KnowledgeTools();
const queryInput = document.getElementById("query") as HTMLInputElement;
const output = document.getElementById("output") as HTMLPreElement;
const evalOutput = document.getElementById("eval-output") as HTMLPreElement;

document.getElementById("run")?.addEventListener("click", () => {
  const message = { method: "tools/call", id: 1, params: { name: "search_docs", arguments: { query: queryInput.value } } };
  output.textContent = JSON.stringify(dispatch(message, tools), null, 2);
});

document.getElementById("run-eval")?.addEventListener("click", () => {
  evalOutput.textContent = JSON.stringify(evaluateAll(), null, 2);
});
