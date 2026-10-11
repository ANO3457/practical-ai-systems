import unittest

from systems.pii_redactor.app import detect, redact


class PiiRedactorTests(unittest.TestCase):
    def test_detects_email(self):
        findings = detect("Contact jane.doe@example.com for help.")
        self.assertEqual([f["type"] for f in findings], ["email"])

    def test_redacts_matches_in_place(self):
        text = "Call (555) 123-4567 now."
        redacted = redact(text)
        self.assertNotIn("123-4567", redacted)
        self.assertIn("[REDACTED:PHONE]", redacted)

    def test_clean_text_has_no_findings(self):
        self.assertEqual(detect("No personal data here, just a meeting at 3pm."), [])

    def test_ssn_pattern_does_not_match_phone(self):
        findings = detect("SSN on file: 123-45-6789.")
        self.assertEqual([f["type"] for f in findings], ["ssn"])


if __name__ == "__main__":
    unittest.main()
