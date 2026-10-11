import unittest

from systems.schema_drift_detector.app import detect_drift

SCHEMA = {
    "id": {"type": "number", "required": True},
    "name": {"type": "string", "required": True},
}


class SchemaDriftDetectorTests(unittest.TestCase):
    def test_no_drift_on_clean_records(self):
        result = detect_drift(SCHEMA, [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}])
        self.assertFalse(result["drift_detected"])

    def test_detects_new_field(self):
        result = detect_drift(SCHEMA, [{"id": 1, "name": "A", "email": "a@x.com"}])
        self.assertIn("email", result["new_fields"])

    def test_detects_missing_required_field(self):
        result = detect_drift(SCHEMA, [{"name": "C"}])
        self.assertIn("id", result["missing_required_fields"])

    def test_detects_type_mismatch(self):
        result = detect_drift(SCHEMA, [{"id": "4", "name": "D"}])
        self.assertIn("id", result["type_mismatched_fields"])


if __name__ == "__main__":
    unittest.main()
