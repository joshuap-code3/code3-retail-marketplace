#!/usr/bin/env python3
"""Read-only brand / quality audit of an existing .pptx — reports, never edits.

This is the mechanical half of the QA checklist (references/quality_checks.md):
it catches the things a regex can catch reliably — leftover scaffolding,
off-brand fonts, AI-tell phrases, em-dash spray, descriptive titles, uncited
data. The things that need eyes (overlaps, overflow, clipping, low contrast,
blank cells, off-brand color) are NOT guessed here — run `--render` and hand the
JPGs to the visual-QA subagent prompt in SKILL.md step 8.

It is **read-only**: it opens the .pptx, scans, and prints a report. It changes
nothing. "Fix it" is re-skin / refresh territory, not lint.

Usage:
    python lint_deck.py DECK.pptx                 # report to stdout
    python lint_deck.py DECK.pptx --md report.md  # also write a markdown report
    python lint_deck.py DECK.pptx --render        # also render JPGs for the eyes pass

How the brand baseline is set
-----------------------------
Allowed fonts are derived from the **bundled template core** (its theme font
scheme + any fonts its own slides use), not hardcoded — so the deployed template
defines "on-brand," and this works unchanged for a spawned variant (LVMH, etc.)
whose core uses different fonts. The brand book's named fonts are folded in as a
backstop. Color/contrast is deliberately left to the visual pass (too many false
positives from photos, gradients, and theme fills to flag mechanically).
"""

import argparse
import glob
import html
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

# Voice/scaffolding lists mirror references/quality_checks.md + references/brand.md.
CRITICAL_PLACEHOLDERS = [
    "lorem ipsum", "lorem", "click to add", "click to edit", "section title",
    "slide title", "presentation title", "subtitle", "subtext", "month year",
    "[callout", "[draft", "todo:", "lorem ipsum dolor", "your title here",
    "add a heading", "body level",
]
STAT_PLACEHOLDERS = ["0%", "$0k", "$0", "0.0%", " xx ", "x.x", "00%"]
AI_TELLS = [
    "delve", "leverage", "navigate the complexities", "navigate the landscape",
    "unlock the potential", "unlock potential", "embark", "journey",
    "synergize", "ideate", "deep dive", "at the end of the day",
    "in today's fast-paced", "ever-evolving", "game-changer", "best-in-class",
]
SOFT_AI_TELLS = ["landscape", "ecosystem"]  # legit sometimes — noted, not failed
DESCRIPTIVE_TITLE = re.compile(
    r"^\s*(a look at|understanding|intro(duction)? to|overview of|"
    r".*\boverview\b|.*\bupdate\b|.*\bsummary\b|exploring)\s*$", re.I)
FILLER_OPENERS = re.compile(
    r"^\s*(in this section|we are pleased|this slide|here we will|"
    r"in this presentation|today we)", re.I)
OFFICE_DEFAULT_FONTS = {
    "calibri", "arial", "aptos", "times new roman", "verdana", "helvetica",
    "cambria", "tahoma", "georgia", "segoe ui",
}
DATA_RE = re.compile(r"\d+(\.\d+)?\s?%|\$\s?\d|[+\-]\s?\d|\bROAS\b|\bCTR\b|\bNTB\b|\bCPM\b")


def core_path(skill_dir):
    hits = sorted(glob.glob(str(skill_dir / "assets" / "*template_core*.pptx")))
    return Path(hits[0]) if hits else None


def latin_fonts(xml):
    return set(re.findall(r'<a:latin[^>]*typeface="([^"]*)"', xml))


def allowed_fonts(core_pptx):
    """On-brand fonts = every font the bundled core uses in its theme, slides,
    layouts, and masters. Theme refs ('+mn-lt') and empty are always allowed.
    Reading all four parts (not just theme+slides) means real template weights
    that only appear in layouts — e.g. Barlow Condensed — aren't false-flagged."""
    allowed = {"barlow", "kalam"}  # brand-book backstop
    if core_pptx and core_pptx.exists():
        with zipfile.ZipFile(core_pptx) as z:
            for n in z.namelist():
                if re.match(r"ppt/(theme/theme|slides/slide|slideLayouts/slideLayout|"
                            r"slideMasters/slideMaster)\d+\.xml$", n):
                    for f in latin_fonts(z.read(n).decode("utf-8", "ignore")):
                        if f and not f.startswith("+"):
                            allowed.add(f.lower())
    return allowed


def slide_order(z):
    pres = z.read("ppt/presentation.xml").decode("utf-8", "ignore")
    rels = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8", "ignore")
    rid2f = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"', rels))
    order = re.findall(r'<p:sldId\b[^>]*r:id="(rId\d+)"', pres)
    return [(i + 1, rid2f[r]) for i, r in enumerate(order) if r in rid2f]


def text_runs(xml):
    return [html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
            for t in re.findall(r"<a:t[^>]*>(.*?)</a:t>", xml, re.DOTALL)]


