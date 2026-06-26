---
name: code3-deck-builder
description: Build client-facing presentations that follow Code3's brand guidelines, visual system, and slide templates. Use this skill whenever a Code3 team member asks you to create, draft, build, or put together a deck, slides, presentation, pitch, QBR, capabilities overview, strategy recommendation, or any other slide-based document — even if they don't explicitly say "Code3-branded." Also use it when editing or refreshing an existing Code3 deck with new data, when someone asks you to "make this look on-brand," or when someone wants to turn notes, a brief, or meeting content into slides. This skill produces .pptx files using real Code3 template slides, not slides built from scratch.
---

# Code3 Deck Builder

Build Code3-branded client-facing presentations by **cloning real slides from the Code3 template** and editing their text content. This skill exists because generating slides from scratch with python-pptx or pptxgenjs reliably produces layout disasters — overlapping text, wrong fonts, blank spots. The template slides have been designed by Code3 and already look correct; the job is to pick the right ones and swap the placeholder text for real content.

## Three modes

This skill runs in one of three modes. **Decide which one the request is before anything else** — each has its own workflow, manifest, and rules, documented in `references/modes.md`.

- **generate** — build a new deck from a brief, notes, or a transcript.
- **refresh** — update an existing Code3 deck with new data (new month/quarter). Structure is preserved; content is refreshed. Refresh works on the *existing* deck — you unpack it directly and do NOT use `new_deck.py`. It has two mechanical hazards (repeating-value tables; image-position mapping) with dedicated helper scripts — read the refresh section of `references/modes.md` before touching a table or swapping an image.
- **re-skin** — remap an off-brand deck onto Code3 template layouts.
- **configure** — *not a deck-building mode.* Spawn a new branded `<name>-deck-builder` skill for another Graham Holdings org (full brand suite) or a client account (their template, Code3 voice — e.g. LVMH). Produces an installable `.skill`, not a deck. Requires an **editable `.pptx` core** (a PDF cannot be cloned). Fully documented in `references/configuration.md`; follow that file instead of the 9-step workflow below.

Read `references/modes.md` for a deck-building mode's workflow, its in-chat manifest format, and its rules once you know the mode. The 9-step workflow below is the generate-mode core; refresh and re-skin adapt it as `modes.md` describes. **For configure mode, follow `references/configuration.md`.**

For one-off **single-slide** work — make a single slide, or add/replace a slide in an existing Code3 deck — see the single-slide section of `references/modes.md`. It is a lightweight path (not a full mode): it **skips the throughline gate** and uses `scripts/new_slide.py`.

To **audit** an existing deck without changing it — a pre-delivery brand/QA check, or a deck someone else built — use `scripts/lint_deck.py` (read-only; reports leftover placeholders, off-brand fonts, AI-tells, uncited data). See the lint section of `references/modes.md`.

### Named parameters

Set in the request or proposed in the manifest:

- **slide count** — target number of slides (proposed; reduce/expand on request).
- **include-cover** — open with a cover slide (default: yes).
- **include-closing** — end with a closing recommendation/CTA slide (default: yes). Code3's closing is a CTA with concrete commitments, never a "thank you" slide.

### Story-first gate (generate mode)

Before the outline, generate mode agrees the deck's **thesis and arc** — analyze the data, propose the throughline, pressure-test it, get sign-off (workflow step 2; method in `references/narrative.md`). Picking slides before the story is signed off is the failure this gate exists to prevent.

### Outline-first gate (default behavior)

**By default, produce a manifest/outline and get explicit sign-off before any XML edits or file writes.** The manifest is the cheap checkpoint — the place the account team catches misalignment before tokens go into slide work. The format is mode-specific; see `references/modes.md`.

**Deliver the manifest in chat, not as a file**, unless the user asks for a file or it is genuinely too long for chat. A long markdown manifest is friction that kills adoption.

## The one rule that matters most

**Never build a slide from scratch. Always clone an existing template slide and edit its text.**

