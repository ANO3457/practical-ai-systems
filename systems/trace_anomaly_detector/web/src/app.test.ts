import { test } from "node:test";
import { strict as assert } from "node:assert";
import { BASELINE, detectAnomalies, evaluateAll, TRACES } from "./app.js";

test("normal durations are not anomalous", () => {
  const results = detectAnomalies(BASELINE, [{ name: "n", duration_ms: 101 }]);
  assert.equal(results[0].anomalous, false);
});
test("far outlier duration is anomalous", () => {
  const results = detectAnomalies(BASELINE, [{ name: "n", duration_ms: 400 }]);
  assert.equal(results[0].anomalous, true);
});
test("explicit error flag is always anomalous", () => {
  const results = detectAnomalies(BASELINE, [{ name: "n", duration_ms: 100, error: true }]);
  assert.equal(results[0].anomalous, true);
});
test("detects all four bundled traces correctly", () => {
  const results = detectAnomalies(BASELINE, TRACES);
  assert.deepEqual(results.map((r) => r.anomalous), [false, false, true, true]);
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().f1, 1);
});
