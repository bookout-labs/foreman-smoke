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


if __name__ == "__main__":
    unittest.main()
