import { test } from "node:test";
import { strict as assert } from "node:assert";
import { audit, cohenKappa, evaluateAll, judge, SAMPLE_ROWS } from "./app.js";

test("judge flags high lexical overlap as supported", () => {
  assert.equal(judge("The Pro plan costs $8 per month", "The Pro plan costs $8 per user per month."), "supported");
});
test("judge flags low overlap as unsupported", () => {
  assert.equal(judge("The weather is sunny today", "Notes sync automatically every 60 seconds."), "unsupported");
});
test("kappa is 1 for identical raters", () => {
  assert.equal(cohenKappa(["a", "b", "a"], ["a", "b", "a"]), 1);
});
test("audit reports agreement and kappa", () => {
  const report = audit(SAMPLE_ROWS);
  assert.equal(report.cases, SAMPLE_ROWS.length);
  assert.ok(report.judge_human_a_agreement >= 0 && report.judge_human_a_agreement <= 1);
});
test("evaluation runs end to end", () => {
  assert.equal(evaluateAll().cases, SAMPLE_ROWS.length);
});
