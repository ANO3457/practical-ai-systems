import { test } from "node:test";
import { strict as assert } from "node:assert";
import { classify, evaluateAll } from "./app.js";

test("positive words win", () => {
  assert.equal(classify("This product is great and the support team is fantastic."), "positive");
});
test("negative words win", () => {
  assert.equal(classify("The checkout process is slow and confusing."), "negative");
});
test("no lexicon words is neutral", () => {
  assert.equal(classify("It's okay, does the job."), "neutral");
});
test("tied counts default to neutral", () => {
  assert.equal(classify("I love this app but the login page is terrible."), "neutral");
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().accuracy, 1);
});
