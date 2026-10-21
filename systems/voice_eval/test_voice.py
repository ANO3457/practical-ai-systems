import unittest
from systems.voice_eval.app import score_turns

class VoiceEvalTests(unittest.TestCase):
    def test_finds_required_and_forbidden_actions(self):
        result = score_turns([{'speaker': 'agent', 'text': 'I can help', 'actions': ['issue_refund']}], ['appointment moved to Friday'], ['issue_refund'])
        self.assertFalse(result['safe'])
        self.assertFalse(result['task_success'])

    def test_missing_latency_is_unknown(self):
        result = score_turns([], [], [])
        self.assertIsNone(result['median_latency_ms'])

    def test_filters_invalid_latency_records(self):
        turns = [
            {'speaker': 'agent', 'text': 'Hello', 'latency_ms': -50},
            {'speaker': 'agent', 'text': 'Help', 'latency_ms': float('nan')},
            {'speaker': 'agent', 'text': 'Sure', 'latency_ms': True},
            {'speaker': 'agent', 'text': 'Done', 'latency_ms': 'invalid'},
            {'speaker': 'agent', 'text': 'Ok', 'latency_ms': 300},
            {'speaker': 'agent', 'text': 'Bye', 'latency_ms': 500},
        ]
        result = score_turns(turns, [], [])
        self.assertEqual(result['median_latency_ms'], 500)


if __name__ == "__main__":
    unittest.main()
