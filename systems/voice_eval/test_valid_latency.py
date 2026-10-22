import unittest
from systems.voice_eval.app import score_turns
class ValidLatency(unittest.TestCase):
 def test_invalid_agent_measurements_are_rejected(self):
  for value in (-1,float("nan"),float("inf"),True,"20",None):
   with self.subTest(value=value), self.assertRaises(ValueError):
    score_turns([{"speaker":"agent","latency_ms":value}],[])
 def test_missing_latency_and_caller_latency_are_not_samples(self):
  result=score_turns([{"speaker":"caller","latency_ms":-1},{"speaker":"agent"}],[])
  self.assertIsNone(result["median_latency_ms"])
 def test_zero_is_a_valid_agent_measurement(self):
  self.assertEqual(score_turns([{"speaker":"agent","latency_ms":0}],[])["median_latency_ms"],0)
