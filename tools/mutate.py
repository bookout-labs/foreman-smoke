"""Mutation tool for Foreman's contract. Reads path:line entries on standard input, one per line. For each Python source line
outside tests/ it makes one mutation (an if condition negated, or a simple statement replaced by pass), runs the test suite,
restores the file and prints one JSON line {"line", "id", "result"}, where result is killed when the suite fails. The id is
the path, the mutation kind and a digest of the original line, so it stays the same across runs. Exits 0 for an empty list."""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TESTS = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"]


def mutated(text: str) -> tuple[str, str] | None:
    body = text.rstrip("\n")
    indent = body[: len(body) - len(body.lstrip())]
    statement = body.strip()
    if match := re.fullmatch(r"(el)?if (.+):", statement):
        return "negate", f"{indent}{match.group(1) or ''}if not ({match.group(2)}):\n"
    if statement and not statement.startswith("#") and not statement.endswith((":", ",", "(", "[", "{", "\\")):
        return "pass", f"{indent}pass\n"
    return None


def main() -> int:
    for entry in sys.stdin.read().split():
        path, _, number = entry.rpartition(":")
        file = Path(path)
        if file.suffix != ".py" or path.startswith("tests/") or not number.isdigit() or not file.is_file():
            continue
        original = file.read_text()
        lines = original.splitlines(keepends=True)
        index = int(number) - 1
        if not 0 <= index < len(lines) or (change := mutated(lines[index])) is None:
            continue
        kind, replacement = change
        identity = f"{path}:{kind}:{hashlib.sha256(lines[index].strip().encode()).hexdigest()[:12]}"
        try:
            file.write_text("".join(lines[:index] + [replacement] + lines[index + 1:]))
            result = subprocess.run(TESTS, capture_output=True).returncode
        finally:
            file.write_text(original)
        print(json.dumps({"line": entry, "id": identity, "result": "survived" if result == 0 else "killed"}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
