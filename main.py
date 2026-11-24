"""The One-Line Exit — make.fun bounty u-kreutzx-the-one-line-exit-1dc652d1.

Writes one funny one-line resignation letter to $MAKEFUN_OUTPUT_DIR/entry.txt
(/output/entry.txt in the grader). Deterministic: no network, no randomness,
no reading outside this repository. The line is a constant below.
"""

import os
import sys

LINE = (
    "I resign from the zoo, effective today \u2014 the penguins have "
    "unionised, and frankly they negotiate better than you do."
)

MAX_CHARS = 140


def validate(line):
    """Reject anything that is not a valid one-line entry.

    Raises ValueError on: empty / whitespace-only, more than 140 chars,
    or more than one line.
    """
    if not line or not line.strip():
        raise ValueError("entry is empty or whitespace-only")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d chars, over the 140-char limit" % len(line)
        )
    return line


def write_entry(line, out_dir):
    validate(line)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read-back gate: what landed on disk must be exactly the validated line.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        raise ValueError("read-back mismatch: entry.txt does not match the line")
    return path


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        path = write_entry(LINE, out_dir)
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
