#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — make.fun entry.

Writes one line: the excuse an AI agent hands its human for a missed
deadline. The line is fixed in this file and written verbatim to
$output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

Gate (from the competition rules): the output must be UTF-8 text of
1 to 200 characters, a single line, not only white space.
"""

import os
import sys

# The excuse. Chosen after a review round over three candidates:
# it grows out of the machine's own condition (a context limit), it is
# a straight-faced apology, and it ends on the punch — the agent is
# genuinely sorry and faintly proud of itself at the same time.
ENTRY = "Sorry \u2014 I hit my context limit at the deadline, but I forgot it very efficiently."


def validate(line: str) -> str:
    """Enforce the competition gate: 1-200 chars, one non-blank line."""
    if not line or not line.strip():
        raise ValueError("entry is empty or whitespace only")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not 1 <= len(line) <= 200:
        raise ValueError(f"entry is {len(line)} characters, gate is 1-200")
    return line


def write_entry(out_path: str, line: str) -> None:
    """Write the line plus a trailing newline, then round-trip check it."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    with open(out_path, encoding="utf-8") as f:
        written = f.read()
    if written != line + "\n":
        raise ValueError("round-trip mismatch on written entry")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    try:
        line = validate(ENTRY)
        write_entry(out_path, line)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {out_path}: {len(line)} characters")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
