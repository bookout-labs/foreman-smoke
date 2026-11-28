---
name: verify-foreman-smoke
description: Verify a change to foreman-smoke, a synthetic Python fixture whose only app is a health server. Use to prove an acceptance criterion with the repository's own check and the files the change adds.
---

# Verify foreman-smoke

The repository has no sign-in or secrets. Its only app is `app.py`, which answers `GET /health` and nothing else, so a user's surface is its files and the `greet` module.

## Run the check

From the repository root, with Python 3.12:

```sh
python -m unittest discover -s tests
```

It passes when the last line is `OK` and the exit code is 0. It changes no tracked file.

## Drive a criterion

- A criterion about a file's content: read the file at the tested head with `git show HEAD:<path>` and compare its exact bytes, trailing newline included.
- A criterion about `greet`: call it with `python -c 'from greet import greet; print(repr(greet(...)))'` and compare the printed value.

## Evidence

For each criterion, record the command, its exit code and its output, and the head commit it ran at (`git rev-parse HEAD`). A criterion passes only when that output shows the expected result. A check that was not run, or output that doesn't show the criterion, leaves it unverified.

## Cleanup

Nothing to stop. `__pycache__/` is ignored. `git status --short` must be empty afterward.
