# Extending the template library (dev-time, not per-deck)

The core is **demand-driven**: it grows only when a slide *shape* keeps coming up
that no existing template can hold. `scripts/log_miss.py` records those gaps to a
workspace `_miss_log.md` during real builds. When a shape recurs in that log,
promote it — by **transplanting** a matching slide from the full Code3 template
into the core. This is a deliberate maintenance task, never something done while
building a client deck.

> **Judge a candidate by SHAPE, not content.** A slide earns a slot because its
> *layout* fills a gap, not because of what it happens to say. A "chart" that is a
> static image is just a text+image layout (already covered) — not a chart gap.

## Open candidates

1. **Two-channel battlecard with a proof-stat row + targeting pills** — the shape
   both the human and the model independently reached for on the OUAI search pitch,
   which slide 46 can only partly hold (it carries header + plays, not the per-channel
   3-stat row *and* pill sets). If the miss log shows it recurring, transplant it.
2. ~~**Wide landscape chart canvas** (logged 2026-06-09)~~ — **RESOLVED 2026-06-11.**
   The approved "Great Slide Examples" deck supplied it natively (no geometry
   surgery needed): core **slide 65** now carries an 8.74×2.34 in landscape raster
   canvas (plus dual canvases on 69 and a hero canvas on 70), srcRect pre-stripped.

## Curation pools

Two approved sources, in priority order:

1. **The full Code3 template** (125 slides) — `_template_archive/code3_template_core_FULL_animated.pptx`. Blank layout shells.
2. **The "Great Slide Examples" deck** — `examples_v2/2026-06-11_Great-Slide-Examples.pptx`, Jack-approved 2026-06-11. Real client-work slides (richer shapes than the blank template), all 13 content slides already promoted as core 64–76. If a future approved examples deck lands, transplant from it the same way — but **neutralize harder**: client copy → placeholders, client imagery → gray boxes (keep generic platform icons), normalize fonts to Barlow/Kalam.

## The transplant technique (full template → core)

Source of truth for the curation pool: the full Code3 template (125 slides) in
`_template_archive/` (`code3_template_core_FULL_animated.pptx`). The full template
and the core **share the identical `theme1` color scheme and the same
`slideLayouts`**, so a transplant renders pixel-identical and is purely mechanical:

1. **Pick the source slide** in the full template (presentation order via
   `map_slides.py`). Confirm its *shape* fills a real, logged gap.
2. **Copy its slide XML** → core `ppt/slides/slide{N}.xml` (next free number).
3. **Media:** copy referenced media into the core, renaming to avoid collisions
   (e.g. `image901+`); **neutralize client photos** to `#C9C9C9` boxes at original
   px size; rewrite the slide's rels to the renamed media.
4. **Drop the `notesSlide` rel** (orphan notes break packing / can leak content).
4b. **Tables: merge the style.** If the slide carries an `<a:tbl>` with a
   `<a:tableStyleId>`, copy the matching `<a:tblStyle>` from the source's
   `ppt/tableStyles.xml` into the core's — a dangling tableStyleId **crashes
   LibreOffice rendering outright** ("Unspecified Application Error"); found the
   hard way on the creative-audit transplant (core slide 76, 2026-06-11).
5. **Layout:** point the slide's layout rel at the core's existing same-named
   `slideLayoutNN.xml` — do **no** layout/master surgery (they're byte-identical).
6. **Register** the slide in `ppt/presentation.xml` `sldIdLst`,
   `ppt/_rels/presentation.xml.rels`, and `[Content_Types].xml` (Override).
7. **Blank any client-specific copy** to neutral placeholders (this is a template
   slide now, not a one-off). Reword stray "Lorem ipsum".
8. **Repack** (`zip -r -9 -X`) and **render-QA** (LibreOffice → `pdftoppm`) the new
   slide; diff theme/layout to confirm pixel parity.
9. **Index it** in `assets/SLIDE_INDEX.md` (position, file, purpose, placeholders,
   constraints) — *index quality is the real constraint on how big the core can
   grow*, not slide count. Add cover/agenda/divider variants too so high-recurrence
   layouts don't go stale (the "no same layout 3× in a row" rule).

`scripts/new_slide.py`'s `transplant()` is a working reference for the *mechanics*
of the same registration steps (it does core→deck; this does full→core).

## Backups

Before changing the core, copy the current `code3-deck-builder.skill` and the
`assets/*_template_core.pptx` into `_template_archive/` with a dated suffix, like
the existing `_pre-charts_`, `_pre-single-slide_`, `_pre-lint_` snapshots. Then
repackage the `.skill` (SKILL.md at archive root) and reinstall.
