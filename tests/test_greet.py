import unittest

from greet import greet


class GreetTest(unittest.TestCase):
    def test_greets_by_name(self):
        self.assertEqual(greet("Ada"), "Hello, Ada.")

    def test_greets_with_positional_greeting(self):
        self.assertEqual(greet("Ada", "Hi"), "Hi, Ada.")

    def test_greets_with_keyword_greeting(self):
        self.assertEqual(greet("Ada", greeting="Good morning"), "Good morning, Ada.")


if __name__ == "__main__":
    unittest.main()
