import { test } from "node:test";
import { strict as assert } from "node:assert";
import { checkCaption, evaluateAll } from "./app.js";

test("good caption passes", () => {
  assert.equal(checkCaption("A golden retriever running across a sunny beach.").passed, true);
});
test("placeholder caption is banned", () => {
  const result = checkCaption("image of a dog");
  assert.equal(result.passed, false);
  assert.ok(result.reasons.some((r) => r.startsWith("banned_phrase")));
});
test("too short caption fails", () => {
  assert.ok(checkCaption("A cat.").reasons.includes("too_short"));
});
test("missing required keyword fails", () => {
  const result = checkCaption("A red sports car.", ["truck"]);
  assert.ok(result.reasons.some((r) => r.startsWith("missing_keywords")));
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().accuracy, 1);
});
