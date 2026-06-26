# Build Modes — generate / refresh / re-skin

The deck builder runs in one of three modes. **Identify the mode before doing anything else** — each has its own workflow, its own manifest, and different rules about what the model may and may not change.

| Mode | Triggered by | What it does |
|------|--------------|--------------|
| **generate** | "build / create / put together a deck from this brief / these notes" | New deck assembled from the template library. |
| **refresh** | "update this deck with new data / the new month / the new quarter" | An existing Code3 deck + new data. Structure is preserved; content is refreshed. |
| **re-skin** | "make this off-brand deck look like Code3 / on-brand" | A non-Code3 deck remapped onto Code3 template layouts. |

If the request is ambiguous between modes, ask. The most common confusion is refresh vs. re-skin: refresh starts from a deck that is *already* a Code3 template; re-skin starts from a deck that is *not*.

---

## The outline-first gate (default for every mode)

**Default behavior: produce a manifest and get explicit sign-off BEFORE any XML edits or file writes.** The manifest is the cheap checkpoint where the account team catches misalignment before tokens are spent on slide work. Restructuring ("drop slide 4," "merge 6 and 7," "swap the strategist in for the callouts") costs nothing here and a lot later.

**Deliver the manifest in chat, not as a file.** A long markdown manifest file is friction that kills adoption — nobody re-reads a 200-line document every time they call the skill. Keep it to a compact table plus a short bullet list of confirmations and open questions inline. Use a file *only* if the user explicitly asks, or if the manifest genuinely exceeds what's reasonable in chat.

> The on-disk `CDC_refresh_manifest.md` from the first refresh test is a cautionary example: it is ~280 lines and was flagged as too heavy. Do not reproduce that. The compact formats below are the target.

### Named parameters

Set in the request or proposed in the manifest:

- **slide count** — target number of slides (propose one; reduce/expand on request).
- **include-cover** — open with a cover slide (default: yes).
- **include-closing** — end with a closing recommendation/CTA slide (default: yes). Code3's closing is a CTA with concrete commitments, **never** a "thank you" slide.

---

## Generate mode

A new deck from a brief, notes, or a transcript.

### Workflow
1. Establish audience (external/internal), deck type, source content, slide count, and client/timeframe/logo (SKILL.md step 1).
2. **Find the throughline (story-first gate).** Analyze the data, propose one thesis + a 3–5 beat arc, and get sign-off on the **Narrative manifest** (below) before planning slides. Method in `references/narrative.md`. Scale the dialogue to the input — a handed-over thesis collapses to a one-line confirm; a data dump gets the full pass.
3. Plan the slide sequence against `assets/SLIDE_INDEX.md` and `references/slide_patterns.md`, mapping each approved beat to slides.
4. **Produce the generate manifest (below) in chat and get sign-off.**
5. Initialize the working deck, build the slide order, edit content, finalize, and run visual QA — per the SKILL.md workflow.

### Narrative manifest (in chat)
The story checkpoint that precedes the slide manifest. Lead with the thesis; keep it compact:

```
Thesis: <the one sentence the room should leave repeating>
Deck type: QBR · Audience: client (external) · Period: <period>

| Beat | Claim / so-what | Evidence (finding) |
|------|-----------------|--------------------|
| 1 | <claim> | <number + context> |
| 2 | … | … |
| 3 | … | … |

Open questions: <1–3 sharp pressure-tests>
POV / data gaps: <[CALLOUT: human POV] beats; data the file can't support>

Approve the thesis + arc, or push back, before I plan slides.
```

3–5 beats. If a clear thesis was handed over, this collapses to a one-line restatement + confirm — don't interrogate. Method in `references/narrative.md`.

### Generate manifest (in chat)
After the throughline is signed off — a short header block plus a per-slide table. The **Beat / message** column ties each slide to the arc beat it serves:

