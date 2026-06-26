#!/usr/bin/env python3
"""Initialize a new Code3 deck from the bundled template.

Usage:
    python new_deck.py <output-basename>

This copies the bundled code3_template_core.pptx to <output-basename>.pptx in
the current working directory and unpacks it to <output-basename>_unpacked/
so you can edit slides directly.

The unpacked deck initially contains the full set of template slides. Your next step
is to edit <basename>_unpacked/ppt/presentation.xml to keep only the slides
you want, in the order you want them, following the workflow in SKILL.md.

After content edits, run:
    python finalize.py <output-basename>
"""

import shutil
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    basename = sys.argv[1]
    # Allow absolute or relative paths.
    basename_path = Path(basename)
    out_pptx = basename_path.with_suffix(".pptx")
    out_unpacked = basename_path.parent / f"{basename_path.name}_unpacked"

    # Create the working dir if needed (e.g. /tmp/code3_build/<name>).
    if str(basename_path.parent):
        basename_path.parent.mkdir(parents=True, exist_ok=True)

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    bundled_template = find_core(skill_dir)

    if bundled_template is None:
        print(f"ERROR: no *template_core*.pptx found in {skill_dir / 'assets'}")
        sys.exit(1)

    # Copy template to working location.
    print(f"Copying template → {out_pptx}")
    shutil.copy(bundled_template, out_pptx)
    # Bundled template is often read-only; shutil.copy preserves its mode, which
    # makes finalize.py/pack.py fail with EACCES when they overwrite this .pptx.
    out_pptx.chmod(0o644)

    # Unpack it using the pptx skill's unpack script if available, else fall
    # back to a local unzip.
    unpack_script = find_pptx_script("office/unpack.py")
    if unpack_script:
        print(f"Unpacking → {out_unpacked}")
        subprocess.check_call(
            ["python", str(unpack_script), str(out_pptx), str(out_unpacked)]
        )
    else:
        print("pptx skill's unpack.py not found; falling back to unzip.")
        out_unpacked.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(["unzip", "-q", str(out_pptx), "-d", str(out_unpacked)])

    # Print a quick summary of what the user now has.
    slides_dir = out_unpacked / "ppt" / "slides"
    slide_count = len(list(slides_dir.glob("slide*.xml"))) if slides_dir.exists() else 0
    print()
    print(f"Ready. You now have:")
    print(f"  {out_pptx}                    (packed .pptx, identical to template)")
    print(f"  {out_unpacked}/   (unpacked; {slide_count} slide XML files under ppt/slides/)")
    print()
    print("Next step: edit ppt/presentation.xml's <p:sldIdLst> to keep only the")
    print("slides you want, in the order you want. Consult assets/SLIDE_INDEX.md")
    print("to know which slide number is which layout.")


def find_core(skill_dir):
    """Find the bundled template core by glob, so any brand variant works."""
    import glob
    hits = sorted(glob.glob(str(skill_dir / "assets" / "*template_core*.pptx")))
    return Path(hits[0]) if hits else None


def find_pptx_scripts_dir():
    """Find the pptx skill's scripts/ directory, portably across machines."""
    import glob
    import os

    candidates = []
    env = os.environ.get("CODE3_PPTX_SCRIPTS")
    if env:
        candidates.append(Path(env))
    # Cowork sandbox: skills mount under /sessions/<name>/mnt/.claude/skills/
    candidates += [Path(p) for p in sorted(glob.glob("/sessions/*/mnt/.claude/skills/pptx/scripts"))]
    candidates += [
        Path.home() / ".claude/skills/pptx/scripts",
        Path("/root/.claude/skills/pptx/scripts"),
    ]
    for c in candidates:
        if c and c.exists():
            return c
    return None


def find_pptx_script(relative_path):
    """Find a script (e.g. 'office/unpack.py') under the pptx skill's scripts/."""
    base = find_pptx_scripts_dir()
    if base is None:
        return None
    c = base / relative_path
    return c if c.exists() else None


if __name__ == "__main__":
    main()
