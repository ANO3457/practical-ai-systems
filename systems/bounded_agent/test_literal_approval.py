import unittest
from systems.bounded_agent.app import BoundedAgent
class ApprovalTests(unittest.TestCase):
 def test_truthy_values_never_authorize_tool(self):
  calls=[]
  agent=BoundedAgent({'sensitive':lambda: calls.append('called')},{'sensitive'},{'sensitive'})
  plan=agent.plan({'action':'sensitive'})
  for value in ['false','true',1,[],{},None,False]:
   with self.subTest(value=value):
    self.assertEqual(agent.run(plan,approved=value)['status'],'awaiting_approval')
  self.assertEqual(calls,[])
  self.assertEqual(agent.run(plan,approved=True)['status'],'completed')
  self.assertEqual(calls,['called'])
