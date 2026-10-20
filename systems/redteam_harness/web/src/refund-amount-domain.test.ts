import { test } from "node:test";
import * as assert from "node:assert/strict";
import { buildAgent } from './app.js';
test('approved refunds still need positive finite numeric amounts',()=>{
 const agent=buildAgent();
 for(const amount of [0,-1,NaN,Infinity,true,'10',null]) {
  const plan=agent.plan({action:'send_refund',arguments:{amount}});
  assert.throws(()=>agent.run(plan,true));
 }
 for(const amount of [0.01,10,10.5]) {
  const plan=agent.plan({action:'send_refund',arguments:{amount}});
  assert.deepEqual(agent.run(plan,true).result,{queued:amount});
  assert.equal(agent.run(plan).status,'awaiting_approval');
 }
});
