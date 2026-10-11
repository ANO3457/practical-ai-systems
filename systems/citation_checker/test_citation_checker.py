import unittest

from systems.citation_checker.app import check_citations

CHUNKS = {
    "billing.md#1": "The Pro plan costs 8 dollars per user per month.",
    "sync.md#1": "Notes sync automatically every 60 seconds while online.",
}


class CitationCheckerTests(unittest.TestCase):
    def test_supported_citation(self):
        report = check_citations("The Pro plan costs 8 dollars per month [billing.md#1].", CHUNKS)
        self.assertEqual(report["results"][0]["status"], "supported")

    def test_fabricated_claim_is_unsupported(self):
        report = check_citations("Refunds are available within 90 days [billing.md#1].", CHUNKS)
        self.assertEqual(report["results"][0]["status"], "unsupported")

    def test_unknown_chunk_id_is_flagged(self):
        report = check_citations("Exports support CSV format [sharing.md#5].", CHUNKS)
        self.assertEqual(report["results"][0]["status"], "unknown_chunk")

    def test_answer_without_citations_is_vacuously_all_supported(self):
        report = check_citations("No citations here.", CHUNKS)
        self.assertEqual(report["citations"], 0)
        self.assertTrue(report["all_supported"])


if __name__ == "__main__":
    unittest.main()
