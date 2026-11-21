import unittest

from greet import greet


class GreetTest(unittest.TestCase):
    def test_greets_by_name(self):
        self.assertEqual(greet("Ada"), "Hello, Ada.")

    def test_rejects_empty_or_whitespace_only_names(self):
        for name in ("", "   ", "\t\n"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as error:
                    greet(name)
                self.assertEqual(str(error.exception), "name must not be empty")

    def test_greets_with_positional_or_keyword_punctuation(self):
        for mark, expected in (
            (".", "Hello, Ada."),
            ("!", "Hello, Ada!"),
            ("?", "Hello, Ada?"),
        ):
            with self.subTest(punctuation=mark):
                self.assertEqual(greet("Ada", mark), expected)
                self.assertEqual(greet("Ada", punctuation=mark), expected)

    def test_rejects_invalid_punctuation(self):
        for mark in (",", "", "!!", " ", None, []):
            with self.subTest(punctuation=mark):
                with self.assertRaises(ValueError) as error:
                    greet("Ada", punctuation=mark)
                self.assertEqual(str(error.exception), "punctuation must be one of . ! ?")

    def test_rejects_empty_names_with_custom_punctuation(self):
        for name in ("", "   ", "\t\n"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as error:
                    greet(name, "!")
                self.assertEqual(str(error.exception), "name must not be empty")


if __name__ == "__main__":
    unittest.main()
