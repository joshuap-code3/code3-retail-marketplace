#!/usr/bin/env python3
"""Single-slide builds — make or insert ONE template slide, no full-deck workflow.

Two sub-commands:

  standalone  — clone one template slide into a fresh 1-slide working deck.
      python new_slide.py standalone /tmp/build/oneslide --pos 46
      # (or --file slide126.xml).  Then edit + `finalize.py /tmp/build/oneslide`.

  insert      — transplant one template slide INTO an existing Code3 deck at a
                position (optionally replacing the slide already there).
      python new_slide.py insert /tmp/build/updated --into "QBR.pptx" --pos 7 --at 5
      python new_slide.py insert /tmp/build/updated --into "QBR.pptx" --pos 7 --at 5 --replace
      # Then edit the new slide + `finalize.py /tmp/build/updated`.

Why this exists
---------------
A single slide is not a 3–5 beat argument, so single-slide builds **bypass the
story-first throughline gate** (see references/modes.md → single-slide). All the
other hard rules still apply: clone a real template slide (never build from
scratch), leave no placeholder text, cite data, and run visual QA on the slide.

How it stays safe
-----------------
`clean.py` never strips slideLayouts/masters, so any deck previously built from
the Code3 core still carries every template slide's layout. Insert therefore
copies the chosen core slide's XML + its media into the target and points the new
slide at the SAME-named layout already present in the target. If that layout is
missing (the target wasn't built from this core), insert refuses rather than
shipping a slide with a broken layout reference — rebuild via generate/re-skin.

`--pos` is a SLIDE_INDEX **presentation-order position** (resolved against the
core's order), NOT a slideN.xml filename. `--at` is the 1-based position in the
TARGET deck where the new slide should land (default: append at end).
"""

import argparse
import glob
import re
import shutil
import subprocess
import sys
from pathlib import Path

CT_SLIDE = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
MEDIA_EXT_CT = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".svg": "image/svg+xml", ".emf": "image/x-emf",
    ".wmf": "image/x-wmf", ".bmp": "image/bmp", ".tiff": "image/tiff",
}


# --------------------------------------------------------------------------- #
def find_core(skill_dir):
    hits = sorted(glob.glob(str(skill_dir / "assets" / "*template_core*.pptx")))
    return Path(hits[0]) if hits else None


def unzip_to(pptx, dest):
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["unzip", "-q", "-o", str(pptx), "-d", str(dest)])


def position_to_file(unpacked):
    """Map presentation-order position -> slideN.xml for an unpacked deck."""
    pres = (unpacked / "ppt" / "presentation.xml").read_text(encoding="utf-8")
    rels = (unpacked / "ppt" / "_rels" / "presentation.xml.rels").read_text(encoding="utf-8")
    rid2f = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"', rels))
    order = re.findall(r'<p:sldId\b[^>]*r:id="(rId\d+)"', pres)
    return {i + 1: rid2f[rid] for i, rid in enumerate(order) if rid in rid2f}


def resolve_core_file(core_unpacked, pos, file_arg):
    if file_arg:
        f = file_arg if file_arg.endswith(".xml") else f"{file_arg}.xml"
        if not (core_unpacked / "ppt" / "slides" / f).exists():
            sys.exit(f"ERROR: {f} not found in the core.")
        return f
    p2f = position_to_file(core_unpacked)
    if pos not in p2f:
        sys.exit(f"ERROR: position {pos} out of range (core has {len(p2f)} slides).")
    return p2f[pos]


def next_slide_num(slides_dir):
    nums = [int(m.group(1)) for f in slides_dir.glob("slide*.xml")
            if (m := re.match(r"slide(\d+)\.xml$", f.name))]
    return (max(nums) + 1) if nums else 1


# --------------------------------------------------------------------------- #
def reduce_to_one(unpacked, keep_file):
    """Standalone: rewrite sldIdLst to keep only `keep_file`. finalize/clean drops
    every other slide + its now-orphaned media."""
    rels_p = unpacked / "ppt" / "_rels" / "presentation.xml.rels"
    pres_p = unpacked / "ppt" / "presentation.xml"
    rels = rels_p.read_text(encoding="utf-8")
    pres = pres_p.read_text(encoding="utf-8")
    m = re.search(rf'Id="(rId\d+)"[^>]*Target="slides/{re.escape(keep_file)}"', rels)
    if not m:
        sys.exit(f"ERROR: {keep_file} has no presentation relationship.")
    keep_rid = m.group(1)
    one = re.search(rf'<p:sldId\b[^>]*r:id="{keep_rid}"[^>]*/>', pres)
    if not one:
        sys.exit(f"ERROR: {keep_file} ({keep_rid}) not in sldIdLst.")
    pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>',
                  f'<p:sldIdLst>{one.group(0)}</p:sldIdLst>', pres, flags=re.DOTALL)
    pres_p.write_text(pres, encoding="utf-8")


