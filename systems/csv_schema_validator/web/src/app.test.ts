import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, validateRow, validateRows, type Schema } from "./app.js";

const SCHEMA: Schema = {
  id: { type: "number", required: true },
  name: { type: "string", required: true },
  active: { type: "boolean", required: false },
};

test("valid row has no errors", () => {
  assert.deepEqual(validateRow(SCHEMA, { id: 1, name: "Alice", active: true }), []);
});
test("missing required field", () => {
  assert.ok(validateRow(SCHEMA, { name: "Carol" }).includes("missing:id"));
});
test("wrong type is flagged", () => {
  assert.ok(validateRow(SCHEMA, { id: "two", name: "Bob" }).includes("type:id"));
});
test("optional field may be absent", () => {
  assert.deepEqual(validateRow(SCHEMA, { id: 5, name: "Eve" }), []);
});
test("validate rows indexes each row", () => {
  const results = validateRows(SCHEMA, [{ id: 1, name: "Alice" }, { name: "Bob" }]);
  assert.equal(results[1].row, 1);
  assert.ok(results[1].errors.includes("missing:id"));
});
test("evaluation is perfect on the bundled fixture", () => {
  assert.equal(evaluateAll().row_validity_accuracy, 1);
});
