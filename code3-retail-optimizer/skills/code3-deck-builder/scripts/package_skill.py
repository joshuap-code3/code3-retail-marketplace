#!/usr/bin/env python3
"""Package a deck-builder skill dir into an installable .skill (+ .zip twin).

One command replaces the remembered zip incantation, with the packaging rules
that were learned the hard way baked in:

  * SKILL.md sits at the ARCHIVE ROOT (zip the dir CONTENTS, not the dir) —
    a dir-prefixed archive materializes only SKILL.md on install.
  * .DS_Store, __pycache__, *.pyc, *_bak* never ship.
  * 30 MB skill size limit is enforced (warn at 25).
  * The previous .skill in --out is snapshotted to _template_archive/ first.
  * Drift check: features documented in the parent SKILL.md must also appear in
    scripts/variant_skill_template.md (the source of a spawned variant's
    SKILL.md), or variants silently won't inherit them. Warns; --strict fails.

Usage:
    python scripts/package_skill.py                  # package this skill
    python scripts/package_skill.py --skill-dir DIR  # package another (e.g. a variant)
    python scripts/package_skill.py --strict         # drift warnings are fatal

After packaging, REINSTALL the .skill (Settings > Capabilities) — editing the
dev source does not update the installed skill.
"""

import argparse
import datetime
import re
import sys
import zipfile
from pathlib import Path

EXCLUDE_PATTERNS = (".DS_Store", "__pycache__", ".pyc", "_bak")
SIZE_LIMIT_MB = 30
SIZE_WARN_MB = 25

# Feature markers that must exist in BOTH the parent SKILL.md and the variant
# template, or spawned variants silently lose the feature (the gotcha that bit
# the throughline rollout). Add a marker when you add a feature.
DRIFT_MARKERS = [
    (r"story-first",          "story-first / throughline gate"),
    (r"refresh_text\.py",     "position-aware text replacement"),
    (r"inspect_images\.py",   "image-position inspection"),
    (r"make_chart\.py",       "chart engine"),
    (r"lint_deck\.py",        "lint / brand audit"),
    (r"log_miss\.py",         "library-gap miss log"),
    (r"new_slide\.py",        "single-slide builds"),
    (r"srcRect",              "srcRect crop hazard on image swaps"),
    (r"chart[- ]canvas",      "chart-canvas routing for real-data charts"),
    (r"[Vv]isual QA",         "mandatory visual QA"),
]


def excluded(path: Path) -> bool:
    s = str(path)
    return any(pat in s for pat in EXCLUDE_PATTERNS)


def drift_check(skill_dir: Path) -> list:
    """Compare parent SKILL.md against the variant template; return warnings."""
    parent = skill_dir / "SKILL.md"
    template = skill_dir / "scripts" / "variant_skill_template.md"
    if not template.exists():
        return []  # packaging a spawned variant — no template to check
    p, t = parent.read_text(encoding="utf-8"), template.read_text(encoding="utf-8")
    warnings = []
    for pattern, desc in DRIFT_MARKERS:
        in_p, in_t = bool(re.search(pattern, p)), bool(re.search(pattern, t))
        if in_p and not in_t:
            warnings.append(f"in SKILL.md but NOT in variant template: {desc} (/{pattern}/)")
        elif in_t and not in_p:
            warnings.append(f"in variant template but NOT in SKILL.md: {desc} (/{pattern}/)")
    return warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill-dir", help="skill source dir (default: this script's skill root)")
    ap.add_argument("--out", help="output dir for the .skill/.zip (default: skill dir's parent)")
    ap.add_argument("--no-backup", action="store_true", help="skip the _template_archive snapshot")
    ap.add_argument("--strict", action="store_true", help="drift warnings are fatal")
    args = ap.parse_args()

    skill_dir = Path(args.skill_dir).resolve() if args.skill_dir else \
        Path(__file__).resolve().parent.parent
    out = Path(args.out).resolve() if args.out else skill_dir.parent
    name = skill_dir.name

    if not (skill_dir / "SKILL.md").exists():
        sys.exit(f"ERROR: no SKILL.md in {skill_dir} — not a skill dir")

    # --- drift check ---
    warnings = drift_check(skill_dir)
    for w in warnings:
        print(f"  DRIFT: {w}")
    if warnings and args.strict:
        sys.exit("Drift check failed (--strict). Reconcile SKILL.md and "
                 "scripts/variant_skill_template.md, then re-run.")

    # --- backup the previous package ---
    pkg = out / f"{name}.skill"
    if pkg.exists() and not args.no_backup:
        archive = out / "_template_archive"
        archive.mkdir(exist_ok=True)
        stamp = datetime.date.today().isoformat()
        dest = archive / f"{name}_pre-repack_{stamp}.skill"
        n = 1
        while dest.exists():
            n += 1
            dest = archive / f"{name}_pre-repack_{stamp}_{n}.skill"
        dest.write_bytes(pkg.read_bytes())
        print(f"  backup: {dest.name}")

    # --- build (contents at archive root) ---
    files = [f for f in sorted(skill_dir.rglob("*")) if f.is_file() and not excluded(f)]
    tmp = out / f"{name}.skill.tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f.relative_to(skill_dir))
    tmp.replace(pkg)
    zip_twin = out / f"{name}.zip"
    zip_twin.write_bytes(pkg.read_bytes())

    # --- verify ---
    with zipfile.ZipFile(pkg) as z:
        names = z.namelist()
    assert "SKILL.md" in names, "SKILL.md is not at the archive root — install would break"
    size_mb = pkg.stat().st_size / 1e6
    print(f"\n  Package: {pkg}  ({size_mb:.1f} MB, {len(names)} files, SKILL.md at root)")
    print(f"  Twin:    {zip_twin}")
    if size_mb > SIZE_LIMIT_MB:
        sys.exit(f"  !! {size_mb:.1f} MB exceeds the {SIZE_LIMIT_MB} MB skill limit — slim the core's media.")
    if size_mb > SIZE_WARN_MB:
        print(f"  ! {size_mb:.1f} MB is close to the {SIZE_LIMIT_MB} MB limit.")
    print("\n  REINSTALL the .skill (Settings > Capabilities) — editing the dev "
          "source does not update the installed skill.")


if __name__ == "__main__":
    main()
