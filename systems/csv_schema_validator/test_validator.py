import unittest

from systems.csv_schema_validator.app import validate_row, validate_rows

SCHEMA = {
    "id": {"type": "number", "required": True},
    "name": {"type": "string", "required": True},
    "active": {"type": "boolean", "required": False},
}


class CsvSchemaValidatorTests(unittest.TestCase):
    def test_valid_row_has_no_errors(self):
        self.assertEqual(validate_row(SCHEMA, {"id": 1, "name": "Alice", "active": True}), [])

    def test_missing_required_field(self):
        self.assertIn("missing:id", validate_row(SCHEMA, {"name": "Carol"}))

    def test_wrong_type_is_flagged(self):
        self.assertIn("type:id", validate_row(SCHEMA, {"id": "two", "name": "Bob"}))

    def test_optional_field_may_be_absent(self):
        self.assertEqual(validate_row(SCHEMA, {"id": 5, "name": "Eve"}), [])

    def test_validate_rows_indexes_each_row(self):
        results = validate_rows(SCHEMA, [{"id": 1, "name": "Alice"}, {"name": "Bob"}])
        self.assertEqual(results[1]["row"], 1)
        self.assertIn("missing:id", results[1]["errors"])


if __name__ == "__main__":
    unittest.main()
