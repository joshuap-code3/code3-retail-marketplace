#!/usr/bin/env python3
"""Position-aware text replacement for PPTX slide XML (refresh mode).

Why this exists
---------------
Refreshing a deck means swapping many cell values inside tables and stat grids.
The naive approach -- `txt.replace(find, repl, 1)` once per substitution --
silently corrupts tables when a value repeats (e.g. several "$0K" or "0%"
cells): an earlier replacement creates a string that a later first-match then
matches against, so the wrong cell changes. This walks every <a:t> text run in
document order and edits by POSITION (absolute index, or the Nth occurrence of
a value), so repeating values are disambiguated.

Use this for any table or stat grid with repeating values. One-off prose slots
(titles, eyebrows) can still use the Edit tool.

Usage
-----
1) List every text run in document order, with its index (do this FIRST, and
   again immediately before building index-based edits -- any Edit that adds or
   removes an <a:t> run shifts the indices):

       python refresh_text.py SLIDE_XML --list

2) Apply edits from a JSON file. Always pass --backup; see the note below:

       python refresh_text.py SLIDE_XML EDITS_JSON --backup BACKUP_PATH

   EDITS_JSON is a list of edit objects. Supported forms:

     By absolute run index (0-based, from --list):
       {"index": 47, "replace": "MENFALL26COLLECTION"}

     By ordinal occurrence of an exact cell value (1-based, counted over ALL
     runs in document order):
       {"find": "$0K", "occurrence": 2, "replace": "$53.9K"}

     By ordinal occurrence of a regex match (1-based):
       {"regex": "^March 2024$", "occurrence": 1, "replace": "April 2026"}

--backup semantics (read this)
------------------------------
`--backup BACKUP_PATH` makes runs idempotent and recoverable:
  * If BACKUP_PATH does NOT exist, the current (pristine) slide is copied to it,
    then edits are applied. (First run.)
  * If BACKUP_PATH DOES exist, the slide is first RESTORED from it, then edits
    are applied. (Re-runs apply your edits to the original, every time.)
So: keep ONE backup per slide, put ALL of that slide's edits in ONE JSON, and
re-run freely to iterate. Write BACKUP_PATH OUTSIDE the unpacked tree (e.g. a
sibling `_bak/` dir) -- a .bak left inside ppt/slides/ gets packed into the
deck as junk and can fail validation. (finalize.py also sweeps stray *.bak as a
safety net, but don't rely on it for an existing-deck refresh that packs
manually.)
"""

import json
import os
import re
import shutil
import sys

# <a:t>...</a:t> -- a DrawingML text run. Group 2 is the inner text.
# The optional (?:\s[^>]*)? tolerates attributes like <a:t xml:space="preserve">
# while NOT matching self-closing empty runs (<a:t/>). Matching those as openers
# (the old "<a:t\b[^>]*>") let the lazy .*? swallow following real runs into one
# "blob": --list mis-indexed, find/occurrence edits silently missed, and regex
# edits could overwrite real markup. Group-2 content is [^<]* so a run never
# spans into the next element.
A_T_RE = re.compile(r"(<a:t(?:\s[^>]*)?>)([^<]*)(</a:t>)")


def _unescape_xml(s):
    s = (
        s.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )
    # Numeric character references (e.g. smart quotes &#x2019; / &#8217;).
    s = re.sub(r"&#x([0-9A-Fa-f]+);", lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), s)
    return s.replace("&amp;", "&")


def _escape_xml(s):
    # Order matters: ampersand first.
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def index_runs(xml):
    """Return a list of run dicts in document order."""
    runs = []
    for m in A_T_RE.finditer(xml):
        runs.append(
            {
                "text_start": m.start(2),
                "text_end": m.end(2),
                "text": _unescape_xml(m.group(2)),
            }
        )
    return runs


def apply_edits(xml, edits):
    """Apply position-aware edits. Returns (new_xml, n_applied, misses).

    Occurrence is counted over ALL runs in document order (NOT only
    unclaimed ones), so {"find":"$0K","occurrence":2} always means the 2nd
    "$0K" cell regardless of what other edits are in the batch.
    """
    runs = index_runs(xml)
    planned = {}  # run_index -> replacement_text (escaped)
    misses = []

    for edit in edits:
        repl = edit["replace"]

        # Absolute index form.
        if "index" in edit:
            idx = edit["index"]
            if 0 <= idx < len(runs):
                planned[idx] = _escape_xml(repl)
            else:
                misses.append(edit)
            continue

        # find / regex form, resolved to an absolute index by occurrence.
        if "regex" in edit:
            pat = re.compile(edit["regex"])
            matcher = lambda t, p=pat: p.search(t) is not None
        else:
            needle = edit["find"]
            matcher = lambda t, n=needle: t == n  # exact-cell match

        want = edit.get("occurrence", 1)  # 1-based
        seen = 0
        target = None
        for i, run in enumerate(runs):  # count over ALL runs
            if matcher(run["text"]):
                seen += 1
                if seen == want:
                    target = i
                    break
        if target is None:
            misses.append(edit)
        else:
            planned[target] = _escape_xml(repl)

    # Rebuild from the end so earlier spans stay valid.
    n_applied = 0
    for i in sorted(planned.keys(), reverse=True):
        run = runs[i]
        xml = xml[: run["text_start"]] + planned[i] + xml[run["text_end"] :]
        n_applied += 1

    return xml, n_applied, misses


def list_runs(slide_path):
    with open(slide_path, "r", encoding="utf-8") as f:
        xml = f.read()
    runs = index_runs(xml)
    for i, run in enumerate(runs):
        text = run["text"]
        shown = text if text.strip() else repr(text)
        print(f"{i:4d} | {shown}")
    print(f"\n{len(runs)} text runs total.")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    slide_path = sys.argv[1]

    if sys.argv[2] == "--list":
        list_runs(slide_path)
        return

    edits_path = sys.argv[2]

    backup_path = None
    if "--backup" in sys.argv:
        backup_path = sys.argv[sys.argv.index("--backup") + 1]
        bdir = os.path.dirname(backup_path)
        if bdir:
            os.makedirs(bdir, exist_ok=True)
        if os.path.exists(backup_path):
            # Re-run: restore the pristine original, then re-apply edits.
            shutil.copyfile(backup_path, slide_path)
        else:
            # First run: save the pristine original before editing.
            shutil.copyfile(slide_path, backup_path)
        if os.path.realpath(os.path.dirname(backup_path)).rstrip("/").endswith("/slides") \
                or os.path.basename(os.path.dirname(os.path.realpath(backup_path))) == "slides":
            print("WARNING: backup is inside ppt/slides/. Move it outside the "
                  "unpacked tree or it will be packed into the deck as junk.")

    with open(slide_path, "r", encoding="utf-8") as f:
        xml = f.read()
    with open(edits_path, "r", encoding="utf-8") as f:
        edits = json.load(f)

    new_xml, n_applied, misses = apply_edits(xml, edits)

    with open(slide_path, "w", encoding="utf-8") as f:
        f.write(new_xml)

    print(f"Applied {n_applied}/{len(edits)} edits to {slide_path}")
    if misses:
        print(f"WARNING: {len(misses)} edit(s) matched no <a:t> run:")
        for m in misses:
            print("  ", json.dumps(m))
        sys.exit(2)


if __name__ == "__main__":
    main()
