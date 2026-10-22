import {test} from "node:test";
import {strict as assert} from "node:assert";
import {scoreTurns, type Turn} from "./app.js";
test("rejects invalid observed agent latencies",()=>{
 for(const value of [-1,NaN,Infinity,true,"20",null]) {
  assert.throws(()=>scoreTurns([{speaker:"agent",latency_ms:value} as unknown as Turn],[]));
 }
 assert.equal(scoreTurns([{speaker:"caller",latency_ms:-1},{speaker:"agent"}],[]).median_latency_ms,null);
 assert.equal(scoreTurns([{speaker:"agent",latency_ms:0}],[]).median_latency_ms,0);
});
