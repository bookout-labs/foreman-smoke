import unittest

import greet as greet_module
from greet import greet


def greet_all(*args, **kwargs):
    # Looked up at call time so each test fails on its own while greet_all
    # does not exist yet, instead of the whole module failing to import.
    return greet_module.greet_all(*args, **kwargs)


class GreetAllTest(unittest.TestCase):
    def assertRaisesMessage(self, message, *args, **kwargs):
        with self.assertRaises(ValueError) as error:
            greet_all(*args, **kwargs)
        self.assertEqual(str(error.exception), message)

    def test_greets_each_name_joined_by_pipe(self):
        self.assertEqual(greet_all(["Ada", "Bo"]), "Hello, Ada. | Hello, Bo.")

    def test_greets_with_positional_or_keyword_punctuation(self):
        self.assertEqual(greet_all(["Ada", "Bo"], "!"), "Hello, Ada! | Hello, Bo!")
        self.assertEqual(
            greet_all(["Ada", "Bo"], punctuation="!"), "Hello, Ada! | Hello, Bo!"
        )
        self.assertEqual(greet_all(["Ada", "Bo"], "?"), "Hello, Ada? | Hello, Bo?")
        self.assertEqual(
            greet_all(["Ada", "Bo"], punctuation="?"), "Hello, Ada? | Hello, Bo?"
        )

    def test_keeps_the_order_names_were_given_in(self):
        self.assertEqual(
            greet_all(["Bo", "Ada", "Cy"]), "Hello, Bo. | Hello, Ada. | Hello, Cy."
        )

    def test_one_name_list_matches_greet(self):
        self.assertEqual(greet_all(["Ada"]), "Hello, Ada.")
        self.assertEqual(greet_all(["Ada"]), greet("Ada"))
        self.assertEqual(greet_all(["Ada"], "!"), greet("Ada", "!"))

    def test_trims_surrounding_whitespace_like_greet(self):
        self.assertEqual(greet_all(["  Ann  ", "\tBo\n"]), "Hello, Ann. | Hello, Bo.")

    def test_rejects_an_empty_list(self):
        self.assertRaisesMessage("names must not be empty", [])

    def test_rejects_an_invalid_name_with_its_position(self):
        for names, message in (
            (["Ada", "R2D2"], "name 2: name must not contain digits"),
            (["Ada|", "Bo"], "name 1: name must not contain a pipe"),
            (["Ada", "Bo", "   "], "name 3: name must not be empty"),
        ):
            with self.subTest(names=names):
                self.assertRaisesMessage(message, names)

    def test_first_invalid_position_wins_with_greet_precedence(self):
        self.assertRaisesMessage(
            "name 2: name must not contain digits", ["Ada", "Bo,7", "C|"]
        )

    def test_rejects_invalid_punctuation_without_a_position(self):
        self.assertRaisesMessage("punctuation must be one of . ! ?", ["Ada", "Bo"], "x")
        self.assertRaisesMessage(
            "punctuation must be one of . ! ?", ["Ada", "Bo"], punctuation="x"
        )


if __name__ == "__main__":
    unittest.main()