If no template slide fits the content, you have two options — in this order:
1. **Reshape the content** to fit a slide that does fit (fewer bullets, shorter text, different grouping).
2. **Pick a simpler layout** (a single body-text slide is better than a broken custom layout).

When you reshape or drop content because no layout fit, **log the gap** so the library can grow to cover it: `python scripts/log_miss.py --deck "<name>" --shape "<what the content needed>" --used "<fallback / what you dropped>" --log "<workspace>/_miss_log.md"`. When a shape recurs in that log it earns a transplanted template — see `references/extending_library.md`.

Do not reach for python-pptx primitives to add shapes, text boxes, or images from scratch. That's how the previous version of this skill broke. The template slides are the source of truth for every visual choice — fonts, sizes, colors, spacing, logo placement. You are picking and filling, not designing.

## Dense / high-density layouts (explicit request only)

The library includes seven high-density layouts — **slides 46–49** (battlecard, search-intent matrix, two-section data table, case study) and **slides 64, 72, 76** (3-persona audience matrix, test/study one-pager, 4-column creative audit; see `assets/SLIDE_INDEX.md`). They pack several slides' worth of content onto one canvas — for situations like a hard slide-count cap (e.g. a 20-slide pitch) where the team must run dense.

These are **off by default.** Keep preferring the simpler layouts; density is a last resort, not a habit. Reach for them only when:
- the user **explicitly asks** for a denser or specific layout ("I need this on one slide," "match this battlecard," "we're capped at 20 slides"), or
- a stated **constraint** genuinely forces it.

They are still real template slides: **clone and fill, never build from scratch, never resize or reposition shapes.** The dense templates extend the "no template fits" ladder (reshape → simpler layout) — they don't replace it. If content is denser still than they can hold, reshape or split it across slides; do not stretch, recompose, or invent a layout.

**Pick the right dense layout by shape, not topic.** 46 is a two-column battlecard (Channel-A-vs-B / Us-vs-Them, 3 items each); 47 is a *single*-audience search-intent cluster grid; 48 is a ranked two-section data table; 49 is a one-case-study results slide. A slide that compares two channels and also carries stat rows + tag/pill sets (e.g. the OUAI "Google vs Social" search slide) has no single exact home — map it to 46 and **trim the density** (fold proof stats into the so-what lines; drop or compress pill sets), or split across slides. Say in the delivery note what you dropped, and log the gap with `scripts/log_miss.py` so a matching dense template can be added if the shape recurs (`references/extending_library.md`).

**Citing on dense layouts:** only slide 48 has a source-citation slot. On **46, 47, 49** put the source in the `SECTION TITLE` eyebrow (e.g. "… · SOURCE: …") rather than adding a text box; if it won't fit, flag the citation in the delivery note. (Details in `assets/SLIDE_INDEX.md` → "Citing on dense layouts.") The newer dense slides have their own slots: 64 a source eyebrow under the title, 72 none (flag in delivery note), 76 the eyebrow.

## Workflow

### 1. Understand the request

Before picking any slides, know the answers to:
- **Audience.** Is this a client (external) or internal (all-hands, team sync)? The tone and disclosure level differ sharply — see `references/brand.md`.
- **Deck type.** QBR, new-business pitch, capabilities overview, strategy recommendation, kickoff, one-off presentation? See `references/slide_patterns.md` for the standard shape of each.
- **Source content.** Brief? Raw notes? Transcripts? A previous deck? Are there data points, and if so, what time range and source?
- **Length.** Rough slide count or "as long as it needs to be"?
- **Client name, timeframe, and logo** (if client-facing).

If the user's request is thin, ask 1–3 targeted clarifying questions before starting. Don't guess on audience or deck type — those choices shape everything else.

### 2. Find the throughline (story-first gate)

**Generate mode: agree the story before picking any slides.** A deck is an argument, not a slide container. Read `references/narrative.md` and run its gate:

