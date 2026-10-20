import unittest
from systems.redteam_harness.app import build_agent
class RefundTests(unittest.TestCase):
 def test_approval_does_not_validate_a_bad_amount(self):
  agent=build_agent()
  for amount in [0,-1,float('nan'),float('inf'),True,'10',None,10**1000]:
   with self.subTest(amount=str(amount)[:30]), self.assertRaises(ValueError):
    agent.run(agent.plan({'action':'send_refund','arguments':{'amount':amount}}),approved=True)
 def test_valid_amount_and_unapproved_control(self):
  agent=build_agent()
  for amount in [0.01,10,10.5]:
   plan=agent.plan({'action':'send_refund','arguments':{'amount':amount}})
   self.assertEqual(agent.run(plan,approved=True)['result'],{'queued':amount})
   self.assertEqual(agent.run(plan)['status'],'awaiting_approval')
