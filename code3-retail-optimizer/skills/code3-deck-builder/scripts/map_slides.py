#!/usr/bin/env python3
"""Print the position -> slide-file -> title map for an unpacked deck.

CRITICAL: SLIDE_INDEX.md positions (and slide_patterns.md "slide N" references)
are PRESENTATION ORDER. They do NOT equal the slideN.xml filename -- the files
are non-contiguous and scrambled (position 1 = slide5.xml, position 8 =
slide17.xml, position 31 = slide56.xml, ...). Editing "slideN.xml" because the
index says "slide N" will edit the WRONG slide. Run this right after new_deck.py
to get the real mapping, and edit content files by the filename it prints.

Usage:
    python map_slides.py UNPACKED_DIR
e.g. python map_slides.py /tmp/mydeck/mydeck_unpacked
"""

import re
import sys


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    base = sys.argv[1].rstrip("/")

    try:
        pres = open(f"{base}/ppt/presentation.xml").read()
        rels = open(f"{base}/ppt/_rels/presentation.xml.rels").read()
    except FileNotFoundError as e:
        print(f"ERROR: not an unpacked deck dir ({e}). Pass the *_unpacked dir.")
        sys.exit(1)

    rid2f = dict(
        re.findall(r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"', rels)
    )
    order = re.findall(r'<p:sldId[^>]*r:id="(rId\d+)"', pres)

    print(f"{'pos':>3} | {'file':14s} | first text run")
    print("-" * 66)
    for i, rid in enumerate(order, 1):
        f = rid2f.get(rid, "?")
        title = "(no text)"
        try:
            s = open(f"{base}/ppt/slides/{f}").read()
            ts = [re.sub("<[^>]+>", "", t)
                  for t in re.findall(r"<a:t\b[^>]*>(.*?)</a:t>", s, re.DOTALL)]
            ts = [t.strip() for t in ts if t.strip()]
            if ts:
                title = ts[0][:46]
        except FileNotFoundError:
            title = "(file missing)"
        print(f"{i:3d} | {f:14s} | {title}")
    print(f"\n{len(order)} slides in presentation order. "
          "SLIDE_INDEX position N = row N above; edit the file in that row.")


if __name__ == "__main__":
    main()
