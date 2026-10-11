import unittest

from systems.faq_router.app import route


class FaqRouterTests(unittest.TestCase):
    def test_greeting(self):
        self.assertEqual(route("Hi there, how are you?"), "greeting")

    def test_cancel_request(self):
        self.assertEqual(route("I want to cancel my subscription"), "cancel_request")

    def test_technical_issue(self):
        self.assertEqual(route("The app keeps crashing and showing an error"), "technical_issue")

    def test_unknown_falls_back(self):
        self.assertEqual(route("asdkj qwleoi zzxcv"), "unknown")


if __name__ == "__main__":
    unittest.main()
