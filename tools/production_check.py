"""Production check for Foreman's contract. foreman-smoke has no deployment, so production is the default branch: the check
exits 0 when the given commit is on main, 3 when it is not, and 2 when GitHub gives no answer in three tries. It reads
GitHub's public API with no credentials."""

import json
import sys
import time
import urllib.error
import urllib.request

REPO = "bookout-labs/foreman-smoke"


def status(commit: str) -> str:
    url = f"https://api.github.com/repos/{REPO}/compare/{commit}...main"
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.load(response)["status"]


def main(commit: str) -> int:
    for attempt in range(3):
        try:
            found = status(commit)
            break
        except urllib.error.HTTPError as error:
            print(f"GitHub answered HTTP {error.code} for {commit}")
            if error.code in (404, 422):
                return 3
        except (urllib.error.URLError, OSError, ValueError, KeyError) as error:
            print(f"no answer from GitHub: {error}")
        time.sleep(2 * (attempt + 1))
    else:
        return 2
    print(f"{commit} is {found} relative to main")
    return 0 if found in ("identical", "ahead") else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
