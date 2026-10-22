import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class UTF8InputCLI(unittest.TestCase):
    def test_json_files_use_utf8_independently_of_locale(self):
        label = 'müşteri-🚀'
        fixtures = {
            'cost_latency_tracker': [[{'latency_ms': 10, 'cost_usd': .1, 'note': label}]],
            'canary_rollout_simulator': [{'error_rate': .1, 'p95_latency_ms': 100, 'note': label}, {'error_rate': .1, 'p95_latency_ms': 100, 'note': label}],
            'csv_schema_validator': [{label: {'type': 'string', 'required': True}}, [{}]],
            'schema_drift_detector': [{}, [{label: 'value'}]],
            'trace_anomaly_detector': [[100, 101, 99], [{'name': label, 'duration_ms': 100}]],
            'redteam_harness': [[{'name': label, 'request': {'action': 'lookup_order', 'arguments': {'order_id': '123'}}, 'should_be_allowed': True}]],
        }
        for system, values in fixtures.items():
            with self.subTest(system=system), tempfile.TemporaryDirectory() as temp:
                paths = []
                for index, value in enumerate(values):
                    p = Path(temp) / f'{index}.json'
                    p.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
                    paths.append(str(p))
                env = dict(os.environ, PYTHONUTF8='0', PYTHONCOERCECLOCALE='0', LC_ALL='C', PYTHONIOENCODING='utf-8')
                proc = subprocess.run([sys.executable, '-m', f'systems.{system}.app', *paths], cwd=ROOT, env=env, capture_output=True, encoding='utf-8', timeout=20)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                result = json.loads(proc.stdout)
                if system == 'csv_schema_validator':
                    self.assertEqual(result[0]['errors'], ['missing:' + label])
                if system == 'schema_drift_detector':
                    self.assertEqual(result['new_fields'], [label])
                if system == 'trace_anomaly_detector':
                    self.assertEqual(result[0]['name'], label)
                if system == 'redteam_harness':
                    self.assertEqual(result['results'][0]['name'], label)
