#!/usr/bin/env python3
"""Assemble and package a new <name>-deck-builder.skill from the Code3 skeleton.

Configure-mode helper. Produces an installable, self-contained variant skill that
clones slides from a brand's OWN template core (never builds from scratch).

Two configure paths (set with --voice):
  * client account  (--voice code3, default): the client's visual template +
    Code3's writing voice. Use for an external account such as LVMH whose deck
    template you must match but whose copy you write in Code3 house style.
  * full brand suite (--voice custom): the org's own template AND its own voice.
    Use for another Graham Holdings company (Kaplan, Society6). Supply the org's
    own reference prose via --refs.

Usage:
    python spawn_variant.py \
        --name lvmh --display LVMH --voice code3 \
        --core   /path/lvmh_template_core.pptx \
        --index  /path/SLIDE_INDEX.md \
        --palette /path/brand_palette.json \
        --refs   /path/lvmh_refs_dir \
        --out    /path/build_dir

The variant dir <out>/<name>-deck-builder/ and the packaged
<out>/<name>-deck-builder.skill (SKILL.md at archive root) are written.
Scripts copied into the variant EXCLUDE the configurator (build_slide_index.py,
spawn_variant.py) -- a spawned variant does not re-spawn.
"""

import argparse
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

SKELETON_SCRIPTS = [
    "new_deck.py", "new_slide.py", "finalize.py", "map_slides.py",
    "refresh_text.py", "inspect_images.py", "make_chart.py",
    "lint_deck.py", "log_miss.py",
]
SKELETON_REFS = [
    "modes.md", "narrative.md", "brand.md", "slide_patterns.md",
    "content_guidelines.md", "quality_checks.md", "extending_library.md",
]

VOICE_PARA = {
    "code3": (
        "This skill was spawned from the Code3 deck-builder skeleton. "
        "**Whose voice:** copy follows **Code3 house style** "
        "(`references/brand.md`, `references/content_guidelines.md`). The visual "
        "template and slide layouts are **{DISPLAY}'s** — you are filling "
        "{DISPLAY}'s slides with Code3-written content. If {DISPLAY} has its own "
        "voice you must follow, re-spawn with `--voice custom`."
    ),
    "custom": (
        "This skill was spawned from the Code3 deck-builder skeleton. "
        "**Whose voice:** both the writing voice and the visual templates are "
        "**{DISPLAY}'s own** (`references/brand.md`, "
        "`references/content_guidelines.md`, `references/slide_patterns.md`)."
    ),
}

SKILL_TEMPLATE_FILE = Path(__file__).resolve().parent / "variant_skill_template.md"


def load_skill_template():
    """The variant SKILL.md template lives in variant_skill_template.md (next to
    this script) so it can be edited and diffed like any doc instead of drifting
    inside a Python string. package_skill.py runs a marker-based drift check
    between the parent SKILL.md and that template at packaging time."""
    if not SKILL_TEMPLATE_FILE.exists():
        sys.exit(f"ERROR: missing {SKILL_TEMPLATE_FILE} (the variant SKILL.md template)")
    return SKILL_TEMPLATE_FILE.read_text(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="variant slug, e.g. lvmh")
    ap.add_argument("--display", required=True, help="display brand name, e.g. LVMH")
    ap.add_argument("--voice", choices=["code3", "custom"], default="code3")
    ap.add_argument("--core", required=True, help="template core .pptx")
    ap.add_argument("--index", required=True, help="finished SLIDE_INDEX.md")
    ap.add_argument("--palette", help="brand_palette.json (else a default is written)")
    ap.add_argument("--refs", help="dir of reference .md overrides (brand.md, etc.)")
    ap.add_argument("--skeleton", help="code3-deck-builder skeleton dir "
                    "(default: this script's skill root)")
    ap.add_argument("--out", default=".", help="output dir (default: cwd)")
    args = ap.parse_args()

    slug = args.name.strip().lower()
    display = args.display.strip()
    skeleton = Path(args.skeleton).resolve() if args.skeleton else \
        Path(__file__).resolve().parent.parent
    out = Path(args.out).resolve()
    variant = out / f"{slug}-deck-builder"
    if variant.exists():
        shutil.rmtree(variant)
    (variant / "references").mkdir(parents=True)
    (variant / "scripts").mkdir(parents=True)
    (variant / "assets").mkdir(parents=True)

    core = Path(args.core).resolve()
    index = Path(args.index).resolve()
    for p, what in [(core, "core"), (index, "index"),
                    (skeleton, "skeleton")]:
        if not p.exists():
            print(f"ERROR: {what} not found: {p}")
            sys.exit(1)

    # --- SKILL.md ---
    voice_para = VOICE_PARA[args.voice].replace("{DISPLAY}", display)
    voice_desc = (", in Code3's writing voice" if args.voice == "code3"
                  else f", in {display}'s own voice")
    skill_md = (load_skill_template()
                .replace("{VOICE_PARA}", voice_para)
                .replace("{VOICE_DESC}", voice_desc)
                .replace("{SLUG}", slug)
                .replace("{DISPLAY}", display))
    (variant / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # --- references: skeleton defaults, then overlay --refs overrides ---
    for ref in SKELETON_REFS:
        src = skeleton / "references" / ref
        if src.exists():
            shutil.copy(src, variant / "references" / ref)
    if args.refs:
        refs_dir = Path(args.refs).resolve()
        for md in refs_dir.glob("*.md"):
            shutil.copy(md, variant / "references" / md.name)
            print(f"  overrode reference: {md.name}")

    # --- scripts: skeleton minus the configurator, copied verbatim ---
    # The skeleton scripts locate the core by glob (assets/*template_core*.pptx),
    # so they are already brand-agnostic and need no patching here.
    for s in SKELETON_SCRIPTS:
        src = skeleton / "scripts" / s
        if not src.exists():
            print(f"  WARNING: skeleton script missing: {s}")
            continue
        shutil.copy(src, variant / "scripts" / s)

    # --- assets ---
    shutil.copy(core, variant / "assets" / f"{slug}_template_core.pptx")
    shutil.copy(index, variant / "assets" / "SLIDE_INDEX.md")
    if args.palette and Path(args.palette).exists():
        shutil.copy(args.palette, variant / "assets" / "brand_palette.json")
    else:
        (variant / "assets" / "brand_palette.json").write_text(
            f'{{"name":"{display}","black":"#000000",'
            f'"palette":["#000000","#888888"]}}', encoding="utf-8")

    # --- package: zip CONTENTS (SKILL.md at archive root), like a spawned variant ---
    skill_pkg = out / f"{slug}-deck-builder.skill"
    if skill_pkg.exists():
        skill_pkg.unlink()
    with zipfile.ZipFile(skill_pkg, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(variant.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(variant))

    size_mb = skill_pkg.stat().st_size / 1e6
    print()
    print("Done.")
    print(f"  Variant dir: {variant}/")
    print(f"  Package:     {skill_pkg}  ({size_mb:.1f} MB)")
    if size_mb > 30:
        print(f"  !! {size_mb:.1f} MB exceeds the 30 MB skill limit — slim the core's "
              "media (flatten GIFs, downsample images) and re-spawn.")
    else:
        print(f"  OK: under the 30 MB skill limit.")


if __name__ == "__main__":
    main()