def scan_slide(xml, allowed):
    runs = [r for r in text_runs(xml) if r]
    joined = "   ".join(runs)
    low = joined.lower()
    issues = {"critical": [], "style": [], "stat": [], "source": [], "font": []}

    for ph in CRITICAL_PLACEHOLDERS:
        if ph in low:
            issues["critical"].append(f'leftover "{ph}"')
    for ph in STAT_PLACEHOLDERS:
        if ph in low:
            issues["stat"].append(f'"{ph.strip()}"')

    for f in sorted(latin_fonts(xml)):
        if not f or f.startswith("+") or f.lower() in allowed:
            continue
        if f.lower() in OFFICE_DEFAULT_FONTS:
            issues["font"].append(f'off-brand font "{f}" (Office default)')
        else:
            issues["font"].append(f'non-template font "{f}" — confirm on-brand')

    for term in AI_TELLS:
        if re.search(r"\b" + re.escape(term) + r"\b", low):
            issues["style"].append(f'AI-tell "{term}"')
    for term in SOFT_AI_TELLS:
        if re.search(r"\b" + term + r"\b", low):
            issues["style"].append(f'"{term}" (AI-tell unless literal)')
    em = joined.count("—")
    if em >= 3:
        issues["style"].append(f"{em} em dashes (heavy — an AI-tell)")
    title = runs[0] if runs else ""
    if DESCRIPTIVE_TITLE.match(title):
        issues["style"].append(f'title "{title[:40]}" is descriptive — assert or ask instead')
    for r in runs[:2]:
        if FILLER_OPENERS.match(r):
            issues["style"].append(f'filler opener "{r[:40]}…"')
            break

    if DATA_RE.search(joined) and "source" not in low and "src" not in low:
        issues["source"].append("has stats but no visible source — Code3 always cites")
    return runs[0] if runs else "(no text)", issues


def render(deck, skill_dir):
    """Optional: render to JPGs for the visual pass (reuses the pptx skill)."""
    scripts = find_pptx_scripts()
    if not scripts:
        print("  (--render skipped: pptx skill scripts/ not found)")
        return
    qa = deck.parent / f"{deck.stem}_lint_qa"
    qa.mkdir(exist_ok=True)
    tmp = deck.parent / f".{deck.stem}_lintsoffice"
    tmp.mkdir(exist_ok=True)
    env = os.environ.copy(); env["HOME"] = env["TMPDIR"] = str(tmp)
    subprocess.check_call(["python", str(scripts / "office" / "soffice.py"), "--headless",
                           "--convert-to", "pdf", "--outdir", str(deck.parent), str(deck)],
                          env=env)
    pdf = deck.with_suffix(".pdf")
    subprocess.check_call(["pdftoppm", "-jpeg", "-r", "150", str(pdf), str(qa / "slide")])
    print(f"  Rendered JPGs → {qa}/  (hand to the SKILL.md step-8 visual-QA subagent)")


def find_pptx_scripts():
    for c in ([Path(os.environ["CODE3_PPTX_SCRIPTS"])] if os.environ.get("CODE3_PPTX_SCRIPTS") else []) \
            + [Path(p) for p in sorted(glob.glob("/sessions/*/mnt/.claude/skills/pptx/scripts"))] \
            + [Path.home() / ".claude/skills/pptx/scripts", Path("/root/.claude/skills/pptx/scripts")]:
        if c and c.exists():
            return c
    return None


def main():
    ap = argparse.ArgumentParser(description="Read-only brand/QA lint for a .pptx.")
    ap.add_argument("deck", help="the .pptx to audit")
    ap.add_argument("--md", help="also write the report to this markdown file")
    ap.add_argument("--render", action="store_true", help="render JPGs for the visual pass")
    args = ap.parse_args()

    deck = Path(args.deck)
    if not deck.exists() or deck.suffix.lower() != ".pptx":
        sys.exit(f"ERROR: not a .pptx: {deck}")
    skill_dir = Path(__file__).resolve().parent.parent
    allowed = allowed_fonts(core_path(skill_dir))

    with zipfile.ZipFile(deck) as z:
        order = slide_order(z)
        per_slide = []
        for pos, f in order:
            title, issues = scan_slide(z.read(f"ppt/slides/{f}").decode("utf-8", "ignore"), allowed)
            per_slide.append((pos, f, title, issues))

    L = []
    L.append(f"LINT — {deck.name}  ({len(order)} slides, presentation order)")
    L.append(f"On-brand fonts (from the bundled core): "
             f"{', '.join(sorted(allowed)) or '(none found)'}")
    L.append("")
    tally = {k: 0 for k in ("critical", "font", "style", "stat", "source")}

    def emit(header, key, note=""):
        rows = [(p, f, t, i[key]) for p, f, t, i in per_slide if i[key]]
        L.append(f"{header} ({sum(len(r[3]) for r in rows)}){note}:")
        if not rows:
            L.append("  none")
        for p, f, t, items in rows:
            tally[key] += len(items)
            L.append(f"  pos {p} ({f}) — {t[:46]}")
            for it in items:
                L.append(f"      • {it}")
        L.append("")

    emit("CRITICAL — looks unfinished; fix before any client sees it", "critical")
    emit("OFF-BRAND FONTS", "font")
    emit("STYLE — Code3 voice (references/brand.md)", "style")
    emit("POSSIBLE STAT PLACEHOLDERS — could be real data, confirm", "stat")
    emit("DATA WITHOUT A VISIBLE SOURCE — advisory", "source")

    L.append("VISUAL PASS (not mechanical — needs eyes): overlaps, text overflow/"
             "clipping, low-contrast, blank columns/cells, off-brand color, title "
             "wrapping. Re-run with --render, then use the SKILL.md step-8 subagent prompt.")
    L.append("")
    L.append(f"SUMMARY: {tally['critical']} critical, {tally['font']} font, "
             f"{tally['style']} style, {tally['stat']} stat-placeholder, "
             f"{tally['source']} source — across {len(order)} slides. "
             "(Mechanical checks only; clear the visual pass too.)")
    report = "\n".join(L)
    print(report)

    if args.md:
        Path(args.md).write_text("```\n" + report + "\n```\n", encoding="utf-8")
        print(f"\nWrote {args.md}")
    if args.render:
        render(deck, skill_dir)


if __name__ == "__main__":
    main()