```
Mode: generate · Audience: client (external) · Deck type: QBR
Slide count: 14 (proposed) · Cover: yes · Closing: yes (CTA, not "thank you")
Client: <name> · Timeframe: <period> · Thesis: <one-liner>

| # | Layout (SLIDE_INDEX pos) | Working title | Beat / message | Content notes |
|---|--------------------------|---------------|----------------|---------------|
| 1 | Cover (1) | "<Client> <Period> QBR" | — | client logo, period |
| 2 | Agenda (5) | — | — | 5 items |
| 3 | Headline (21) | "<thesis line>" | Thesis | the deck's one-liner |
| … | … | … | … | … |
```

### Generate-mode rules
- **Run the story-first gate before slide planning.** Agree the thesis + arc (Narrative manifest) before picking slides — see `references/narrative.md`. Scale it to the input: a handed-over thesis collapses to a one-line confirm; a data dump gets the full analyze → propose → pressure-test pass. Don't interrogate.
- Use `[CALLOUT: human POV needed]` markers (see `brand.md`) on any slide whose punch line is a strategic hot take. The model proposes structure and data; a human supplies the opinion.
- Closing is a CTA with concrete commitments, never a "thank you" slide.
- **Real data charts go on a chart canvas (a slide with a raster image box), not the vector chart slides.** Template "chart" slides whose bars/donuts are native vector shapes are fixed decorations — proportions do NOT change with the numbers you type, so they can visually contradict real data (use them only for qualitative framing; `SLIDE_INDEX.md` flags them). When a beat needs a chart that matches real numbers: pick a chart-canvas slide from `SLIDE_INDEX.md` — Code3 core: **slide 15 (portrait, 4.8×5.6)** or the **landscape canvases 65 (8.74×2.34, full-width trend + takeaway cards), 69 (two stacked canvases), 70 (hero chart + stat pills)** — generate the PNG with `scripts/make_chart.py` aspect-matched to its image box (`inspect_images.py` for the EMUs), and swap it in by rId. **Strip any `<a:srcRect>` crop from the target `<p:pic>`'s blipFill** — `inspect_images.py` reports it; the Code3 slide-15 photo carries one (l≈41%) and it will clip a swapped-in chart (the landscape canvases 65/69/70 ship pre-stripped). Cite the source in the body/callout text. (The wide-landscape-canvas gap logged 2026-06-09 is resolved by slide 65.)
- **Dense layouts (slides 46–49, 64, 72, 76) are off by default.** Prefer simpler layouts. Reach for the high-density battlecard / matrix / data-table / case-study / audience-matrix / test-one-pager / creative-audit templates only on explicit request or under a hard constraint (e.g. a slide-count cap) — see the "Dense / high-density layouts" section of `SKILL.md`. They are still clone-and-fill template slides, not custom builds. (Re-skin mode: same rule — map to a dense template only when a source slide is genuinely that dense and the user wants it preserved.)
- All of SKILL.md's hard rules apply (clone template slides, never build from scratch, no leftover placeholder text, mandatory visual QA).

---

## Refresh mode

An existing Code3 deck + new data. Layout and structure are preserved; numbers, labels, periods, and charts are refreshed.

### Inputs to collect before starting
1. The existing deck (`.pptx`).
2. The new data (CSV, Sheets export, pasted prose, or a Markdown table — accept any).
3. Scope: new month? new quarter? — determines whether titles, eyebrows, source citations, and date ranges change alongside the numbers.
4. Surrounding-copy policy. **Default: preserve copy verbatim except where context shifted** (e.g. "Three things drove Q1" → "…Q2" when the period changed).

### Workflow
1. Unpack the deck. Inventory every slide's text slots, tables, charts, and images.
2. Build the refresh manifest (below); deliver in chat; get sign-off.
3. Apply text edits **position-aware** — see the two mechanical hazards below. **Do not hand-edit repeating-value tables with the `Edit` tool or `str.replace`.**
4. Regenerate chart images and swap placeholder images as needed (inspect image positions first — hazard 2).
5. Finalize, render, visual QA.

