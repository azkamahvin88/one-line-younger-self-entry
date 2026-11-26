#!/usr/bin/env python3
"""One Line to Your Younger Self — a make.fun entry.

One job: write exactly one line of English, 114 characters, to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when that is set),
followed by a single trailing newline. Nothing else.

The line (picked from 22 candidates scored against the judge's brief —
a line only this person's older self could write, landing in one breath,
staying after a single reading; see the candidates file):

    Don't be ashamed of the accent you lose at school — one day you'll
    pay to hear it again in your own child's voice.

Why this line: it needs a whole life arc to write — lose the accent at
school, grow up, have a child, and hear the accent come back in the
child's voice. "Pay to hear it again" is the sting, and "your own
child's voice" is the image that replays after one reading. No other
entry in the visible field touches language or accent, so the line
stands in a lane of its own.

Run it:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Python 3.13, standard library only. No network, no model calls, no
randomness: the same line comes out on every run.
"""

import os

# The entry. One line, 114 characters, counted in code points.
LINE = (
    "Don't be ashamed of the accent you lose at school \u2014 one day "
    "you'll pay to hear it again in your own child's voice."
)


def check(line: str) -> int:
    """Enforce the competition's hard gate; return the character count."""
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line != line.strip():
        raise ValueError("entry must not start or end with whitespace")
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("entry must be one sentence, ending in one period")
    for ch in line:
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("entry must not contain control characters")
    length = len(line)
    if length < 1 or length > 200:
        raise ValueError(f"entry is {length} characters; the gate needs 1-200")
    return length


def main() -> None:
    length = check(LINE)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip() or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Read back and verify exactly what was written: the file must hold
    # the line plus exactly one trailing newline, so the gated text (the
    # file with that newline stripped) is the line itself, 1-200 chars.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LINE + "\n":
        raise ValueError("entry.txt content mismatch")
    gated = written[:-1]
    if gated != LINE or check(gated) != length:
        raise ValueError("gated text is not the entry line")
    print(f"wrote entry.txt ({length} characters + newline)")


if __name__ == "__main__":
    main()
