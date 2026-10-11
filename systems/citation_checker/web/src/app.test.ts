import { test } from "node:test";
import { strict as assert } from "node:assert";
import { checkCitations, evaluateAll, SAMPLE_CHUNKS } from "./app.js";

test("supported citation passes", () => {
  const report = checkCitations("The Pro plan costs $8 per month [billing.md#1].", SAMPLE_CHUNKS);
  assert.equal(report.all_supported, true);
});
test("unsupported claim is flagged", () => {
  const report = checkCitations("The Pro plan includes unlimited video calls [billing.md#1].", SAMPLE_CHUNKS);
  assert.equal(report.all_supported, false);
});
test("unknown chunk id is flagged", () => {
  const report = checkCitations("This is backed by data [made-up.md#9].", SAMPLE_CHUNKS);
  assert.equal(report.results[0].status, "unknown_chunk");
});
test("no citations means trivially all supported", () => {
  assert.equal(checkCitations("No citations here.", SAMPLE_CHUNKS).all_supported, true);
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().accuracy, 1);
});
