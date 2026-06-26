#!/usr/bin/env python3
"""Finalize a Code3 deck: clean, pack, and render for visual QA.

Usage:
    python finalize.py <output-basename>

Given a working deck <basename> (expects <basename>_unpacked/ next to where
the final .pptx will go), this script:

1. Runs clean.py on <basename>_unpacked/ — removes orphaned slides, media,
   relationships, and content-type overrides (anything the user cut in step 4
   of the workflow).
2. Runs pack.py to re-zip the unpacked dir into <basename>.pptx with schema
   validation against the original template.
3. Renders <basename>.pptx to PDF via LibreOffice.
4. Converts the PDF to individual JPGs in <basename>_qa/slide-N.jpg for
   subagent visual review.

Every step prints progress. Any failure halts the script with a clear error.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    basename = sys.argv[1]
    basename_path = Path(basename).resolve()
    out_pptx = basename_path.with_suffix(".pptx")
    unpacked = basename_path.parent / f"{basename_path.name}_unpacked"
    qa_dir = basename_path.parent / f"{basename_path.name}_qa"

    if not unpacked.exists():
        print(f"ERROR: unpacked dir not found at {unpacked}")
        print("Did you run new_deck.py first? Or is the basename wrong?")
        sys.exit(1)

    # Safety net: sweep stray backup/junk files that would ship as junk or fail
    # pack validation (e.g. refresh_text.py backups accidentally left in-tree).
    for pattern in ("*.bak", "*.orig", "*~"):
        for junk in unpacked.rglob(pattern):
            try:
                junk.unlink()
                print(f"  swept stray file: {junk.relative_to(unpacked)}")
            except OSError:
                print(f"  WARNING: could not remove {junk} (delete it before packing)")

    skill_dir = Path(__file__).resolve().parent.parent
    import glob as _glob
    _cores = sorted(_glob.glob(str(skill_dir / "assets" / "*template_core*.pptx")))
    template = Path(_cores[0]) if _cores else (skill_dir / "assets" / "code3_template_core.pptx")
    pptx_scripts = find_pptx_scripts_dir()
    if not pptx_scripts:
        print("ERROR: could not locate the pptx skill's scripts/ directory.")
        print("Set CODE3_PPTX_SCRIPTS to the pptx skill's scripts/ dir, or install")
        print("the pptx skill where this script can find it (searched")
        print("/sessions/*/mnt/.claude/skills/pptx/scripts, ~/.claude/..., /root/...).")
        sys.exit(1)

    # --- 1. Clean --------------------------------------------------------
    clean_script = pptx_scripts / "clean.py"
    print(f"[1/4] Cleaning orphans in {unpacked}")
    subprocess.check_call(["python", str(clean_script), str(unpacked)])

    # --- 2. Pack ---------------------------------------------------------
    pack_script = pptx_scripts / "office" / "pack.py"
    print(f"[2/4] Packing → {out_pptx}")
    pack_cmd = [
        "python",
        str(pack_script),
        str(unpacked),
        str(out_pptx),
    ]
    if template.exists():
        pack_cmd.extend(["--original", str(template)])
    subprocess.check_call(pack_cmd, cwd=str(pptx_scripts / "office"))

    # --- 3. Render PDF ---------------------------------------------------
    # LibreOffice needs a writeable TMPDIR / HOME in sandbox envs. Default
    # TMPDIR may be a stale host path — override to a dir we know exists.
    tmpdir = basename_path.parent / f".{basename_path.name}_sofficetmp"
    tmpdir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TMPDIR"] = str(tmpdir)
    env["HOME"] = str(tmpdir)

    soffice_script = pptx_scripts / "office" / "soffice.py"
    print(f"[3/4] Converting {out_pptx.name} → PDF")
    subprocess.check_call(
        [
            "python",
            str(soffice_script),
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_pptx.parent),
            str(out_pptx),
        ],
        env=env,
    )
    out_pdf = out_pptx.with_suffix(".pdf")
    if not out_pdf.exists():
        print(f"ERROR: PDF conversion produced no output at {out_pdf}")
        sys.exit(1)

    # --- 4. PDF → JPGs ---------------------------------------------------
    if qa_dir.exists():
        shutil.rmtree(qa_dir)
    qa_dir.mkdir(parents=True)
    print(f"[4/4] Rendering pages → {qa_dir}/slide-*.jpg")
    subprocess.check_call(
        [
            "pdftoppm",
            "-jpeg",
            "-r",
            "150",
            str(out_pdf),
            str(qa_dir / "slide"),
        ]
    )

    jpgs = sorted(qa_dir.glob("slide-*.jpg"))

    # Human-fill markers ([CALLOUT...] / [DRAFT...]) are intentional placeholders
    # for the account team. They're fine in an internal handoff but MUST be
    # cleared before the deck goes to a client, so surface any that remain.
    import re as _re
    pending = []
    for sx in sorted((unpacked / "ppt" / "slides").glob("slide*.xml")):
        body = sx.read_text(encoding="utf-8", errors="ignore")
        for mk in _re.findall(r"\[(?:CALLOUT|DRAFT)[^\]]*\]", body):
            pending.append((sx.name, mk))

    print()
    print("Done.")
    print(f"  Final deck: {out_pptx}")
    print(f"  PDF:        {out_pdf}  (deliver alongside the .pptx)")
    print(f"  QA images:  {qa_dir}/ ({len(jpgs)} slide images)")
    if pending:
        print()
        print(f"  !! {len(pending)} human-fill marker(s) still in the deck "
              "-- CLEAR before client delivery:")
        for name, mk in pending:
            print(f"       {name}: {mk}")
    print()
    print("Next: visually inspect every slide-*.jpg (subagent recommended).")
    print("      See SKILL.md step 7 for the review prompt.")


def find_pptx_scripts_dir():
    """Find the pptx skill's scripts/ directory, portably across machines."""
    import glob

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


if __name__ == "__main__":
    main()
