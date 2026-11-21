# Issue 36 verification

- Before the implementation change, `python -m unittest tests.test_greet.GreetTest.test_rejects_percent_signs_and_greets_plain_names` failed for both `Ann%Bo` and `%` because no `ValueError` was raised.
- After the change, `python -m unittest discover -s tests -t .` passed all 17 tests. The new test checks both rejected names, the exact required error message, and `greet("Ann") == "Hello, Ann."`.
- `git diff --check` passed.

Test commands used `PYTHONDONTWRITEBYTECODE=1` to avoid creating bytecode files in the checkout.
