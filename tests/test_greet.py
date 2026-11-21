import unittest

from greet import greet


class GreetTest(unittest.TestCase):
    def test_greets_by_name(self):
        self.assertEqual(greet("Ada"), "Hello, Ada.")
        self.assertEqual(greet("Jean-Luc", "?"), "Hello, Jean-Luc?")
        self.assertEqual(greet("Ada Lovelace"), "Hello, Ada Lovelace.")
        self.assertEqual(greet("Ada-Lovelace"), "Hello, Ada-Lovelace.")

    def test_greets_with_surrounding_whitespace_removed(self):
        for name, expected in (
            ("  Ann  ", "Hello, Ann."),
            ("\tBo\n", "Hello, Bo."),
            ("Ann", "Hello, Ann."),
        ):
            with self.subTest(name=name):
                self.assertEqual(greet(name), expected)

    def test_rejects_names_containing_ascii_digits(self):
        cases = [("R2D2", "."), ("Ada 2", "!"), ("Ada3", ","), ("Ada@2", ".")]
        cases.extend((f"Ada{digit}", ".") for digit in "0123456789")
        for name, mark in cases:
            with self.subTest(name=name, punctuation=mark):
                with self.assertRaises(ValueError) as error:
                    greet(name, mark)
                self.assertEqual(str(error.exception), "name must not contain digits")

    def test_rejects_names_containing_at_sign(self):
        for name, mark in (("ada@home", "."), ("@Ada", "!"), ("Ada@", ",")):
            with self.subTest(name=name, punctuation=mark):
                with self.assertRaises(ValueError) as error:
                    greet(name, mark)
                self.assertEqual(str(error.exception), "name must not contain @")

    def test_rejects_names_containing_commas_with_validation_precedence(self):
        for name, mark, message in (
            ("Ada,Bob", ".", "name must not contain a comma"),
            (",Ada", "!", "name must not contain a comma"),
            ("Ada,", ";", "name must not contain a comma"),
            ("Ada,@", ".", "name must not contain @"),
            ("Ada,7", ".", "name must not contain digits"),
            ("," * 21, ".", "name must be at most 20 characters"),
        ):
            with self.subTest(name=name, punctuation=mark):
                with self.assertRaises(ValueError) as error:
                    greet(name, mark)
                self.assertEqual(str(error.exception), message)

    def test_rejects_tabs_or_newlines_with_validation_precedence(self):
        for name, mark, expected in (
            ("\tAda", ".", "Hello, Ada."),
            ("Ada\n", "!", "Hello, Ada!"),
        ):
            with self.subTest(name=name, punctuation=mark):
                self.assertEqual(greet(name, mark), expected)

        for name, mark, message in (
            ("Ada\tLovelace", ".", "name must not contain a tab or newline"),
            ("Ada\nLovelace", "!", "name must not contain a tab or newline"),
            ("Ada\n", ";", "punctuation must be one of . ! ?"),
            ("Ada,\t", ".", "name must not contain a comma"),
            ("Ada\t7", ".", "name must not contain digits"),
            ("Ada@\n", ".", "name must not contain @"),
            ("A" * 20 + "\t", ".", "name must be at most 20 characters"),
            ("\t\n", ".", "name must not be empty"),
        ):
            with self.subTest(name=name, punctuation=mark):
                with self.assertRaises(ValueError) as error:
                    greet(name, mark)
                self.assertEqual(str(error.exception), message)

    def test_rejects_semicolons_with_validation_precedence(self):
        for name, mark, message in (
            ("Ada;Lovelace", ".", "name must not contain a semicolon"),
            (";Ada", "!", "name must not contain a semicolon"),
            ("Ada;", "x", "name must not contain a semicolon"),
            ("Ada;\t", ".", "name must not contain a semicolon"),
            ("Ada;\n", ".", "name must not contain a semicolon"),
            ("Ada\t;", ".", "name must not contain a tab or newline"),
            ("Ada\n;", ".", "name must not contain a tab or newline"),
            ("Ada,;", ".", "name must not contain a comma"),
            ("Ada;7", ".", "name must not contain digits"),
            ("Ada;@", ".", "name must not contain @"),
            (";" * 21, ".", "name must be at most 20 characters"),
        ):
            with self.subTest(name=name, punctuation=mark):
                with self.assertRaises(ValueError) as error:
                    greet(name, mark)
                self.assertEqual(str(error.exception), message)

    def test_rejects_slashes_with_validation_precedence(self):
        for name, mark, message in (
            ("Ada/Lovelace", ".", "name must not contain a slash"),
            ("/Ada", "!", "name must not contain a slash"),
            ("Ada/", "x", "name must not contain a slash"),
            ("Ada;/", ".", "name must not contain a semicolon"),
            ("Ada,/", ".", "name must not contain a comma"),
            ("Ada/7", ".", "name must not contain digits"),
            ("Ada/@", ".", "name must not contain @"),
            ("Ada/\t", ".", "name must not contain a slash"),
            ("Ada/\n", ".", "name must not contain a slash"),
            ("Ada\t/", ".", "name must not contain a tab or newline"),
            ("Ada\n/", ".", "name must not contain a tab or newline"),
            ("/" * 21, ".", "name must be at most 20 characters"),
        ):
            with self.subTest(name=name, punctuation=mark):
                with self.assertRaises(ValueError) as error:
                    greet(name, mark)
                self.assertEqual(str(error.exception), message)

    def test_rejects_hashes_with_validation_precedence(self):
        for name, mark, message in (
            ("Ada#Lovelace", ".", "name must not contain a hash"),
            ("#Ada", "!", "name must not contain a hash"),
            ("Ada#", "x", "name must not contain a hash"),
            ("Ada/#", ".", "name must not contain a slash"),
            ("Ada@#", ".", "name must not contain @"),
            ("Ada#7", ".", "name must not contain digits"),
            ("Ada,#", ".", "name must not contain a comma"),
            ("Ada\t#", ".", "name must not contain a tab or newline"),
            ("Ada\n#", ".", "name must not contain a tab or newline"),
            ("Ada;#", ".", "name must not contain a semicolon"),
            ("#" * 21, ".", "name must be at most 20 characters"),
        ):
            with self.subTest(name=name, punctuation=mark):
                with self.assertRaises(ValueError) as error:
                    greet(name, mark)
                self.assertEqual(str(error.exception), message)

    def test_greets_names_containing_backslashes(self):
        self.assertEqual(greet("Ada\\Lovelace"), "Hello, Ada\\Lovelace.")

    def test_greets_names_containing_non_ascii_digits(self):
        for name in ("Ada٢", "Ada２", "Ada²"):
            with self.subTest(name=name):
                self.assertEqual(greet(name), f"Hello, {name}.")

    def test_greets_names_at_length_limit(self):
        self.assertEqual(greet("A" * 20), "Hello, AAAAAAAAAAAAAAAAAAAA.")
        self.assertEqual(greet("A" * 20, "!"), "Hello, AAAAAAAAAAAAAAAAAAAA!")

    def test_rejects_names_over_length_limit_without_trimming(self):
        for name in (
            "A" * 21,
            "Bartholomew Montgomery",
            " " + "A" * 20,
            "A" * 20 + "1",
            "@" * 21,
        ):
            for mark in (".", ","):
                with self.subTest(name=name, punctuation=mark):
                    with self.assertRaises(ValueError) as error:
                        greet(name, mark)
                    self.assertEqual(
                        str(error.exception), "name must be at most 20 characters"
                    )

    def test_rejects_empty_or_whitespace_only_names(self):
        for name in ("", "   ", "\t\n", " " * 21):
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
