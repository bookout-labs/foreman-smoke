import unittest

import greet as greet_module


def greet_all(*args, **kwargs):
    # Looked up at call time so each test fails on its own if greet_all is missing.
    return greet_module.greet_all(*args, **kwargs)


class GreetAllTest(unittest.TestCase):
    def assertRaisesMessage(self, message, *args, **kwargs):
        with self.assertRaises(ValueError) as error:
            greet_all(*args, **kwargs)
        self.assertEqual(str(error.exception), message)

    def test_greets_each_name_joined_by_pipe(self):
        self.assertEqual(greet_all(["Ada", "Bo"]), "Hello, Ada. | Hello, Bo.")
        self.assertEqual(greet_all(["Ada"]), "Hello, Ada.")

    def test_greets_with_positional_or_keyword_punctuation(self):
        self.assertEqual(greet_all(["Ada", "Bo"], "!"), "Hello, Ada! | Hello, Bo!")
        self.assertEqual(
            greet_all(["Ada", "Bo"], punctuation="!"), "Hello, Ada! | Hello, Bo!"
        )
        self.assertEqual(greet_all(["Ada"], punctuation="?"), "Hello, Ada?")

    def test_keeps_order_and_trims_each_name(self):
        self.assertEqual(greet_all(["Bo", "  Ada  "]), "Hello, Bo. | Hello, Ada.")
        self.assertEqual(
            greet_all(["Cy", "Ada", "Bo"]), "Hello, Cy. | Hello, Ada. | Hello, Bo."
        )

    def test_rejects_empty_names_list_before_punctuation(self):
        self.assertRaisesMessage("names must not be empty", [])
        self.assertRaisesMessage("names must not be empty", [], "x")
        self.assertRaisesMessage("names must not be empty", [], punctuation="x")

    def test_reports_first_invalid_name_with_position(self):
        for names, message in (
            (["Ada", "R2D2"], "name 2: name must not contain digits"),
            (["R2D2", "a|b"], "name 1: name must not contain digits"),
            (["Ada", "   "], "name 2: name must not be empty"),
        ):
            with self.subTest(names=names):
                self.assertRaisesMessage(message, names)

    def test_rejects_invalid_punctuation_without_position_prefix(self):
        self.assertRaisesMessage("punctuation must be one of . ! ?", ["Ada", "Bo"], "x")
        self.assertRaisesMessage(
            "punctuation must be one of . ! ?", ["Ada", "Bo"], punctuation="x"
        )

    def test_name_error_takes_precedence_over_punctuation_error(self):
        for names, message in (
            (["R2D2"], "name 1: name must not contain digits"),
            (["Ada", "R2D2"], "name 2: name must not contain digits"),
        ):
            with self.subTest(names=names):
                self.assertRaisesMessage(message, names, "x")


if __name__ == "__main__":
    unittest.main()
