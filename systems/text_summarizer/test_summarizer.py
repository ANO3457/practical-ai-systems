import unittest

from systems.text_summarizer.app import compression_ratio, summarize


class SummarizerTests(unittest.TestCase):
    def test_short_text_returned_unchanged(self):
        self.assertEqual(summarize("One sentence only."), ["One sentence only."])

    def test_picks_sentence_with_frequent_terms(self):
        text = (
            "Database indexing speeds up queries. "
            "Indexing indexing indexing is crucial for performance. "
            "The weather was nice yesterday."
        )
        summary = summarize(text, n=1)
        self.assertIn("indexing", summary[0].lower())

    def test_compression_ratio_is_fraction_of_original(self):
        text = "Short sentence one. Short sentence two. Short sentence three."
        summary = summarize(text, n=1)
        ratio = compression_ratio(text, summary)
        self.assertGreater(ratio, 0)
        self.assertLess(ratio, 1)

    def test_empty_text_has_zero_ratio(self):
        self.assertEqual(compression_ratio("", []), 0.0)


if __name__ == "__main__":
    unittest.main()
