#!/usr/bin/env python3
"""Inspect the images on a PPTX slide by on-slide POSITION, not filename.

Why this exists
---------------
When refreshing a deck you often regenerate a chart PNG and swap it into the
slide. Picking which media file to replace by its `imageN.png` filename is
unreliable -- the numbering varies slide to slide, and guessing transposes
images (on the CDC refresh, a pie chart and a traffic card rendered swapped).
Geometry is the source of truth. This prints every picture on a slide with its
position and size in EMU and inches, plus the relationship id and the media
file it currently points to, so you map regenerated images by coordinates.

Usage
-----
    python inspect_images.py SLIDE_XML

SLIDE_XML is e.g. deck_unpacked/ppt/slides/slide7.xml. The matching rels file
(ppt/slides/_rels/slide7.xml.rels) is located automatically.

EMU = English Metric Units. 914400 EMU = 1 inch.
"""

import os
import sys
import xml.etree.ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
EMU_PER_INCH = 914400.0


def load_rels(slide_path):
    """Map relationship id -> target media path for the slide's rels file."""
    d = os.path.dirname(slide_path)
    base = os.path.basename(slide_path)
    rels_path = os.path.join(d, "_rels", base + ".rels")
    rid_to_target = {}
    if not os.path.exists(rels_path):
        return rid_to_target, rels_path
    tree = ET.parse(rels_path)
    for rel in tree.getroot().findall("rel:Relationship", NS):
        rid_to_target[rel.get("Id")] = rel.get("Target")
    return rid_to_target, rels_path


def emu(val):
    try:
        n = int(val)
    except (TypeError, ValueError):
        return None
    return n


def fmt(n):
    if n is None:
        return "?"
    return f"{n} ({n / EMU_PER_INCH:.2f}in)"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    slide_path = sys.argv[1]

    rid_to_target, rels_path = load_rels(slide_path)
    tree = ET.parse(slide_path)
    root = tree.getroot()

    pics = root.findall(".//p:pic", NS)
    if not pics:
        print(f"No <p:pic> elements found in {slide_path}.")
        return

    rows = []
    for pic in pics:
        cnv = pic.find(".//p:nvPicPr/p:cNvPr", NS)
        name = cnv.get("name") if cnv is not None else "?"
        blip = pic.find(".//a:blip", NS)
        embed = blip.get("{%s}embed" % NS["r"]) if blip is not None else None
        target = rid_to_target.get(embed, "?")

        off = pic.find(".//p:spPr/a:xfrm/a:off", NS)
        ext = pic.find(".//p:spPr/a:xfrm/a:ext", NS)
        x = emu(off.get("x")) if off is not None else None
        y = emu(off.get("y")) if off is not None else None
        cx = emu(ext.get("cx")) if ext is not None else None
        cy = emu(ext.get("cy")) if ext is not None else None

        # srcRect = a crop applied to the fill image (values are 1/1000 %).
        # A photo cropped 40% from the left will crop a swapped-in chart PNG
        # identically -- the chart renders clipped. Report it so the swap
        # workflow knows to REMOVE the <a:srcRect> when inserting a chart
        # that is already aspect-matched to the box.
        src = pic.find(".//p:blipFill/a:srcRect", NS)
        crop = None
        if src is not None:
            parts = []
            for side in ("l", "t", "r", "b"):
                v = src.get(side)
                if v and v != "0":
                    parts.append(f"{side}={int(v)/1000:.1f}%")
            crop = " ".join(parts) if parts else None
        rows.append((y, x, name, embed, target, cx, cy, crop))

    # Sort top-to-bottom, then left-to-right -- matches how you read a slide.
    rows.sort(key=lambda t: (t[0] is None, t[0] or 0, t[1] or 0))

    print(f"Slide: {slide_path}")
    print(f"Rels:  {rels_path}")
    print(f"{len(pics)} picture(s), ordered top->bottom, left->right:\n")
    for y, x, name, embed, target, cx, cy, crop in rows:
        print(f"  name : {name}")
        print(f"  rId  : {embed}  ->  {target}")
        print(f"  pos  : x={fmt(x)}  y={fmt(y)}")
        print(f"  size : w={fmt(cx)}  h={fmt(cy)}")
        if crop:
            print(f"  crop : srcRect {crop}  <-- REMOVE the <a:srcRect> if swapping in an aspect-matched chart PNG, or it will render clipped")
        print()


if __name__ == "__main__":
    main()
