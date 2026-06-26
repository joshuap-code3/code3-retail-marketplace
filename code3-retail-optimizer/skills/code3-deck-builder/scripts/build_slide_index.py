#!/usr/bin/env python3
"""Render an arbitrary template core to thumbnails and scaffold its SLIDE_INDEX.

Configure-mode helper. Given a `*_template_core.pptx`, this:
  1. Unpacks it (pptx skill's office/unpack.py, else unzip).
  2. Renders every slide to thumbs/slide-<pos>.jpg (LibreOffice -> PDF -> pdftoppm),
     in PRESENTATION ORDER, so a thumbnail's number == its SLIDE_INDEX position.
  3. Builds the position -> slideN.xml map (presentation order != filename).
  4. For each slide, extracts every <a:t> text run in document order and every
     <p:pic> image box (EMU position + size + media file) -- the mechanical facts.
  5. Writes SLIDE_INDEX_SCAFFOLD.md: facts filled in, with _TODO_ fields for
     Purpose / Best for / Visual / Placeholders / Constraints that a human (or the
     model, after viewing each thumbnail) completes and saves as SLIDE_INDEX.md.

Usage:
    python build_slide_index.py CORE.pptx [OUT_DIR]
        OUT_DIR defaults to <core-stem>_index/ next to the core.

After running: view each thumbs/slide-*.jpg, complete the _TODO_ fields, and save
the result as SLIDE_INDEX.md next to the core (the deck-builder reads that file).
"""

import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

EMU_PER_IN = 914400


def find_pptx_scripts_dir():
    """Find the pptx skill's scripts/ directory, portably across machines."""
    candidates = []
    env = os.environ.get("CODE3_PPTX_SCRIPTS")
    if env:
        candidates.append(Path(env))
    candidates += [Path(p) for p in sorted(
        glob.glob("/sessions/*/mnt/.claude/skills/pptx/scripts"))]
    candidates += [
        Path.home() / ".claude/skills/pptx/scripts",
        Path("/root/.claude/skills/pptx/scripts"),
    ]
    for c in candidates:
        if c and c.exists():
            return c
    return None


def unpack(core_pptx, dest):
    pptx_scripts = find_pptx_scripts_dir()
    unpack_script = pptx_scripts / "office" / "unpack.py" if pptx_scripts else None
    if unpack_script and unpack_script.exists():
        subprocess.check_call(["python", str(unpack_script), str(core_pptx), str(dest)])
    else:
        dest.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(["unzip", "-q", str(core_pptx), "-d", str(dest)])


def render_thumbs(core_pptx, out_dir, thumbs_dir, dpi=100):
    """Render core -> PDF -> per-page JPG named by 1-based page (== presentation order)."""
    tmpdir = out_dir / ".sofficetmp"
    tmpdir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TMPDIR"] = str(tmpdir)
    env["HOME"] = str(tmpdir)

    pptx_scripts = find_pptx_scripts_dir()
    soffice = (pptx_scripts / "office" / "soffice.py") if pptx_scripts else None
    if soffice and soffice.exists():
        subprocess.check_call(
            ["python", str(soffice), "--headless", "--convert-to", "pdf",
             "--outdir", str(out_dir), str(core_pptx)], env=env)
    else:
        subprocess.check_call(
            ["soffice", "--headless", "--convert-to", "pdf",
             "--outdir", str(out_dir), str(core_pptx)], env=env)
    pdf = out_dir / (core_pptx.stem + ".pdf")
    if not pdf.exists():
        # soffice sometimes sanitizes the stem; grab whatever pdf landed.
        pdfs = sorted(out_dir.glob("*.pdf"))
        if not pdfs:
            print("ERROR: no PDF produced by LibreOffice.")
            sys.exit(1)
        pdf = pdfs[0]
    thumbs_dir.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        ["pdftoppm", "-jpeg", "-r", str(dpi), str(pdf), str(thumbs_dir / "slide")])
    # Normalize pdftoppm's zero-padded "slide-001.jpg" -> "slide-1.jpg".
    for jpg in thumbs_dir.glob("slide-*.jpg"):
        m = re.match(r"slide-0*(\d+)\.jpg$", jpg.name)
        if m:
            tgt = thumbs_dir / f"slide-{int(m.group(1))}.jpg"
            if jpg != tgt:
                jpg.rename(tgt)