def transplant(core_unpacked, target, core_file, at_index, replace):
    """Copy one core slide (+media) into `target`, pointing at the same-named
    layout already in target. Register it in sldIdLst at `at_index` (1-based)."""
    NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    core_slide = core_unpacked / "ppt" / "slides" / core_file
    core_rels = core_unpacked / "ppt" / "slides" / "_rels" / f"{core_file}.rels"
    rels_txt = core_rels.read_text(encoding="utf-8") if core_rels.exists() else \
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'

    # Layout the core slide uses must already exist in the target.
    lm = re.search(r'Target="\.\./slideLayouts/(slideLayout\d+\.xml)"', rels_txt)
    if lm and not (target / "ppt" / "slideLayouts" / lm.group(1)).exists():
        sys.exit(f"ERROR: target deck is missing {lm.group(1)} — it wasn't built "
                 "from this Code3 core. Rebuild via generate/re-skin instead of insert.")

    slides_dir = target / "ppt" / "slides"
    new_num = next_slide_num(slides_dir)
    new_file = f"slide{new_num}.xml"
    shutil.copy(core_slide, slides_dir / new_file)

    # Rebuild the new slide's rels: keep layout as-is, drop notesSlide, copy media.
    media_dir = target / "ppt" / "media"
    media_dir.mkdir(exist_ok=True)
    base = next_media_base(media_dir)
    new_rels_lines, i = [], 0
    for rel in re.findall(r"<Relationship\b[^>]*/>", rels_txt):
        rtype = (re.search(r'Type="([^"]+)"', rel) or [None, ""])[1]
        if "notesSlide" in rtype:
            continue
        tgt = (re.search(r'Target="([^"]+)"', rel) or [None, ""])[1]
        mm = re.match(r"\.\./media/(.+)$", tgt)
        if mm:
            src = core_unpacked / "ppt" / "media" / mm.group(1)
            ext = src.suffix.lower()
            dest_name = f"image{base + i}{ext}"
            i += 1
            if src.exists():
                shutil.copy(src, media_dir / dest_name)
            rel = rel.replace(f'Target="{tgt}"', f'Target="../media/{dest_name}"')
        new_rels_lines.append(rel)
        ensure_content_type(target, Path(tgt).suffix.lower())
    (slides_dir / "_rels").mkdir(exist_ok=True)
    (slides_dir / "_rels" / f"{new_file}.rels").write_text(
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(new_rels_lines) + "</Relationships>", encoding="utf-8")

    # [Content_Types].xml: Override for the new slide part.
    ct_p = target / "[Content_Types].xml"
    ct = ct_p.read_text(encoding="utf-8")
    if f'PartName="/ppt/slides/{new_file}"' not in ct:
        ct = ct.replace("</Types>",
                        f'<Override PartName="/ppt/slides/{new_file}" '
                        f'ContentType="{CT_SLIDE}"/></Types>')
        ct_p.write_text(ct, encoding="utf-8")

    # presentation.xml.rels: new relationship for the slide.
    pr_p = target / "ppt" / "_rels" / "presentation.xml.rels"
    pr = pr_p.read_text(encoding="utf-8")
    existing_rids = [int(x) for x in re.findall(r'Id="rId(\d+)"', pr)]
    new_rid = f"rId{(max(existing_rids) if existing_rids else 0) + 1}"
    pr = pr.replace("</Relationships>",
                    f'<Relationship Id="{new_rid}" Type="http://schemas.openxmlformats.org/'
                    f'officeDocument/2006/relationships/slide" Target="slides/{new_file}"/>'
                    "</Relationships>")
    pr_p.write_text(pr, encoding="utf-8")

    # presentation.xml: insert (and maybe replace) the sldId at `at_index`.
    pres_p = target / "ppt" / "presentation.xml"
    pres = pres_p.read_text(encoding="utf-8")
    sldids = re.findall(r"<p:sldId\b[^>]*/>", pres)
    new_id = max((int(x) for x in re.findall(r'<p:sldId\s+id="(\d+)"', pres)), default=255) + 1
    new_el = f'<p:sldId id="{new_id}" r:id="{new_rid}"/>'
    k = len(sldids) if at_index is None else max(0, min(at_index - 1, len(sldids)))
    replaced = None
    if replace and sldids:
        ri = min(k, len(sldids) - 1)
        replaced = sldids.pop(ri)
        k = ri
    sldids.insert(k, new_el)
    pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>',
                  "<p:sldIdLst>" + "".join(sldids) + "</p:sldIdLst>", pres, flags=re.DOTALL)
    pres_p.write_text(pres, encoding="utf-8")
    return new_file, k + 1, replaced