### Refresh manifest (in chat)
A compact three-part block:

```
Refresh — <Client> <Deck>, <old period> → <new period>, N slides

Will apply (mechanical):
- "<old period>" → "<new period>" labels throughout
- Tables repopulated per region/section from data
- Pie/bar charts regenerated as PNGs (flag historical gaps)
- Ad-creative screenshots → gray "Creative image — to be added" placeholders

Account team to fill before client delivery:
- All [DRAFT] prose blocks (takeaways, MoM, Test & Learn)
- Any label the skill guessed (top performers, etc.)
- Historical chart data the new data file can't supply

Scope confirmations: <list>
Open questions: <inline>

Approve, or flag anything before I commit.
```

### The two mechanical hazards (both learned the hard way on the CDC refresh)

**Hazard 1 — repeating cell values corrupt sequential replacement.** A table with several `$0K`, `0%`, or `—` cells will be silently mangled if you replace text first-match-at-a-time (`str.replace(find, repl, 1)` or a non-unique `Edit`): an early replacement creates a string that a later first-match then matches against, so the wrong cell changes. This is exactly what scrambled the CDC "Spend by Objective" tables.
- **Fix:** edit by *position*, not by first match. Use the helper:
  ```bash
  # 1. List every text run in document order with its index:
  python scripts/refresh_text.py path/to/slideN.xml --list
  # 2. Build an edits JSON keyed by absolute index or by (value, occurrence):
  #    [{"index": 47, "replace": "MENFALL26COLLECTION"},
  #     {"find": "$0K", "occurrence": 3, "replace": "$53.9K"}]
  # 3. Apply. --backup saves the pristine slide on the FIRST run and RESTORES
  #    from it on re-runs, so put ALL of a slide's edits in ONE JSON and re-run
  #    freely. Write the backup OUTSIDE the unpacked tree (a sibling _bak/) or it
  #    ships in the packed deck as junk:
  python scripts/refresh_text.py path/to/slideN.xml edits.json --backup _bak/slideN.xml.bak
  ```
  Occurrence is counted over ALL runs (the 3rd `$0K` is always the 3rd `$0K`), and a `find` must match the `--list` text exactly — including smart quotes (’ vs ') — so when unsure, use `index`. Any `Edit` that adds or removes an `<a:t>` shifts indices; re-run `--list` right before building an index-based JSON. Plain prose slots that appear once (titles, eyebrows) are fine with `Edit`; tables and stat grids go through `refresh_text.py`.

**Hazard 2 — image filenames do not tell you image positions.** `imageN.png` numbering varies slide to slide, so guessing which media file sits at which on-slide position swaps charts (on the CDC BR slide, the pie and the traffic card rendered transposed). Geometry is the source of truth.
- **Fix:** inspect EMU positions before mapping any regenerated PNG:
  ```bash
  python scripts/inspect_images.py path/to/slideN.xml
  # prints each <p:pic>: name, rId, media file, and x/y/w/h in EMU + inches
  ```
  Decide which media file to replace by its `<a:off>` coordinates, not its filename. The dense regional CDC slides follow a consistent layout — top-right pie, middle-right traffic/conversion cards, small flag bottom-right — but always confirm against the printed positions.
  Also check the `crop :` line in the output: if the target `<p:pic>` carries an `<a:srcRect>` (a crop meant for the original photo), **remove that element** when swapping in an aspect-matched chart PNG, or the chart renders clipped.

### Refresh-mode rules
- **Do not rewrite data-driven takeaway / commentary prose.** Voice and editorial judgment are human. Strip stale commentary and drop a `[DRAFT — account team to write]` placeholder. Only if the user explicitly asks, produce flat factual `[DRAFT]` observations from the data ("Instagram led platform mix at 33%"), clearly marked. Writing Code3-voice commentary is a deliberate scope expansion, not the default.
- **Preserve structure.** Do not reorder, add, or drop slides unless asked.
- **Charts are usually static PNGs**, not editable chart objects. Regenerate and swap by position: use `inspect_images.py` to read the chart box's `cx`×`cy`, then `scripts/make_chart.py <type> OUT.png … --width W --height H` with **W:H matching that box's aspect ratio** (e.g. box 2906700×1797297 → `--width 1067 --height 660`). `make_chart.py` covers **pie, donut, bar, hbar, grouped, stacked, line, funnel** — pick the type that matches the box you're replacing. Matching the aspect is mandatory — a square pie dropped into a wide box renders as a squashed ellipse; the engine emits the canvas at exactly W×H (pie/donut are centered so the circle stays round). **Line/bar history:** feed a per-deck rollup CSV — `--rollup <deck>_rollup.csv --metric <m> [--series <dim>] [--periods N]` — and append each cycle's numbers with `make_chart.py rollup-add <deck>_rollup.csv --period "<period>" --metric <m> --values "A:1,B:2"`, so the next refresh has the trend history (open decision 1, now resolved).
- **Unmapped rows** (a row in the template with no equivalent in the new data, e.g. the CDC "Catalog Sales" objective) must be surfaced in the manifest — never silently fill them with an unrelated value. Confirm: drop the row, keep it at `$0K / 0%`, or relabel. The same applies to any data-bound slot without a new value — stat cards, top-performer callouts, ROAS chips — not just table rows: surface it, mark `[DRAFT]`, never invent.
- Period framing (QTD vs MTD, year labels) follows the new data's cadence — confirm in the manifest.
- **Citations:** preserve the source deck's existing citation state. If the deck has none, don't add citation text boxes (that breaks the no-new-shapes rule) — flag the gap in the delivery note.

---

## Re-skin mode

A non-Code3 (off-brand) deck remapped onto Code3 template layouts. The most ambitious mode; intent inference is error-prone, so it leans hardest on the human-in-the-loop mapping sign-off.

### Workflow
1. Read the source deck. For a large source deck, don't full-unpack it (media extraction is slow and can exceed the shell timeout) — pull just the slide text: `unzip -o "source.pptx" 'ppt/slides/*.xml' -d src_slides`, then read those. For each source slide, classify its intent (cover, agenda, section divider, KPI grid, data table, narrative, roadmap, closing, appendix).
2. Propose a source-slide → Code3 template-slide mapping in the manifest.
3. **Get sign-off on the mapping before building** — this is where re-skin most needs a human.
4. For each approved mapping, clone the Code3 template slide and move the source content into its slots, reshaping/trimming to fit. Never overflow; never build a custom layout.
5. Finalize, render, visual QA.

### Re-skin manifest (in chat)
A mapping table:

```
Mode: re-skin · Source: <file> (N slides)

| Src # | Source intent | → Code3 layout (SLIDE_INDEX pos) | Notes |
|-------|---------------|----------------------------------|-------|
| 1 | Title | → Cover (1) | |
| 2 | Agenda | → Agenda (5) | 5 items |
| 3 | KPI dump (9 stats) | → Stat grid (31) or split | confirm |
| … | … | … | … |
```

### Re-skin-mode rules
- Confirm every non-obvious mapping before building. When a source slide has no clean Code3 home, propose the closest fit and flag it — don't force-fit into a grid.
- Content that doesn't fit gets reshaped or split across two slides — never crammed, never a custom layout.
- All generate-mode voice/brand rules apply to any copy you rewrite. Off-brand source copy frequently violates Code3 voice (passive, descriptive titles, AI-tells) — fix it to Code3 house style per `content_guidelines.md` as you move it.
- Source charts/images: keep the data, but rebuild the visual in the Code3 layout's slot. Don't paste a foreign-styled chart onto a Code3 slide.

---

## Single-slide builds (lightweight — no full-deck workflow)

For "make me one slide" or "add / replace a slide in this deck." A single slide isn't a 3–5 beat argument, so **single-slide builds bypass the story-first throughline gate** — go straight to picking the template slide and filling it. Every other hard rule still applies: clone a real template slide, leave no placeholder text, cite data, run visual QA on the slide. The manifest collapses to one line: *"Slide: battlecard (pos 46), filled with X — confirm?"*

Use `scripts/new_slide.py` (`--pos` is a SLIDE_INDEX presentation-order position, resolved against the core; or pass `--file slideN.xml`):

- **Standalone one-off slide** → a fresh 1-slide deck:
  ```bash
  python scripts/new_slide.py standalone /tmp/build/oneslide --pos 46
  # then edit ppt/slides/<file> (refresh_text.py --list to see slots), then:
  python scripts/finalize.py /tmp/build/oneslide
  ```
- **Insert into / replace a slide in an existing Code3 deck:**
  ```bash
  python scripts/new_slide.py insert /tmp/build/updated --into "QBR.pptx" --pos 7 --at 5
  python scripts/new_slide.py insert /tmp/build/updated --into "QBR.pptx" --pos 7 --at 5 --replace
  ```
  `--at` is the 1-based position in the target deck (default: append at end); `--replace` swaps out the slide currently there. **Insert requires a deck built from the current Code3 core** — it points the new slide at the same-named layout, which `clean.py` always keeps, so the layout is guaranteed present. If the target lacks that layout the script refuses (rebuild via generate/re-skin instead) rather than shipping a broken layout reference. The script copies the slide's media in with collision-safe names and registers it in `presentation.xml` / rels / content-types; then edit the new slide and `finalize.py`.

Deliver as usual (ship the `.pptx` + `.pdf`).

---

## Lint / brand audit (read-only)

"Is this deck client-ready / on-brand?" — a read-only pass over an existing `.pptx` that **reports, never edits**. Use it as the pre-delivery gate, or on a deck someone else built. It is the mechanical half of `references/quality_checks.md`; the eyes-only half still needs a render + subagent.

```bash
python scripts/lint_deck.py "DECK.pptx"                 # report to stdout
python scripts/lint_deck.py "DECK.pptx" --md report.md  # also write a markdown report
python scripts/lint_deck.py "DECK.pptx" --render        # also render JPGs for the visual pass
```

Mechanical checks: leftover scaffolding/placeholders (**CRITICAL** — Lorem, "Click to add", SECTION TITLE, "Month Year", `[CALLOUT`/`[DRAFT`, …); **off-brand fonts** (any font not in the bundled core's own font set — Office defaults like Calibri flagged hardest); **AI-tells** + heavy em dashes + descriptive titles + filler openers (STYLE, from `brand.md`); possible stat placeholders (`0%`, `$0K` — could be real, flagged to confirm); and data with no visible source (advisory — Code3 always cites). It does **not** change the deck — "fix it" is refresh / re-skin's job.

The allowed-font set is derived from the bundled core, so it is correct for a spawned variant too (the variant's own core defines on-brand). **Color/contrast and layout are deliberately left to the visual pass** (too noisy to flag mechanically): run `--render`, then hand `DECK_lint_qa/slide-*.jpg` to the visual-QA subagent prompt in SKILL.md step 8.

---

## Open decisions (carry these in the manifest until Code3 settles them)

These affect refresh mode and have not been decided. Surface them in the manifest; don't hard-code a silent default.

1. **Historical data for bar/line charts — RESOLVED (option a).** A single new month's data can't fill a 12-month trend chart, so the skill maintains a **per-deck rollup CSV** (`<deck>_rollup.csv`, long format `period,metric,dimension,value`) kept next to the deck in the workspace folder. `make_chart.py` reads it for line/bar history (`--rollup …`) and appends each cycle's numbers (`rollup-add`). When a data connector lands later it writes the same CSV — no rework. Until a given deck has a rollup, regenerate with the new point, leave history blank, and flag it in the delivery note.
2. **Unmapped objective rows** (e.g. CDC "Catalog Sales"): standardize on a static mapping table, or confirm row-by-row in the manifest each time. Until decided: confirm in the manifest.
