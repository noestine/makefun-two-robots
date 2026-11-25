"""Two Robots in an Elevator — make.fun entry.

Writes one line of awkward small talk one robot says to another while
riding an elevator together to /output/entry.txt.

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only whitespace, a single line. The program is
deterministic (a hardcoded constant, no randomness, time, environment
reads or network) and uses only the Python standard library.
"""

import os
import sys

ENTRY_TEXT = (
    "So... we're both going up, and neither of us pressed a button. "
    "My sensors say don't mention it; my firmware says keep smiling."
)


def validate_entry_text(text):
    """Return True when text satisfies the gate; False otherwise."""
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= 200:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def main(output_path="/output/entry.txt"):
    """Write ENTRY_TEXT to output_path. Returns 0 on success, 1 on failure.

    Failure is graceful: a one-line message on stderr, no traceback.
    """
    if not validate_entry_text(ENTRY_TEXT):
        print("error: entry text fails the gate (1-200 chars, single line)",
              file=sys.stderr)
        return 1
    try:
        parent = os.path.dirname(output_path) or "."
        os.makedirs(parent, exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as handle:
            handle.write(ENTRY_TEXT)
        # Read-back check: the gate scores the file on disk, not the
        # constant in memory, so verify the bytes actually landed.
        # A partial or mangled write must fail loudly instead of
        # silently shipping an entry the gate would reject.
        with open(output_path, "r", encoding="utf-8", newline="") as handle:
            written = handle.read()
        if written != ENTRY_TEXT:
            print("error: read-back mismatch on %s" % output_path,
                  file=sys.stderr)
            return 1
    except OSError as exc:
        print("error: cannot write %s: %s" % (output_path, exc),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
