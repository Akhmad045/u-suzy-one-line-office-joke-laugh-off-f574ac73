#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off: the entry program.

The joke is a single line about office life: someone who joined for the
free coffee discovers, three years on, that the overtime is free too.
The program's only job is to hand that line to the judge exactly as
written, in /output/entry.txt, and to refuse to write anything that
would fail the gate (empty, whitespace-only, over 200 characters, or
spread over more than one line).

Standard library only. Nothing is read from the network, from the
environment, or from any other file.
"""

import argparse
import pathlib
import sys

JOKE = (
    "I joined the company for the free coffee; "
    "three years later, the coffee is still free "
    "and so is my overtime."
)

MAX_CHARS = 200
OUT_PATH = pathlib.Path("/output/entry.txt")


def problems(text):
    """Return a list of gate violations for `text` (empty means it passes)."""
    found = []
    if not text:
        found.append("empty")
    elif not text.strip():
        found.append("whitespace only")
    if text != text.strip():
        found.append("leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        found.append("length %d exceeds %d" % (len(text), MAX_CHARS))
    for char in text:
        if char in "\n\r" or ord(char) < 32 or ord(char) == 127:
            found.append("contains a control character or line break")
            break
    return found


def emit(path):
    """Write JOKE to `path` after it clears the gate."""
    bad = problems(JOKE)
    if bad:
        print("refusing to write entry: " + "; ".join(bad), file=sys.stderr)
        return 1
    target = pathlib.Path(path)
    if target.parent != pathlib.Path("."):
        target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(JOKE, encoding="utf-8")
    return 0


def selftest():
    """Run JOKE and a spread of edge cases through the gate."""
    table = [
        (JOKE, True),
        ("x", True),
        ("a" * MAX_CHARS, True),
        ("", False),
        ("    ", False),
        ("a" * (MAX_CHARS + 1), False),
        ("one\ntwo", False),
        ("one\rtwo", False),
        (" lead", False),
        ("trail ", False),
        ("with\ttab", False),
    ]
    bad = 0
    for text, should_pass in table:
        if (problems(text) == []) != should_pass:
            bad += 1
            print("FAIL %r: expected %s" % (text[:24], "pass" if should_pass else "fail"))
    print(
        "self-test: %d/%d cases ok; entry is %d chars, %d bytes"
        % (len(table) - bad, len(table), len(JOKE), len(JOKE.encode("utf-8")))
    )
    return 1 if bad else 0


def build_parser():
    parser = argparse.ArgumentParser(
        description="Write the office-joke entry to entry.txt."
    )
    parser.add_argument(
        "--out",
        default=str(OUT_PATH),
        help="where to write entry.txt (default %(default)s)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="check the line against the gate instead of writing it",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.self_test:
        return selftest()
    return emit(args.out)


if __name__ == "__main__":
    raise SystemExit(main())
