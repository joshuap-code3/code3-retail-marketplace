---
name: {SLUG}-deck-builder
description: Build decks for the {DISPLAY} account using {DISPLAY}'s own slide template{VOICE_DESC}. Use this skill whenever the team works on {DISPLAY} deliverables — creating, drafting, building, refreshing with new data, or re-skinning slides into {DISPLAY}'s template. Produces .pptx files using real {DISPLAY} template slides, not slides built from scratch.
---

# {DISPLAY} Deck Builder

Build {DISPLAY} client-facing presentations by **cloning real slides from the
{DISPLAY} template core** and editing their text content. Generating slides
from scratch with python-pptx reliably produces layout disasters — overlapping
text, wrong fonts, blank spots. The template slides already look correct; the
job is to pick the right ones and swap placeholder text for real content.

{VOICE_PARA}

## Three modes

Decide which one the request is before anything else — each has its own
workflow, manifest, and rules, documented in `references/modes.md`.

- **generate** — build a new deck from a brief, notes, or a transcript.
- **refresh** — update an existing {DISPLAY} deck with new data (new
  month/quarter). Structure preserved; content refreshed. Two mechanical hazards
  (repeating-value tables; image-position mapping) have dedicated helper scripts
  — read the refresh section of `references/modes.md` before touching a table or
  swapping an image.
- **re-skin** — remap an off-template deck onto {DISPLAY} template layouts.

### Story-first gate (generate mode)

Before the outline, generate mode agrees the deck's thesis and arc — analyze the
data, propose the throughline, pressure-test, sign off (workflow step 2; method
in `references/narrative.md`). Don't pick slides before the story is signed off.

### Outline-first gate (default)

Produce a manifest/outline in chat and get explicit sign-off before any XML
edits or file writes. The manifest is the cheap checkpoint. Format is
mode-specific; see `references/modes.md`.

## The one rule that matters most

**Never build a slide from scratch. Always clone an existing template slide and
edit its text.** If no template slide fits: (1) reshape the content to fit one
that does, or (2) pick a simpler layout. When you reshape or drop content for
lack of a fitting layout, log it with `scripts/log_miss.py` (see
`references/extending_library.md`). Do not reach for python-pptx primitives
to add shapes, text boxes, or images from scratch. The template slides are the
source of truth for every visual choice — fonts, sizes, colors, spacing, logo
placement. You are picking and filling, not designing.

## Workflow

1. **Understand the request** — audience (external/internal), deck type, source
   content, length, client/timeframe/logo. If thin, ask 1–3 questions first.
2. **Find the throughline (story-first gate)** — generate mode. Analyze the
   data, propose one thesis + a 3–5 beat arc, pressure-test it, and get sign-off
   on the Narrative manifest *before* picking slides (method in
   `references/narrative.md`; manifest format in `references/modes.md`). Scale it
   to the input: a handed-over thesis collapses to a one-line confirm; a data
   dump gets the full pass. Mark strategic opinions `[CALLOUT: human POV needed]`.
3. **Plan the slide sequence** against `assets/SLIDE_INDEX.md` and
   `references/slide_patterns.md`. Produce a per-slide plan and get a thumbs-up
   (the outline-first gate). Match each slide's shape to the content's shape;
   prefer simpler layouts; don't repeat one layout >3× in a row; respect text
   limits noted in the index. **Charts that must match real numbers go on the
   chart-canvas slide your `SLIDE_INDEX.md` designates** (a slide with a raster
   image box, filled with a `scripts/make_chart.py` PNG) — template "chart"
   slides whose bars/donuts are fixed vector shapes are decorative only and will
   visually contradict real data.
4. **Initialize the working deck** on the local filesystem (e.g.
   `/tmp/{SLUG}-deck-builder_build/deck_name`), NOT inside a mounted workspace
   (deletion is sometimes blocked there, which breaks finalize):
   ```bash
   python scripts/new_deck.py /tmp/{SLUG}-deck-builder_build/deck_name
   python scripts/map_slides.py /tmp/{SLUG}-deck-builder_build/deck_name_unpacked
   ```
   `SLIDE_INDEX.md` positions are presentation order, **NOT** the `slideN.xml`
   filename. Always edit the file `map_slides.py` reports for a position.
   **Cowork note:** the working dir must be on `/tmp` (deletable), but the
   `Edit`/`Read` tools can't reach `/tmp` — so make ALL slide-text edits with
   `scripts/refresh_text.py`, not the `Edit` tool. Copy QA JPGs to the mounted
   folder to view them.
