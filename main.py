#!/usr/bin/env python3
"""Write one funny line to entry.txt.

The program holds a single joke line about modern life and writes it to
``entry.txt`` inside the output directory given by the ``MAKEFUN_OUTPUT_DIR``
environment variable (``/output`` when unset). Before writing, it validates
the line against the entry rules: exactly one line, at most 200 characters,
no trailing whitespace, and ending with proper punctuation. It prints the
SHA-256 of the written file so two runs can be compared byte for byte.

Standard library only. No network access. No reads outside the repo.
"""

import hashlib
import os
import sys

LINE = (
    "My password manager reminded me to change the password "
    "I only know because my password manager knows it."
)

MAX_CHARS = 200


def validate(line: str) -> None:
    """Check the line against the entry rules; raise ValueError if it fails."""
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, over the {MAX_CHARS} limit")
    if not line:
        raise ValueError("line must not be empty")
    if line != line.rstrip():
        raise ValueError("line must not have trailing whitespace")
    if line != line.lstrip():
        raise ValueError("line must not have leading whitespace")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line must not contain control characters")
    if line[-1] not in ".!?":
        raise ValueError("line must end with proper punctuation")


def main() -> int:
    validate(LINE)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    with open(path, "rb") as f:
        data = f.read()
    # Round-trip check: what landed on disk must be exactly the validated line.
    if data != (LINE + "\n").encode("utf-8"):
        raise ValueError("written file does not match the validated line")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {path} ({len(LINE)} chars)")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
