import {test} from 'node:test';
import {strict as assert} from 'node:assert';
import {dispatch, KnowledgeTools} from './app.js';

test('notifications produce no response, including unknown methods', () => {
  for (const method of ['tools/list', 'notifications/cancelled', 'unknown-method']) {
    assert.deepEqual(dispatch({method}, new KnowledgeTools()), {});
  }
});

test('explicit falsy request IDs still receive responses', () => {
  for (const id of [0, '', null]) {
    const response = dispatch({method: 'tools/list', id}, new KnowledgeTools());
    assert.equal(response.id, id);
    assert.ok(response.result);
  }
});

test('a tool notification executes the actual read-only tool', () => {
  class ObservedTools extends KnowledgeTools {
    calls = 0;
    override search(query: string, limit = 3) {
      this.calls++;
      return super.search(query, limit);
    }
  }
  const tools = new ObservedTools();
  const response = dispatch({method: 'tools/call', params: {name: 'search_docs', arguments: {query: 'reset password'}}}, tools);
  assert.equal(tools.calls, 1);
  assert.deepEqual(response, {});
});
