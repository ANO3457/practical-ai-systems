import { test } from "node:test";
import * as assert from "node:assert/strict";
import { BoundedAgent } from './app.js';
test('only literal true authorizes a sensitive tool',()=>{
 let calls=0;
 const agent=new BoundedAgent({sensitive:()=>++calls},new Set(['sensitive']),new Set(['sensitive']));
 const plan=agent.plan({action:'sensitive'});
 for(const value of ['false','true',1,[],{},null,false]) assert.equal(agent.run(plan,value as boolean).status,'awaiting_approval');
 assert.equal(calls,0);
 assert.equal(agent.run(plan,true).status,'completed');
 assert.equal(calls,1);
});