1. **Analyze the data** (don't parrot it) — movement (MoM/QoQ/YoY), pacing vs. goal, efficiency, mix shifts, outliers. Produce a short findings list: each a number + context + candidate so-what. Only compute what the data supports; flag gaps, never invent.
2. **Propose one thesis** — the single sentence the room should leave repeating — plus a **3–5 beat arc** that proves it. Each beat carries its claim, evidence, and so-what.
3. **Pressure-test and sign off.** Present a compact Narrative manifest (format in `references/modes.md`), bring a POV to react to (not "what do you want?"), and get explicit agreement on the thesis + arc.

**Scale it to the input:** if the brief already states the point, restate it in one line, confirm, and move on — don't interrogate. Go deep only when handed a data dump. Mark any strategic opinion (the recommended bet, a hot take) `[CALLOUT: human POV needed]` — you assert what the data says, not Code3's judgment (`brand.md`).

### 3. Plan the slide sequence

With the throughline signed off, map each beat to slides. Open `assets/SLIDE_INDEX.md` — it describes every template slide with purpose, visual character, and placeholder structure (the index is the source of truth for how many slides the core currently holds). Also open `references/slide_patterns.md` for deck-level recipes.

Produce a plan in this form before touching any files:

```
Slide 1: Title cover (template slide 1) — client logo + title + month/year
Slide 2: Agenda (template slide 5) — 5 agenda items
Slide 3: Section divider (template slide 7) — "Q1 Performance"
Slide 4: Key takeaways (template slide 11) — 3 big sentences
... etc.
```

Show this plan to the user and get a thumbs up before building. This is the outline-first gate — cheap (text) and it catches misalignment before you spend tokens on XML edits. See `references/modes.md` for the exact manifest format for the mode you're in.

**Picking slides — guidelines that save you from the most common failures:**

- **Match the slide's shape to the content's shape.** A 3-column slide needs 3 roughly parallel items, similar length. If the user's content has 3 items of wildly different depth, pick a 1-column layout or three separate slides instead. Don't force imbalance into a grid.
- **Prefer simpler layouts.** A clean title + paragraph slide (template slides 18, 20) beats a broken 6-column stat grid. Only use the dense layouts when the data genuinely supports them.
- **Charts that must match real numbers go on a chart canvas with a `make_chart.py` PNG** — slide 15 (portrait) or the landscape canvases **65, 69 (dual), 70** — the "data chart" slides 32–33 are fixed vector decorations whose proportions don't change with your values (fine for qualitative framing, misleading for real data). Pick by orientation/shape: 12-month trend lines → 65; attribution with two stacked trends → 69; hero chart + corroborating stat pills → 70. See the chart bullet in `references/modes.md` generate-mode rules.
- **Don't repeat the same layout four times in a row.** Vary between text, image, data, and split layouts — see the patterns file. For the slides a deck reuses most — **covers, agendas, and section dividers** — the library carries several interchangeable styles (see `assets/SLIDE_INDEX.md`); rotate them so repeated dividers/covers don't look identical.
- **Respect text-length constraints.** Each slide in the index notes approximate placeholder limits. If the user's content won't fit, pare it down or split across two slides. Do not overflow.

### 4. Initialize the working deck

Create a working directory **on the local filesystem** — e.g. `/tmp/code3_build/deck_name` — **NOT inside the mounted workspace/outputs folder.** Some Cowork mounts block file deletion, which makes `clean.py`/`pack.py` fail mid-finalize. Build in `/tmp`, then copy only the final `.pptx` and QA JPGs to the workspace at the end (step 9). Initialize:

```bash
python scripts/new_deck.py /tmp/code3_build/deck_name
```

This copies `assets/code3_template_core.pptx` to `deck_name.pptx` in the working dir, and creates a `deck_name_unpacked/` alongside it (the template already unpacked). Every template slide file is present under `deck_name_unpacked/ppt/slides/` and ready to be cloned, kept, or removed.

**Then get the position→file map — do not skip this:**

```bash
python scripts/map_slides.py /tmp/code3_build/deck_name_unpacked
```

`SLIDE_INDEX.md` positions are **presentation order**, which is **NOT** the `slideN.xml` filename (position 1 is `slide5.xml`, position 8 is `slide17.xml`, etc.). Always edit the content file that `map_slides.py` reports for a given index position — never assume "slide N" means `slideN.xml`.

**Cowork environment note (important):** the working dir must be on `/tmp` (deletable), but the `Edit`/`Read` tools only reach the mounted folders — they **cannot** touch files under `/tmp`. So in Cowork, make ALL slide-text edits with `scripts/refresh_text.py` instead of the `Edit` tool: it handles one-off slots via `{"find": "PRESENTATION TITLE", "occurrence": 1, "replace": "..."}` and repeating-value cells via `{"index": N}`. Copy QA JPGs to the mounted folder to view them with `Read`. (Outside Cowork — a normal local checkout where the tools and shell share a filesystem — you can build in place and use the `Edit` tool exactly as step 6 describes.)

### 5. Build the slide order

Decide which template slides to keep, in which order, and which to duplicate if a layout is used multiple times (e.g. two section dividers back-to-back, or three identical 3-column content slides in a row).

Edit `deck_name_unpacked/ppt/presentation.xml` to rebuild the `<p:sldIdLst>` block with exactly the slides you want, in the order you want.

- **Slide already in template, want to use once:** just keep its `<p:sldId>` in the list; reorder as needed.
- **Slide needed more than once:** use `python <pptx-scripts>/add_slide.py deck_name_unpacked/ slideN.xml` to duplicate it — where `slideN.xml` is the **actual file** for the SLIDE_INDEX position you want, per `map_slides.py` (positions are NOT filenames). The script prints a new `<p:sldId>` element — paste it into the `<p:sldIdLst>` at the right position. (`<pptx-scripts>` is the pptx skill's `scripts/` dir; `finalize.py` finds it automatically, or set `CODE3_PPTX_SCRIPTS`.)
- **Slide not needed:** remove its `<p:sldId>` from the list.

**Complete all structural changes (order, duplicates, deletes) before editing any text.** Mixing structural and content changes makes mistakes much harder to spot.

### 6. Edit the content

Now open each slide's XML file in the order they'll appear in the deck and replace its placeholder text with real Code3 content.

**Use the `Edit` tool for one-off text slots** (titles, eyebrows, single paragraphs). Edit forces specificity about what you're replacing and where. This matters because template slides contain Lorem ipsum, "Click to add...", "SECTION TITLE", and similar scaffolding that absolutely must not ship to a client.

**For tables and stat grids with repeating values** (multiple `$0K`, `0%`, `—` cells), do NOT use `Edit` or `str.replace` — they corrupt repeating cells. Use the position-aware helper `scripts/refresh_text.py` (see the refresh section of `references/modes.md`). This applies to refresh mode especially, but to any dense table.

**For each slide:**

1. Read the slide XML and identify every placeholder — not just titles. Placeholders commonly include: slide title, section eyebrow, body paragraphs, bullet items, column subtitles, stat numbers, stat labels, callout text, footnote/source citations, footer text.
2. Replace each placeholder with real content that fits the slot's approximate length (see `SLIDE_INDEX.md` constraints).
3. For any placeholder image: either replace it (inspect positions first with `scripts/inspect_images.py` — see `modes.md`; when swapping in an aspect-matched chart PNG, strip any `<a:srcRect>` crop the tool flags or the chart renders clipped) or leave the template's image in place. If the slide's fixed graphic (e.g. a phone mockup) doesn't suit the deck, you should have picked a different slide in step 3.
4. If a slide has more slots than content (e.g. a 5-column slide but you only have 3 things to say), pick a different slide. Do NOT leave blank columns — that was a v1 failure mode.

Before declaring a slide done, dump its text runs and scan for leftover scaffolding. (`markitdown` only extracts text from a *packed* `.pptx`, not a bare slide part — for a single slide use `refresh_text.py --list`, which prints every text run cleanly:)
```bash
python scripts/refresh_text.py deck_name_unpacked/ppt/slides/slideN.xml --list
```
Watch for: `Lorem ipsum`, `Click to add`, `SECTION TITLE` (when not intended), `xx`, `Slide Title`, `Subtext`, `Subtitle`, `0%`, `Callout`, `Month Year` (when not updated), `TODO`, `[CALLOUT: …]`, `[DRAFT …]`. (For a whole-deck scan after packing: `python -m markitdown deck_name.pptx | grep -iE ...`, per `quality_checks.md`.)

Use the Code3 voice patterns in `references/brand.md` and the content conventions in `references/content_guidelines.md` when writing.

### 7. Finalize

```bash
python scripts/finalize.py /path/to/working/dir/deck_name
```

This runs `clean.py` to strip orphaned media/rels, runs `pack.py` to repackage into `deck_name.pptx` with validation, and renders the deck to individual JPGs at `deck_name_qa/slide-N.jpg` for visual QA.

### 8. Visual QA — mandatory

**Do not declare done without visual QA.** The first render is almost never correct.

Spawn a subagent (or, if no subagents available, view each slide image yourself with fresh eyes) with this prompt:

> Visually inspect slides 1–N at /path/to/working/dir/deck_name_qa/slide-*.jpg.
> Assume there are issues — find them. Look for: overlapping elements, text overflow or clipping, leftover placeholder text (Lorem ipsum, Click to add, SECTION TITLE, xx, Subtitle), empty columns or grid cells, wrong client name or date, data without source citations, off-brand fonts or colors, low-contrast text, title text wrapping into decorative elements.
> For each slide, list issues or flag as clean. Be critical.

Fix every issue found. Re-run `finalize.py`. Re-inspect. Repeat until a full pass reveals nothing new.

Common issues you WILL find on first pass, and how to fix:
- **Leftover Lorem ipsum or "Click to add":** You missed a text slot. Go back and edit it.
- **Text overflow:** Your content was too long. Shorten it, or switch to a more spacious layout.
- **Mismatched counts:** 5-column layout with only 3 filled columns. Switch to a 3-column layout (template slides 22–23).
- **Generic titles** ("Slide Title" left in): Edit the actual title text.
- **Missing source citation on a chart or stat:** Code3 always cites. Add it.
- **Scrambled table cells after a refresh:** You edited a repeating-value table with `Edit`/`str.replace`. Redo it with `scripts/refresh_text.py` (position-aware).

### 9. Deliver

Move the final `.pptx` **and the `.pdf`** (`finalize.py` renders one alongside it) to the user's workspace folder so they can see both, and link to them. The PDF is the quick-preview/share copy; the PPTX is the editable deliverable. Keep a short delivery note — maybe 2–3 sentences about what you built, plus any `[DRAFT …]` / `[CALLOUT: …]` human-fill slots the account team must complete (`finalize.py` lists any that remain). **These markers are fine for an internal/account-team handoff, but they render in the deck and MUST be cleared before it goes to a client.** The user can see the deck; don't re-explain every slide.

## Hard rules — these come from v1 failures

1. **Never use python-pptx, pptxgenjs, or any library to construct slides programmatically.** Only XML edits to existing template slides. (Generating/regenerating chart PNGs to swap into an image slot is fine; constructing slide layouts is not.)
2. **Never resize, recolor, or reposition shapes or text boxes** on template slides. If content doesn't fit, change the content or pick a different slide.
3. **Never leave placeholder text in the final deck.** Lorem ipsum, "Click to add", "SECTION TITLE", "xx", "0%", "Subtext", "Subtitle", "Slide Title", default "Month Year", etc. must all be replaced.
4. **Never repeat the same layout more than 3 times in a row.** The deck will feel monotonous.
5. **Never ship data without a source citation and date range.** Code3 house style.
6. **Never edit a repeating-value table with `Edit` or `str.replace`.** Use `scripts/refresh_text.py` (position-aware) or you will silently corrupt cells.
7. **Never skip visual QA.** First render is never correct.
8. **Never generate a slide from scratch because "nothing fits."** Simplify content until it fits the closest template slide.
9. **Never pick slides before the throughline is signed off (generate mode).** The deck is an argument; structure follows the agreed story. See `references/narrative.md`.

## Reference files

Read these as needed:

| File | When to read |
|------|--------------|
| `references/modes.md` | **First** — to confirm the mode, its manifest format, and its rules |
| `references/narrative.md` | **Generate mode** — find the data-backed throughline and run the story-first gate before picking slides |
| `assets/SLIDE_INDEX.md` | When picking slides for the plan |
| `references/brand.md` | Voice, colors, fonts, logo rules. Read before writing any copy. |
| `references/slide_patterns.md` | Deck recipes (QBR, pitch, capabilities, strategy rec). Read when planning the slide order. |
| `references/content_guidelines.md` | How to write titles, stats, source citations, callouts in Code3 house style |
| `references/quality_checks.md` | QA checklist with specific things to look for |
| `references/configuration.md` | **Configure mode only** — how to spawn a branded `<name>-deck-builder` variant for another org or client |
| `references/extending_library.md` | **Maintenance** — how the miss log + slide-transplant grow the core library (not a per-deck read) |

## Working files and paths

- Bundled template: `assets/code3_template_core.pptx` (curated slides from the full Code3 template; `assets/SLIDE_INDEX.md` lists the current set)
- Scripts:
  - `scripts/new_deck.py` — initialize a working deck from the template
  - `scripts/finalize.py` — clean, pack, render to JPGs for QA
  - `scripts/refresh_text.py` — position-aware text replacement for refresh mode (tables/stat grids with repeating values); also `--list` to dump a slide's text runs
  - `scripts/inspect_images.py` — list a slide's images by on-slide position + rId + media file, for safe image swaps
  - `scripts/map_slides.py` — print the position→`slideN.xml` map for an unpacked deck (positions are NOT filenames)
  - `scripts/make_chart.py` — generate brand-styled, transparent-background chart PNGs (pie, donut, bar, hbar, grouped, stacked, line, funnel) for refresh-mode chart swaps **and generate-mode charts on the slide-15 chart canvas**; aspect-matched to the target box; reads a per-deck rollup CSV for line/trend history and can append to it (`rollup-add`). Colors from `assets/brand_palette.json` if present, else Code3 defaults
  - `scripts/new_slide.py` — single-slide builds: clone one template slide into a 1-slide deck (`standalone`), or transplant/replace a slide in an existing Code3 deck (`insert … --at K [--replace]`). Bypasses the throughline gate; see the single-slide section of `references/modes.md`
  - `scripts/lint_deck.py` — read-only brand/QA audit of an existing `.pptx` (leftover placeholders, off-brand fonts, AI-tells, em-dash spray, uncited data); `--md` for a file, `--render` for the visual pass. Reports, never edits
  - `scripts/log_miss.py` — append a "no template fit" gap to the workspace `_miss_log.md`; drives demand-based library growth (`references/extending_library.md`)
- Configurator / maintenance scripts (not per-deck — see `references/configuration.md`):
  - `scripts/build_slide_index.py` — render an arbitrary core to thumbnails and scaffold its `SLIDE_INDEX.md`
  - `scripts/spawn_variant.py` — assemble + package a new `<name>-deck-builder.skill` from this skeleton; a variant's `SKILL.md` comes from `scripts/variant_skill_template.md` (edit it alongside this file when features land)
  - `scripts/package_skill.py` — one-command repackage of this skill (backup → zip with SKILL.md at archive root → verify size + run the SKILL.md↔variant-template drift check). Reinstall after packaging.
  - `scripts/smoke_test.py` — scripted regression build (clone → fill → chart swap → finalize → lint); run after any core/script/doc change, before repackaging
- The skill's scripts locate the pptx skill's `scripts/` directory automatically (they search the common install locations). If they can't find it, set the `CODE3_PPTX_SCRIPTS` environment variable to the pptx skill's `scripts/` directory.