def next_media_base(media_dir):
    nums = [int(m.group(1)) for f in media_dir.glob("image*")
            if (m := re.match(r"image(\d+)", f.name))]
    return max(nums + [900]) + 1


def ensure_content_type(target, ext):
    if ext not in MEDIA_EXT_CT:
        return
    ct_p = target / "[Content_Types].xml"
    ct = ct_p.read_text(encoding="utf-8")
    if f'Extension="{ext.lstrip(".")}"' not in ct:
        ct = ct.replace("</Types>",
                        f'<Default Extension="{ext.lstrip(".")}" '
                        f'ContentType="{MEDIA_EXT_CT[ext]}"/></Types>')
        ct_p.write_text(ct, encoding="utf-8")


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Single-slide builds (standalone / insert).")
    ap.add_argument("mode", choices=["standalone", "insert"])
    ap.add_argument("basename", help="working basename, e.g. /tmp/build/oneslide")
    ap.add_argument("--pos", type=int, help="core SLIDE_INDEX position to clone")
    ap.add_argument("--file", help="core slide file (e.g. slide126.xml) instead of --pos")
    ap.add_argument("--into", help="insert mode: the existing .pptx to add the slide to")
    ap.add_argument("--at", type=int, help="insert mode: 1-based target position (default: end)")
    ap.add_argument("--replace", action="store_true",
                    help="insert mode: replace the slide currently at --at")
    args = ap.parse_args()

    if not args.pos and not args.file:
        sys.exit("ERROR: give --pos N or --file slideN.xml (which template slide to use).")

    skill_dir = Path(__file__).resolve().parent.parent
    core = find_core(skill_dir)
    if not core:
        sys.exit(f"ERROR: no *template_core*.pptx in {skill_dir/'assets'}")

    base = Path(args.basename)
    base.parent.mkdir(parents=True, exist_ok=True)
    out_pptx = base.with_suffix(".pptx")
    unpacked = base.parent / f"{base.name}_unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)

    core_unpacked = base.parent / f".{base.name}_core"
    if core_unpacked.exists():
        shutil.rmtree(core_unpacked)
    unzip_to(core, core_unpacked)
    core_file = resolve_core_file(core_unpacked, args.pos, args.file)

    if args.mode == "standalone":
        shutil.copy(core, out_pptx); out_pptx.chmod(0o644)
        unzip_to(out_pptx, unpacked)
        reduce_to_one(unpacked, core_file)
        shutil.rmtree(core_unpacked, ignore_errors=True)
        print(f"Standalone 1-slide deck ready: {unpacked}")
        print(f"  Cloned core {core_file} (position {args.pos or core_file}).")
        print(f"  Edit ppt/slides/{core_file} (use refresh_text.py --list to see slots),")
        print(f"  then: python finalize.py {base}")
        return

    # insert
    if not args.into:
        sys.exit("ERROR: insert mode needs --into <existing.pptx>.")
    existing = Path(args.into)
    if not existing.exists():
        sys.exit(f"ERROR: --into deck not found: {existing}")
    shutil.copy(existing, out_pptx); out_pptx.chmod(0o644)
    unzip_to(out_pptx, unpacked)
    new_file, final_pos, replaced = transplant(core_unpacked, unpacked, core_file,
                                               args.at, args.replace)
    shutil.rmtree(core_unpacked, ignore_errors=True)
    print(f"Inserted core {core_file} into {existing.name} as {new_file} "
          f"at position {final_pos}" + (" (replaced the slide there)" if replaced else "") + ".")
    print(f"  Working dir: {unpacked}")
    print(f"  Edit ppt/slides/{new_file} (refresh_text.py --list to see slots), "
          f"then: python finalize.py {base}")


if __name__ == "__main__":
    main()
