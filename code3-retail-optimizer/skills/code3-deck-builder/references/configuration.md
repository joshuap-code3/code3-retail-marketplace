# Configure mode — spawn a branded `<name>-deck-builder` variant

Configure mode is **not a deck-building mode.** It provisions a new, self-contained
skill that builds decks from *another brand's* template core. The output is an
installable `<name>-deck-builder.skill`, not a deck.

Two paths:

| Path | When | Voice | Visual template | `--voice` |
|------|------|-------|-----------------|-----------|
| **Graham Holdings org** | Another GHC company (Kaplan, Society6) with its own full brand | The org's own | The org's own | `custom` |
| **Client account** | An external account (e.g. LVMH) whose deck template you must match | **Code3 house style** | The client's | `code3` (default) |

For a client account you write in Code3's voice but fill the *client's* slides;
`brand.md` carries the client's visual identity (fonts, colors, logo rules) while
`content_guidelines.md` keeps Code3's writing conventions.

## The one hard prerequisite: an EDITABLE `.pptx` core

The engine works by **cloning slide XML and swapping text.** It therefore needs an
**editable PowerPoint** template — a `.pptx` whose slides contain real text runs and
placeholders.

- A **PDF is not a usable core.** Converting PDF→PPTX only embeds each page as a flat
  image, producing uneditable "picture" slides. If all you have is a PDF, get the
  source Google Slides / `.pptx` it was exported from.
- Only if **no editable core can be obtained** do you fall back to building template
  slides from scratch — and then the **design-review loop** below is mandatory.

## Workflow

### 1. Gather inputs
- The brand's editable template core (`.pptx`).
- Brand guidelines (fonts, color palettes, logo/co-branding rules) — often embedded
  in a brand-book PDF.
- Decide the path/voice (table above) and a slug (`lvmh` → `lvmh-deck-builder`).

### 2. Prepare the core — slim it under 30 MB
Skills must be **< 30 MB**. Template cores are media-heavy (hero photography,
animated GIFs). On `/tmp` (the mount blocks deletes):
- Flatten animated GIFs to their first frame (a static export looks identical).
- Downsample oversized images (cap longest edge ~1600px) and re-encode JPEG ~80%.
- Re-pack and confirm it still opens. Keep the full-fidelity original archived.
Save the result as `assets/<slug>_template_core.pptx`.

### 3. Build the slide index
```bash
python scripts/build_slide_index.py assets/<slug>_template_core.pptx OUT_DIR
```
This renders `OUT_DIR/thumbs/slide-<pos>.jpg` (presentation order), unpacks the
core, and writes `SLIDE_INDEX_SCAFFOLD.md` with the position→file map plus every
slide's text runs and image boxes. **View each thumbnail**, complete the `_TODO_`
fields (Purpose / Best for / Visual / Placeholders / Constraints), curate out pure
spec/guideline pages and near-duplicate variants if they don't earn a slot, and save
as `SLIDE_INDEX.md`. Curation is a brand decision — propose the keep/cut list to the
account owner before finalizing (the configure-mode manifest gate).

### 4. Build the brand + reference layer
- `assets/brand_palette.json` — `{"name","black","palette":[...]}`; `make_chart.py`
  reads it so charts are on-brand (without it, charts fall back to the core's own
  theme colors, which is usually right anyway).
- `references/brand.md` — the brand's fonts, color palettes, logo/co-branding,
  and (client path) a note that copy stays Code3 voice.
- Adapt `slide_patterns.md` to the new index's slide numbers; `content_guidelines.md`
  stays Code3 for a client account. `modes.md` / `quality_checks.md` carry over.

### 5. Spawn the package
```bash
python scripts/spawn_variant.py \
  --name <slug> --display "<Brand>" --voice code3 \
  --core assets/<slug>_template_core.pptx \
  --index path/to/SLIDE_INDEX.md \
  --palette path/to/brand_palette.json \
  --refs path/to/<slug>_refs_dir \
  --out  BUILD_DIR
```
Produces `BUILD_DIR/<slug>-deck-builder/` and `BUILD_DIR/<slug>-deck-builder.skill`
(SKILL.md at archive root; configurator scripts excluded — a variant doesn't
re-spawn). The script warns if the package exceeds 30 MB.

The variant's `SKILL.md` is generated from `scripts/variant_skill_template.md`
(NOT from the parent `SKILL.md`). When a feature lands in the parent, add it to
that template too — `scripts/package_skill.py` runs a marker-based drift check
between the two at packaging time and warns on mismatches.

### 6. Validate end-to-end
Before shipping, build a short real deck with the spawned variant
(`new_deck.py` → edit → `finalize.py`) and run visual QA on the JPGs. Confirm the
cloned slides render on-brand and editable. Fix the core/index, re-spawn, repeat.

## Design-review loop (only when building slides from scratch)
If no editable core exists and you must generate template slides:
critique the render → refine the XML → re-render, and repeat until a full visual
pass is clean, **before** the slide enters the core. Never ship a from-scratch slide
that hasn't survived this loop. This is the failure mode the whole skill exists to
avoid, so prefer obtaining the real editable core every time.
