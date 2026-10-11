import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, route } from "./app.js";

test("greeting", () => assert.equal(route("Hi there, how are you?"), "greeting"));
test("cancel request", () => assert.equal(route("I want to cancel my subscription"), "cancel_request"));
test("technical issue", () => assert.equal(route("The app keeps crashing and showing an error"), "technical_issue"));
test("unknown falls back", () => assert.equal(route("asdkj qwleoi zzxcv"), "unknown"));
test("evaluation is perfect on the bundled fixtures", () => assert.equal(evaluateAll().routing_accuracy, 1));