5. **Build the slide order** — edit `ppt/presentation.xml`'s `<p:sldIdLst>` to
   keep exactly the slides you want, in order. Duplicate a layout with the pptx
   skill's `add_slide.py`. Complete all structural changes before editing text.
6. **Edit the content** — replace every placeholder (titles, eyebrows, body,
   bullets, column subtitles, stat numbers/labels, callouts, source citations,
   footers). Use `Edit` for one-off slots; use `scripts/refresh_text.py`
   (position-aware) for tables/stat grids with repeating values — `Edit` or
   `str.replace` corrupts repeating cells. Never leave a column/cell blank;
   switch layouts instead. When swapping a chart/image PNG into a `<p:pic>`,
   map it by EMU position (`scripts/inspect_images.py`), aspect-match the PNG,
   and **strip any `<a:srcRect>` crop** from the blipFill (the tool flags it) or
   the PNG renders clipped. Scan each slide for leftover scaffolding with
   `python scripts/refresh_text.py <slide>.xml --list`.
7. **Finalize:** `python scripts/finalize.py /path/to/working/dir/deck_name`
   (cleans, packs, renders QA JPGs to `deck_name_qa/slide-N.jpg`).
8. **Visual QA — mandatory.** The first render is never correct. Inspect every
   slide image (subagent recommended) for overlaps, overflow, leftover
   placeholder text, empty cells, wrong client/date, uncited data, off-brand
   fonts/colors. Fix, re-finalize, re-inspect until a full pass is clean.
9. **Deliver** — move the final `.pptx` and the `.pdf` (`finalize.py` renders
   one) to the user's workspace and link them. Note any `[DRAFT …]` /
   `[CALLOUT: …]` human-fill slots that remain; these MUST be cleared before the
   deck goes to a client.

## Hard rules

1. Never use python-pptx / pptxgenjs to construct slides. Only XML edits to
   existing template slides. (Regenerating a chart PNG to swap into an image slot
   is fine.)
2. Never resize, recolor, or reposition shapes/text boxes. Change the content or
   pick a different slide.
3. Never leave placeholder text in the final deck (Lorem ipsum, "Click to add",
   "SECTION TITLE", "xx", "0%", "Subtitle", default "Month Year", etc.).
4. Never repeat the same layout more than 3× in a row.
5. Never ship data without a source citation and date range.
6. Never edit a repeating-value table with `Edit` or `str.replace`. Use
   `scripts/refresh_text.py`.
7. Never skip visual QA.
8. Never generate a slide from scratch because "nothing fits." Simplify content
   until it fits the closest template slide.
9. Never pick slides before the throughline is signed off (generate mode). The
   deck is an argument; structure follows the agreed story. See
   `references/narrative.md`.

## Reference files

| File | When to read |
|------|--------------|
| `references/modes.md` | First — confirm the mode, its manifest format, its rules |
| `references/narrative.md` | Generate mode — find the data-backed throughline before picking slides |
| `assets/SLIDE_INDEX.md` | When picking slides for the plan |
| `references/brand.md` | Voice, colors, fonts, logo rules. Read before writing copy. |
| `references/slide_patterns.md` | Deck recipes. Read when planning the slide order. |
| `references/content_guidelines.md` | How to write titles, stats, citations, callouts |
| `references/quality_checks.md` | QA checklist |

## Working files

- Template core: `assets/{SLUG}_template_core.pptx`
- Chart colors: `assets/brand_palette.json` (read by `make_chart.py`; else the
  core's own theme colors are used)
- Scripts: `new_deck.py`, `new_slide.py` (single-slide: standalone + insert/
  replace), `finalize.py`, `map_slides.py`, `refresh_text.py`, `inspect_images.py`,
  `make_chart.py` (pie/donut/bar/hbar/grouped/stacked/line/funnel + per-deck
  rollup history), `lint_deck.py` (read-only brand/QA audit),
  `log_miss.py` (library-gap log). They locate the pptx skill's `scripts/`
  automatically; if not, set `CODE3_PPTX_SCRIPTS`.
