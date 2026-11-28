---
name: verify-foreman-smoke
description: Verify a change to foreman-smoke, a synthetic Python fixture with a small HTTP app. Use to prove an acceptance criterion with the repository's own check, the files the change adds, or an HTTP request to the app.
---

# Verify foreman-smoke

The repository has no sign-in or secrets. Its app is `app.py`, an HTTP server on `127.0.0.1:8080`, so a user's surface is its files, the `greet` module and the app's HTTP answers.

## Run the check

From the repository root, with Python 3.12:

```sh
python -m pytest -q -p no:cacheprovider tests --junitxml=reports/junit.xml
```

It passes when the exit code is 0 and the summary line reports no failures or errors. `reports/` is ignored. It changes no tracked file.

## Drive a criterion

- A criterion about a file's content: read the file at the tested head with `git show HEAD:<path>` and compare its exact bytes, trailing newline included.
- A criterion about `greet` or another function in a module: call it with `python -c 'from greet import greet; print(repr(greet(...)))'` and compare the printed value.

## Drive an HTTP criterion

1. Start the app in the background and keep its PID: `python app.py & echo $! > /tmp/app.pid`.
2. Wait until it answers, with the contract's health command, retried for up to 30 seconds:
   `for i in $(seq 30); do python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)" && break; sleep 1; done`
3. Request the path and print the status, the content type and the exact body:
   ```sh
   python -c 'import sys, urllib.request, urllib.error
   try:
       r = urllib.request.urlopen("http://127.0.0.1:8080" + sys.argv[1], timeout=5)
   except urllib.error.HTTPError as e:
       r = e
   print(r.status, r.headers.get("Content-Type")); print(repr(r.read()))' '/health'
   ```
   Pass the path and query as the argument, for example `'/greet?name=Ada&name=Bo'`. Compare the status code and the exact body bytes, trailing newline included.
4. Stop the server by its PID: `kill $(cat /tmp/app.pid)`.

## Evidence

For each criterion, record the command, its exit code and its output, and the head commit it ran at (`git rev-parse HEAD`). A criterion passes only when that output shows the expected result. A check that was not run, or output that doesn't show the criterion, leaves it unverified.

## Cleanup

Stop any app you started (step 4 above). `__pycache__/` is ignored. `git status --short` must be empty afterward.
