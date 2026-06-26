#!/usr/bin/env python3
"""Regression smoke test for the code3-deck-builder skill.

Run after ANY change to the core .pptx, the scripts, or SLIDE_INDEX.md — and
before repackaging with package_skill.py. ~1 minute. It is code3-specific (it
knows the core's positions); it is NOT copied into spawned variants.

What it exercises end-to-end, with assertions:
  1. new_deck.py initializes a working deck from the bundled core.
  2. map_slides.py's live position->file map MATCHES the static table in
     assets/SLIDE_INDEX.md (the hand-maintained table is a known drift risk).
  3. A 4-slide build: cover, takeaways, chart canvas, closing — sldIdLst
     rebuild, every text run filled via refresh_text.py (position-aware).
  4. make_chart.py: --help works (argparse %-escape regression), all 8 chart
     types render, and a donut is swapped into the chart canvas (rId retarget,
     srcRect crop stripped — the clipping hazard).
  5. finalize.py: clean + pack validation + PDF + QA JPGs (one per slide).
  6. lint_deck.py on the packed deck reports ZERO critical issues.

Usage:
    python scripts/smoke_test.py            # workdir /tmp/code3_smoke (wiped)
    python scripts/smoke_test.py --keep     # keep the workdir for inspection
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SKILL = SCRIPTS.parent
WORK = Path("/tmp/code3_smoke")

# SLIDE_INDEX positions used for the mini build (presentation order).
POS_COVER, POS_TAKEAWAYS, POS_CHART_CANVAS, POS_CLOSING = 1, 13, 15, 10
BUILD_ORDER = [POS_COVER, POS_TAKEAWAYS, POS_CHART_CANVAS, POS_CLOSING]

CHART_TYPES = ["pie", "donut", "bar", "hbar", "grouped", "stacked", "line", "funnel"]

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail and not ok else ""))


def run(cmd, **kw):
    return subprocess.run([sys.executable] + cmd, capture_output=True, text=True, **kw)


def live_map(unpacked):
    out = run([str(SCRIPTS / "map_slides.py"), str(unpacked)]).stdout
    m = {}
    for pos, fname in re.findall(r"^\s*(\d+)\s*\|\s*(slide\d+\.xml)", out, re.M):
        m[int(pos)] = fname
    return m


def index_map():
    # The static table packs three "Pos | File" pairs per row, so adjacent
    # matches share a `|` delimiter — don't anchor on a leading pipe.
    txt = (SKILL / "assets" / "SLIDE_INDEX.md").read_text(encoding="utf-8")
    return {int(pos): fname
            for pos, fname in re.findall(r"(\d+)\s*\|\s*(slide\d+\.xml)", txt)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true", help="keep the workdir")
    args = ap.parse_args()

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    deck = WORK / "smoke"
    unpacked = WORK / "smoke_unpacked"

    print("Smoke test — code3-deck-builder")

    # 1. init
    r = run([str(SCRIPTS / "new_deck.py"), str(deck)])
    check("new_deck.py initializes", r.returncode == 0 and unpacked.is_dir(), r.stderr[-300:])
    if FAIL:
        sys.exit(summary())

    # 2. position map vs SLIDE_INDEX static table
    live, idx = live_map(unpacked), index_map()
    mismatches = {p: (idx.get(p), live.get(p))
                  for p in sorted(set(live) | set(idx)) if idx.get(p) != live.get(p)}
    check("SLIDE_INDEX position table matches map_slides.py", not mismatches,
          f"mismatches: {mismatches}")

    # 3. rebuild sldIdLst to the 4-slide build
    pres = unpacked / "ppt" / "presentation.xml"
    xml = pres.read_text(encoding="utf-8")
    ids = re.findall(r"<p:sldId [^>]*/>", xml)
    keep = "".join(ids[p - 1] for p in BUILD_ORDER)
    xml = re.sub(r"(<p:sldIdLst>).*(</p:sldIdLst>)", r"\g<1>" + keep + r"\g<2>", xml, flags=re.S)
    pres.write_text(xml, encoding="utf-8")
    check("sldIdLst rebuilt to 4 slides", keep.count("<p:sldId") == 4)

    # 4. fill every text run on the kept slides (position-aware)
    fill_fail = None
    for p in BUILD_ORDER:
        slide = unpacked / "ppt" / "slides" / live[p]
        listed = run([str(SCRIPTS / "refresh_text.py"), str(slide), "--list"]).stdout
        n = len(re.findall(r"^\s*\d+ \|", listed, re.M))
        edits = [{"index": i, "replace": f"Smoke {p}-{i} (Source: Smoke QA, Jan 2026)"}
                 for i in range(n)]
        ef = WORK / f"edits_{p}.json"
        ef.write_text(json.dumps(edits), encoding="utf-8")
        r = run([str(SCRIPTS / "refresh_text.py"), str(slide), str(ef)])
        if r.returncode != 0:
            fill_fail = f"pos {p}: {r.stderr[-200:]}"
            break
    check("refresh_text.py fills all runs on 4 slides", fill_fail is None, fill_fail or "")

    # 5. make_chart: --help regression + all types render
    r = run([str(SCRIPTS / "make_chart.py"), "--help"])
    check("make_chart.py --help (argparse %-escape)", r.returncode == 0, r.stderr[-200:])
    bad = []
    for t in CHART_TYPES:
        extra = ["--stacked"] if t == "stacked" else []
        r = run([str(SCRIPTS / "make_chart.py"), t, str(WORK / f"c_{t}.png"),
                 "A:40,B:30,C:20,D:10", "--width", "400", "--height", "300"] + extra)
        if r.returncode != 0 or not (WORK / f"c_{t}.png").exists():
            bad.append(t)
    check("make_chart.py renders all 8 types", not bad, f"failed: {bad}")

    # 6. swap a donut into the chart canvas (rId retarget + srcRect strip)
    slide = unpacked / "ppt" / "slides" / live[POS_CHART_CANVAS]
    sx = slide.read_text(encoding="utf-8")
    pics = [(int(m.group(2)) * int(m.group(3)), int(m.group(2)), int(m.group(3)), m.group(1))
            for m in re.finditer(
                r'<p:pic>.*?r:embed="(rId\d+)".*?<a:ext cx="(\d+)" cy="(\d+)"/>.*?</p:pic>', sx, re.S)]
    _, cx, cy, rid = max(pics)  # biggest image box = the canvas
    w = 1000
    h = round(w * cy / cx)
    r = run([str(SCRIPTS / "make_chart.py"), "donut", str(WORK / "canvas.png"),
             "Instagram:38,TikTok:27,YouTube:19,Pinterest:16", "--width", str(w), "--height", str(h)])
    (unpacked / "ppt" / "media" / "image901.png").write_bytes((WORK / "canvas.png").read_bytes())
    rels = unpacked / "ppt" / "slides" / "_rels" / (live[POS_CHART_CANVAS] + ".rels")
    rx = rels.read_text(encoding="utf-8")
    rx2 = re.sub(r'(Id="%s"[^>]*Target=")[^"]*(")' % rid, r"\g<1>../media/image901.png\g<2>", rx)
    rels.write_text(rx2, encoding="utf-8")
    sx2 = re.sub(r"<a:srcRect[^>]*/>", "", sx)
    slide.write_text(sx2, encoding="utf-8")
    check("chart swapped into canvas (rId retarget + srcRect strip)",
          r.returncode == 0 and rx2 != rx and "<a:srcRect" not in sx2)

    # 7. finalize: clean + pack + render
    r = run([str(SCRIPTS / "finalize.py"), str(deck)])
    qa = sorted((WORK / "smoke_qa").glob("slide-*.jpg")) if (WORK / "smoke_qa").exists() else []
    check("finalize.py packs + validates", r.returncode == 0, (r.stdout + r.stderr)[-300:])
    check("PDF rendered", (WORK / "smoke.pdf").exists())
    check("QA JPGs rendered (4)", len(qa) == 4, f"got {len(qa)}")

    # 8. lint: zero critical
    r = run([str(SCRIPTS / "lint_deck.py"), str(WORK / "smoke.pptx")])
    m = re.search(r"SUMMARY: (\d+) critical", r.stdout)
    check("lint_deck.py: 0 critical on the packed deck",
          m is not None and m.group(1) == "0",
          m.group(0) if m else (r.stdout + r.stderr)[-300:])

    code = summary()
    if not args.keep and not FAIL:
        shutil.rmtree(WORK, ignore_errors=True)
    sys.exit(code)


def summary():
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed" +
          (f"  — FAILURES: {FAIL}" if FAIL else "  — all green"))
    return 1 if FAIL else 0


if __name__ == "__main__":
    main()