def position_file_map(unpacked):
    pres = (unpacked / "ppt" / "presentation.xml").read_text(encoding="utf-8", errors="ignore")
    rels = (unpacked / "ppt" / "_rels" / "presentation.xml.rels").read_text(
        encoding="utf-8", errors="ignore")
    rid2f = dict(re.findall(
        r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"', rels))
    order = re.findall(r'<p:sldId[^>]*r:id="(rId\d+)"', pres)
    return [(i + 1, rid2f.get(rid, "?")) for i, rid in enumerate(order)]


def text_runs(slide_xml):
    raw = re.findall(r"<a:t\b[^>]*>(.*?)</a:t>", slide_xml, re.DOTALL)
    runs = []
    for t in raw:
        t = re.sub("<[^>]+>", "", t).strip()
        if t:
            runs.append(t)
    return runs


def image_boxes(slide_xml, slide_file, unpacked):
    """Return [(x_in, y_in, w_in, h_in, media)] for each <p:pic>, by EMU position."""
    rels_path = unpacked / "ppt" / "slides" / "_rels" / (slide_file + ".rels")
    rid2media = {}
    if rels_path.exists():
        rels = rels_path.read_text(encoding="utf-8", errors="ignore")
        rid2media = dict(re.findall(
            r'Id="(rId\d+)"[^>]*Target="\.\./media/([^"]+)"', rels))
    boxes = []
    for pic in re.findall(r"<p:pic\b.*?</p:pic>", slide_xml, re.DOTALL):
        embed = re.search(r'r:embed="(rId\d+)"', pic)
        off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', pic)
        ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"', pic)
        media = rid2media.get(embed.group(1), "?") if embed else "?"
        if off and ext:
            x, y = int(off.group(1)), int(off.group(2))
            cx, cy = int(ext.group(1)), int(ext.group(2))
            boxes.append((x / EMU_PER_IN, y / EMU_PER_IN,
                          cx / EMU_PER_IN, cy / EMU_PER_IN, media))
        else:
            boxes.append((None, None, None, None, media))
    return boxes


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    core = Path(sys.argv[1]).resolve()
    if not core.exists():
        print(f"ERROR: core not found: {core}")
        sys.exit(1)
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else core.parent / f"{core.stem}_index"
    out_dir.mkdir(parents=True, exist_ok=True)
    unpacked = out_dir / "_unpacked"
    thumbs = out_dir / "thumbs"

    print(f"[1/4] Unpacking {core.name} -> {unpacked}")
    if unpacked.exists():
        shutil.rmtree(unpacked)
    unpack(core, unpacked)

    print(f"[2/4] Rendering thumbnails -> {thumbs}/slide-*.jpg")
    render_thumbs(core, out_dir, thumbs)

    print("[3/4] Building position -> file map")
    pos_map = position_file_map(unpacked)

    print("[4/4] Extracting text runs + image boxes; writing scaffold")
    lines = []
    lines.append(f"# {core.stem} - Slide Index (SCAFFOLD - complete the _TODO_ fields)\n")
    lines.append(
        "Generated by build_slide_index.py. The mechanical facts below (file, text "
        "runs, image boxes) are filled in. **You must view each thumbnail in "
        "`thumbs/` and complete every _TODO_ field** (Purpose / Best for / Visual / "
        "Placeholders / Constraints), then save this as `SLIDE_INDEX.md` next to the "
        "core. The deck-builder relies on these descriptions to pick slides.\n")
    lines.append("## Position -> file map\n")
    lines.append("| Pos | File | First text run |")
    lines.append("|----:|------|----------------|")
    cache = {}
    for pos, f in pos_map:
        sx = ""
        if f != "?":
            p = unpacked / "ppt" / "slides" / f
            if p.exists():
                sx = p.read_text(encoding="utf-8", errors="ignore")
        cache[pos] = (f, sx)
        runs = text_runs(sx)
        first = esc(runs[0][:46]) if runs else "(no text)"
        lines.append(f"| {pos} | {f} | {first} |")
    lines.append("\n> Positions are PRESENTATION ORDER, not slideN.xml filenames. "
                 "map_slides.py reproduces this map at build time.\n")
    lines.append("## Slides\n")
    for pos, f in pos_map:
        _, sx = cache[pos]
        runs = text_runs(sx)
        boxes = image_boxes(sx, f, unpacked) if f != "?" else []
        lines.append(f"### Position {pos} - {f}  ·  thumbnail: thumbs/slide-{pos}.jpg")
        lines.append("**Purpose:** _TODO_  ")
        lines.append("**Best for:** _TODO_  ")
        lines.append("**Visual:** _TODO - describe from the thumbnail (layout, colors, motifs)_  ")
        lines.append("**Text runs (document order):**")
        if runs:
            for i, t in enumerate(runs, 1):
                lines.append(f"  {i}. \"{esc(t[:70])}{'…' if len(t) > 70 else ''}\"")
        else:
            lines.append("  (none)")
        if boxes:
            lines.append("**Image boxes:**")
            for (x, y, w, h, media) in boxes:
                if x is None:
                    lines.append(f"  - {media} (position not parsed)")
                else:
                    lines.append(f"  - {media} @ x={x:.2f}in y={y:.2f}in  {w:.2f}×{h:.2f}in")
        else:
            lines.append("**Image boxes:** none")
        lines.append("**Placeholders to replace:** _TODO - list each editable slot_  ")
        lines.append("**Constraints:** _TODO - approx text length / # of items the layout holds_  ")
        lines.append(f"**Has image placeholder:** {'yes' if boxes else 'no'}\n")

    out_md = out_dir / "SLIDE_INDEX_SCAFFOLD.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    n = len(pos_map)
    print()
    print("Done.")
    print(f"  Scaffold:   {out_md}")
    print(f"  Thumbnails: {thumbs}/ ({n} slides, slide-1..slide-{n})")
    print(f"  Unpacked:   {unpacked}/")
    print()
    print("Next: view every thumbs/slide-*.jpg, fill the _TODO_ fields, save as")
    print("SLIDE_INDEX.md next to the core.")


if __name__ == "__main__":
    main()
