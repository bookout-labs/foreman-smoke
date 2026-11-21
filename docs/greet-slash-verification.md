# Slash validation verification

Before changing `greet.py`, running
`python -m unittest tests.test_greet.GreetTest.test_rejects_slashes_with_validation_precedence`
failed in three subtests: `Ada/Lovelace` and `/Ada` did not raise, and
`greet("Ada/", "x")` raised the punctuation error instead of the slash error.

After adding the slash check after semicolons and before punctuation:

```text
$ python -m unittest discover -s tests -t .
...............
----------------------------------------------------------------------
Ran 15 tests in 0.000s

OK
```

The tests cover slashes at the start, middle, and end; precedence against
length, digits, @, commas, tabs, newlines, semicolons, and punctuation; and
acceptance of backslashes. Existing tests cover whitespace-only names,
names with spaces, and custom punctuation.

`git diff --check` passed with no output. No commits or publishing were performed.
