#!/usr/bin/env python3
"""Append a 'no template fit' entry to the deck-builder miss log.

When slide planning has to reshape, drop, or split content because no template
slide fit its shape — the "no template fits" ladder in SKILL.md step 3, or a
dense slide trimmed under a cap — record it here. The log turns one-off coverage
gaps into data: when the same shape recurs, it has earned a new transplanted
template (see references/extending_library.md).

The log lives in the user's workspace folder (the installed skill can't write to
itself), so it persists across sessions for periodic review.

Usage:
    python log_miss.py --shape "two-channel battlecard + 3-stat proof row + pills" \
        --deck "OUAI search pitch" --used "battlecard (46); dropped the pill sets" \
        [--log "/path/to/workspace/_miss_log.md"]

If --log is omitted it writes ./_miss_log.md. In a Cowork build (where you build
on /tmp), pass the workspace path explicitly so the log persists for the user.
"""

import argparse
import datetime
from pathlib import Path

HEADER = (
    "# Deck-builder miss log\n\n"
    "Content shapes that had no fitting template slide, and what was done instead. "
    "Review periodically — when a shape recurs, transplant a matching template "
    "(see `references/extending_library.md`); judge candidates by SHAPE, not topic.\n\n"
    "| Date | Deck | Shape with no home | Fell back to / dropped |\n"
    "|------|------|--------------------|------------------------|\n"
)


def esc(s):
    return (s or "").replace("|", "/").replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser(description="Log a 'no template fit' coverage gap.")
    ap.add_argument("--shape", required=True,
                    help="the content shape that had no fitting template slide")
    ap.add_argument("--deck", default="", help="deck name / context")
    ap.add_argument("--used", default="",
                    help="what you fell back to, trimmed, or dropped")
    ap.add_argument("--log", default="_miss_log.md", help="log file path")
    a = ap.parse_args()

    p = Path(a.log)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(HEADER, encoding="utf-8")
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"| {datetime.date.today().isoformat()} | {esc(a.deck)} | "
                f"{esc(a.shape)} | {esc(a.used)} |\n")
    print(f"Logged miss → {p}")


if __name__ == "__main__":
    main()
