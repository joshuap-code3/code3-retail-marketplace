# Code3 Core Template — Slide Index

This index describes each of the 76 slides in code3_template_core.pptx. Use this to pick the right slide to clone when building a new deck.

> **Slides 46–49, 64, 72, and 76 are high-density layouts** (battlecard, search-intent matrix, two-section data table, case study, audience matrix, test one-pager, creative audit). They are **off by default** — the skill prefers simpler layouts. Use them only on explicit request or when a hard constraint (e.g. a slide-count cap) genuinely requires packing several slides' worth of content onto one. See the "Dense / high-density layouts" section of `SKILL.md` and `references/modes.md`.

> **Slides 64–76 were promoted 2026-06-11** from the approved "Great Slide Examples" deck (`examples_v2/2026-06-11_Great-Slide-Examples.pptx`) — real client-work layouts, blanked to placeholders. **Slides 65, 69, 70 carry landscape raster chart canvases** for `make_chart.py` output (srcRect crops already stripped).

## Quick Lookup

| Purpose | Slide | Purpose | Slide |
|---------|-------|---------|-------|
| **Title/Cover** | 1–4, 50–52 | **Data Charts** | 32–34 (decorative — real charts → 15 + make_chart) |
| **Agenda** | 5–6, 53–54 | **Timeline** | 35 |
| **Section Break** | 7–10, 55–56 | **Infographic** | 36–38 |
| **Key Takeaways** | 11–14 | **Company Story** | 39–43 |
| **Text + Image** | 15–20 | **Capabilities** | 44 |
| **2-Column** | 21 | **Mobile/App** | 45 |
| **3-Column** | 22–23 | | |
| **Process/Flow** | 24–26 | | |
| **Mobile Mockup** | 27–29 | | |
| **Stats Grid** | 30–31 | | |
| **Dense (battlecard/matrix/table/case)** | 46–49 | **Big statement** | 57 |
| **Multi-column (4 / 5)** | 58–59 | **5-step process** | 60 |
| **Client logo wall** | 61 | **Positioning / 2×2 map** | 62 |
| **Pricing / comparison table** | 63 | **Audience matrix (dense)** | 64 |
| **Chart canvas (landscape)** | 65, 69, 70 | **Before/after comparison** | 66 |
| **3-pillar color columns** | 67 | **Brand × metric stat matrix** | 68 |
| **Staircase / ascending path** | 71 | **Test/study one-pager (dense)** | 72 |
| **Annotated screenshots** | 73 | **Funnel** | 74 |
| **Split stat + chart panel** | 75 | **Creative audit (dense)** | 76 |

---

## Position → file map (READ THIS BEFORE EDITING SLIDES)

The position numbers in this index are **presentation order**. They are **NOT** the `slideN.xml` filenames — the unpacked files are non-contiguous and scrambled. To edit a slide's content, edit the **file** in this table. For the live, authoritative map (which stays correct even if the template changes), run `python scripts/map_slides.py <deck>_unpacked`.

| Pos | File | Pos | File | Pos | File |
|----:|------|----:|------|----:|------|
| 1 | slide5.xml | 16 | slide28.xml | 31 | slide56.xml |
| 2 | slide8.xml | 17 | slide33.xml | 32 | slide58.xml |
| 3 | slide9.xml | 18 | slide34.xml | 33 | slide60.xml |
| 4 | slide11.xml | 19 | slide36.xml | 34 | slide61.xml |
| 5 | slide12.xml | 20 | slide50.xml | 35 | slide57.xml |
| 6 | slide13.xml | 21 | slide39.xml | 36 | slide59.xml |
| 7 | slide16.xml | 22 | slide41.xml | 37 | slide62.xml |
| 8 | slide17.xml | 23 | slide43.xml | 38 | slide63.xml |
| 9 | slide19.xml | 24 | slide45.xml | 39 | slide72.xml |
| 10 | slide20.xml | 25 | slide47.xml | 40 | slide74.xml |
| 11 | slide22.xml | 26 | slide48.xml | 41 | slide77.xml |
| 12 | slide23.xml | 27 | slide49.xml | 42 | slide78.xml |
| 13 | slide24.xml | 28 | slide52.xml | 43 | slide83.xml |
| 14 | slide25.xml | 29 | slide53.xml | 44 | slide84.xml |
| 15 | slide26.xml | 30 | slide54.xml | 45 | slide125.xml |
| 46 | slide126.xml | 48 | slide128.xml | | |
| 47 | slide127.xml | 49 | slide129.xml | | |
| 50 | slide130.xml | 54 | slide134.xml | 58 | slide138.xml |
| 51 | slide131.xml | 55 | slide135.xml | 59 | slide139.xml |
| 52 | slide132.xml | 56 | slide136.xml | 60 | slide140.xml |
| 53 | slide133.xml | 57 | slide137.xml | 61 | slide141.xml |
| 62 | slide142.xml | 63 | slide143.xml | 64 | slide144.xml |
| 65 | slide145.xml | 66 | slide146.xml | 67 | slide147.xml |
| 68 | slide148.xml | 69 | slide149.xml | 70 | slide150.xml |
| 71 | slide151.xml | 72 | slide152.xml | 73 | slide153.xml |
| 74 | slide154.xml | 75 | slide155.xml | 76 | slide156.xml |

**Dense layouts (46–49)** were promoted from the full Code3 template (slides 99/95/96/116 there) and blanked to placeholders. They are real template slides — clone and fill like any other.

**Note on images:** the "Has image placeholder" / "Fixed graphics" lines below are approximate. Several slides carry decorative `<p:pic>` elements not noted here. For the real per-slide image inventory, run `python scripts/inspect_images.py <slide>.xml`.

---

## Detailed Slide Descriptions

### Slide 1 — title_cover
**Purpose:** Main title slide with lime-green geometric rope graphic.  
**Best for:** Opening a presentation with a modern, playful look.  
**Visual:** Lime-green background, 3D twisted rope illustration (black, yellow, green) on right side. "PRESENTATION TITLE" in bold sans-serif upper-left, "MONTH YEAR" subtitle below.  
**Placeholders to replace:** Title (2 lines max), month/year  
**Constraints:** Title ~45pt display font, 2–3 words per line recommended.  
**Has image placeholder:** No (graphic is fixed).

### Slide 2 — title_cover
**Purpose:** Alternate title slide with lime-green rounded shape graphic.  
**Best for:** When you want geometry over illustration.  
**Visual:** Light gray background, lime-green layered pill shapes (horizontal strokes) on right.  
**Placeholders to replace:** Title, month/year  
**Constraints:** Same as Slide 1.  
**Has image placeholder:** No.

### Slide 3 — title_cover
**Purpose:** Title slide with office photograph.  
**Best for:** Emphasizing people/team aspect or company culture.  
**Visual:** Light gray bg, rounded photograph (silhouettes in warm light) right side.  
**Placeholders to replace:** Title, month/year  
**Constraints:** Photo is fixed; title field adapts.  
**Has image placeholder:** Yes (photo is replaceable).

### Slide 4 — title_cover
**Purpose:** Dark tech title slide with digital grid/code background.  
**Best for:** Tech, digital transformation, or innovation-focused decks.  
**Visual:** Dark blue/black background with grid lines and binary-like patterns. White rounded pill in center holds title. "PRESENTATION TITLE" centered in pill.  
**Placeholders to replace:** Title  
**Constraints:** Title text is centered, max 2–3 words.  
**Has image placeholder:** No.

### Slide 5 — agenda
**Purpose:** Main agenda/contents slide (dark background).  
**Best for:** Outlining topics in 5 sections.  
**Visual:** Dark charcoal background. White rounded shape right side. Left: "WHAT'S COVERED HERE" in white, with lime-green star accent. Right: 5 numbered items (01–05) "Click to add agenda item."  
**Placeholders to replace:** 5 agenda items (one per line, 4–10 words each)  
**Constraints:** Numbered format is fixed; items are short phrases.  
**Has image placeholder:** No.

### Slide 6 — agenda
**Purpose:** Alternate agenda slide (light background).  
**Best for:** Softer, accessible alternative to Slide 5.  
**Visual:** Light gray background, lime-green rounded shape right, "WHAT'S COVERED HERE" left in dark text.  
**Placeholders to replace:** 5 agenda items  
**Constraints:** Same structure as Slide 5.  
**Has image placeholder:** No.

### Slide 7 — section_divider
**Purpose:** Section break with warm-toned photograph and title.  
**Best for:** Transitioning between major sections.  
**Visual:** Left side: rounded office photo (people silhouettes, warm backlit). Right: "SECTION TITLE" in large serif italic font, dark text on light background.  
**Placeholders to replace:** Section title  
**Constraints:** Title is italic, ~60pt, 2–4 words.  
**Has image placeholder:** Yes (photo is replaceable).

### Slide 8 — section_divider
**Purpose:** Abstract section divider with directional arrows.  
**Best for:** Modern, impactful section breaks.  
**Visual:** Light blue background, dense radial arrow pattern pointing inward. Blue pill-shaped callout in center: "SECTION TITLE" black text.  
**Placeholders to replace:** Section title  
**Constraints:** Title is centered, 1–3 words.  
**Has image placeholder:** No.

### Slide 9 — section_divider
**Purpose:** Blue pill section header with stacked text layers.  
**Best for:** Minimal, clear section transitions.  
**Visual:** Light blue background, overlapping pill shapes. Two text layers: "Section Break" and "Where we go for answers" in blue and white.  
**Placeholders to replace:** Both text lines  
**Constraints:** Each line ~20–30 chars.  
**Has image placeholder:** No.

### Slide 10 — section_divider
**Purpose:** Coral/salmon section divider with pill pattern.  
**Best for:** Thematic section break (varies color from blue/green).  
**Visual:** Coral/salmon background, overlapping pill outlines, red pill with white text: "So... what now?"  
**Placeholders to replace:** Main section text  
**Constraints:** Centered, 1–2 phrases.  
**Has image placeholder:** No.

### Slide 11 — key_takeaways
**Purpose:** Text-heavy recap slide.  
**Best for:** Summarizing brief details or recap paragraphs.  
**Visual:** White/light bg. Title: "Brief recap of the brief." (italic). Body: Lorem ipsum paragraph, left-aligned.  
**Placeholders to replace:** Title, full paragraph of body text  
**Constraints:** Body can be multi-line; use 10–15pt body font.  
**Has image placeholder:** No.

### Slide 12 — executive_summary
**Purpose:** Executive summary with three rounded callouts.  
**Best for:** Summarizing business impact in 3 statements.  
**Visual:** Lime-green background, section label "SECTION TITLE" top-left, title "Use Me for an Executive Summary" italic. Three lime-green pills with italic text: "We did really great things", "Here's how it impacted your business", "Here's what we have lined up next!"  
**Placeholders to replace:** 3 summary statements  
**Constraints:** Each 5–10 words max, fits in pill.  
**Has image placeholder:** No.

### Slide 13 — key_takeaways
**Purpose:** Key learnings slide with blue callout boxes.  
**Best for:** Presenting 4 major insights or lessons.  
**Visual:** Light blue background, title "We've learned a lot over the past quarter..." Blue rounded pills below: "Big sentence 1–4" (italic, white text).  
**Placeholders to replace:** 4 key learning statements  
**Constraints:** 8–15 words each, bold impact language.  
**Has image placeholder:** No.

### Slide 14 — key_takeaways
**Purpose:** Alternate learnings slide (coral/salmon variant).  
**Best for:** Same purpose, different color theme.  
**Visual:** Coral/salmon background, 5 red/orange pills with white text: "Big sentence 1–5".  
**Placeholders to replace:** 5 learning statements  
**Constraints:** 8–15 words each.  
**Has image placeholder:** No.

### Slide 15 — content_text_image
**Purpose:** Content slide with left image, right text + callout. **Also the standard CHART CANVAS.**  
**Best for:** Showcasing a visual concept with supporting text — or presenting a real data chart (chart left, commentary right).  
**Visual:** Left: full-height dark urban photo (nighttime cityscape). Right: "Slide Title" (section label), body text (~60 words), lime-green callout box with arrow pointing to bullet points (2 items).  
**Placeholders to replace:** Title, body text, 2 bullet points in callout  
**Constraints:** Body is 3–4 sentences; bullets are 1–2 lines each.  
**Has image placeholder:** Yes (left photo — a raster `<p:pic>`, ~4.8×5.6 in, portrait).  
**Chart canvas:** this is the only core content slide with a real raster image box, so it is the home for `make_chart.py` PNGs in generate mode. Donut/pie, hbar, funnel, and grouped bars suit the portrait box well. Confirm the exact box EMUs with `inspect_images.py` and aspect-match the PNG (`--width`/`--height`). **The photo's `<p:pic>` carries an `<a:srcRect>` crop (l≈41%) — remove that element when swapping in a chart or it renders clipped** (`inspect_images.py` flags it). Put the source citation in the body or callout text. A wide landscape trend line is a known gap — see slides 32–33 warning and `references/extending_library.md`.

### Slide 16 — content_text
**Purpose:** Dark background content slide with floating callouts.  
**Best for:** Presenting insights with visual hierarchy.  
**Visual:** Dark charcoal bg. "Slide Title" (italic, white). White and lime-green floating boxes with lorem ipsum, 2 callouts with arrows.  
**Placeholders to replace:** Title, 2 text boxes  
**Constraints:** Text boxes ~50 words each.  
**Has image placeholder:** No.

### Slide 17 — content_text
**Purpose:** Clean text slide with section label and bullets.  
**Best for:** Straightforward content delivery.  
**Visual:** Light gray bg, "SECTION TITLE" label top-left. "Slide Title" (italic). "Header" (lime-green) + multi-level bullet list (3 levels: filled, hollow, solid squares).  
**Placeholders to replace:** Title, header, bullet list (nested up to 3 levels)  
**Constraints:** Bullets are 2–3 lines max per item.  
**Has image placeholder:** No.

### Slide 18 — content_text_image
**Purpose:** Content with large lime-green rounded shape right.  
**Best for:** Text-driven slide with visual breathing room.  
**Visual:** Light bg. "Slide Title" left, body text + bullets left. Large lime-green pill shape right (no graphic inside).  
**Placeholders to replace:** Title, body text, 2–3 bullet points  
**Constraints:** Shape is fixed background; text wraps left.  
**Has image placeholder:** No.

### Slide 19 — content_text_image
**Purpose:** Content with large blue rounded shape + callout label.  
**Best for:** Variant of Slide 18 with blue theme.  
**Visual:** Light bg. "Slide Title" left, body + bullets, large blue rounded shape right with "Callout" label.  
**Placeholders to replace:** Title, body text, bullets  
**Constraints:** Same as Slide 18.  
**Has image placeholder:** No.

### Slide 20 — content_text_image
**Purpose:** Content slide with phone mockup (fixed).  
**Best for:** Mobile/app-specific content when phone visual is relevant.  
**Visual:** Light bg. "Slide Title" left, body text + bullets. Right: phone mockup (black frame, blue callout inside).  
**Placeholders to replace:** Title, body text, callout text on phone  
**Constraints:** Phone mockup is fixed; text placeholder is inside blue area.  
**Has image placeholder:** No (phone is fixed graphic).

### Slide 21 — content_twocol
**Purpose:** Process flow with 5 numbered callouts and curved connector.  
**Best for:** Showing a sequence or workflow.  
**Visual:** Light bg. "Slide Title" top-left. Red curved line (top) connecting 5 items. Items labeled with red compass-star icons, body text (40–60 words each). Flow is left to right.  
**Placeholders to replace:** Title, 5 text blocks (one per item)  
**Constraints:** Each block ~30 words; items must fit in flow.  
**Has image placeholder:** No.

### Slide 22 — content_threecol
**Purpose:** Three-column layout with header pills and bordered boxes.  
**Best for:** Comparing 3 concepts, features, or sections.  
**Visual:** Light bg. "Slide Title" top-left. 3 columns: lime-green pill header ("Subtitle"), bordered box below with body text (40–60 words each). Callout label at bottom.  
**Placeholders to replace:** Title, 3 subtitles, 3 body text blocks  
**Constraints:** Pills are 1–2 words; boxes hold ~60 words each.  
**Has image placeholder:** No.

### Slide 23 — content_threecol
**Purpose:** Alternate 3-column with blue borders and subtitle text.  
**Best for:** Similar to Slide 22, different visual style.  
**Visual:** Light bg. 3 columns with blue borders, "Subtitle" + "SUBTEXT" header, body text, "Callout" label bottom.  
**Placeholders to replace:** Title, 3 subtitles, 3 subtext, 3 body blocks  
**Constraints:** Similar constraints as Slide 22.  
**Has image placeholder:** No.

### Slide 24 — timeline_process
**Purpose:** Vertical flow with numbered steps (1–3) and descriptions.  
**Best for:** Step-by-step processes or workflows.  
**Visual:** Light bg. "Slide Title" top-left. 3 rows: lime-green header pill ("Subtitle"), numbered circle (1, 2, 3), white bordered box with body text, down arrows between rows.  
**Placeholders to replace:** Title, 3 subtitles, 3 body text blocks  
**Constraints:** Numbers and arrows are fixed; text boxes hold ~50 words.  
**Has image placeholder:** No.

### Slide 25 — timeline_process
**Purpose:** Left-aligned numbered list (1–3) with right-aligned text descriptions.  
**Best for:** Simple process or feature list with flow.  
**Visual:** Light bg. "Slide Title". Blue blocks (numbered 1–3, "Subtitle"), right-aligned bordered boxes with body text, right-pointing arrows between.  
**Placeholders to replace:** Title, 3 subtitles, 3 body text descriptions  
**Constraints:** Numbered items are compact; descriptions ~40 words each.  
**Has image placeholder:** No.

### Slide 26 — timeline_process
**Purpose:** Left panel list (1–4 items) with right panel descriptions.  
**Best for:** Extended list with corresponding details.  
**Visual:** Light bg. "Slide Title". Left: 4 blue numbered items ("Subtitle"). Right: 4 bordered boxes with body text, arrows linking each.  
**Placeholders to replace:** Title, 4 subtitles, 4 body descriptions  
**Constraints:** Left items are compact; right boxes hold ~50 words each.  
**Has image placeholder:** No.

### Slide 27 — content_grid
**Purpose:** Three mobile phone mockups with text labels and top connector.  
**Best for:** Showing mobile user flows or app progression.  
**Visual:** Light yellow-green left panel. "Slide Title" left. Right: 3 phone mockups (black frames, labeled "TEXT" at top) with body text below each ("Lorem ipsum...").  
**Placeholders to replace:** Title, 3 phone labels, 3 description texts  
**Constraints:** Phone mockups are fixed; text placeholders below each.  
**Has image placeholder:** No (phones are fixed graphics).

### Slide 28 — content_grid
**Purpose:** Grid of 6 mobile mockups (2×3) with TikTok and other app logos.  
**Best for:** Showcasing multiple app screens or social media platforms.  
**Visual:** Light yellow-green left panel. Right: 6 phone mockups arranged in 2 rows, with app logos (TikTok, Instagram) labeled on curves.  
**Placeholders to replace:** App/platform labels  
**Constraints:** Phone mockups are fixed; labels are minimal.  
**Has image placeholder:** No.

### Slide 29 — big_stat
**Purpose:** Four large circular stat display (percentage + text).  
**Best for:** Highlighting 4 key metrics or percentages.  
**Visual:** Dark charcoal bg. "Slide Title" (white, italic) left. Right: 4 white circles, each with "0%" (large) and "TEXT" label below.  
**Placeholders to replace:** 4 percentages/stats, 4 labels  
**Constraints:** Numbers are ~100pt; labels are 1–2 words.  
**Has image placeholder:** No.

### Slide 30 — data_chart
**Purpose:** Six small circular progress charts with descriptions.  
**Best for:** Showing 6 related metrics or progress points.  
**Visual:** Light bg. "Slide Title" top-left. 6 columns: blue/yellow progress circle ("0%", "SUBTEXT"), gray box with body text, "Subtext" label below. Callout label at bottom.  
**Placeholders to replace:** Title, 6 percentages, 6 subtext labels, 6 descriptions, callout label  
**Constraints:** Percentages are large; descriptions are 40–50 words each.  
**Has image placeholder:** No.

### Slide 31 — data_grid
**Purpose:** Six-cell stat grid (2×3) with percentages and labels.  
**Best for:** Comparing 6 metrics in a compact grid.  
**Visual:** Light bg. "Slide Title". 6 cells in 2×3 grid: lime-green (odd) or white bordered (even), "Subtitle" pill header, large "0%", "Subtext" label. "Callout Here As Necessary" italic callout above.  
**Placeholders to replace:** Title, 6 subtitles, 6 percentages, 6 subtext labels, callout  
**Constraints:** Grid layout is fixed; cells are compact.  
**Has image placeholder:** No.

### Slide 32 — data_chart
**Purpose:** Pie chart + legend with multi-level callout branching.  
**Best for:** Showing breakdown with platform or category details.  
**Visual:** Light bg. Left: blue/yellow donut chart ("0%", "SUBTEXT") with "Callout" label. Right: branching callouts for "SUBJECT" and "SUBSET" items with social platform icons (Instagram, TikTok, Reddit, Twitter, Facebook).  
**Placeholders to replace:** Percentage, subtext, title, 5 platform/item descriptions  
**Constraints:** Chart is mostly fixed; callout text ~30 words.  
**⚠ Accuracy warning:** the donut is a **fixed vector decoration** — its visual split does NOT change when you edit the "0%" label. A real percentage on this slide can visually contradict itself. Use it only when the chart is illustrative (the callouts carry the content). For a chart that must match real numbers, use slide 15 + `make_chart.py`.  
**Has image placeholder:** No.

### Slide 33 — data_chart
**Purpose:** Before/after bar chart comparison.  
**Best for:** Showing data transformation or improvement.  
**Visual:** Light bg. "Slide Title" top-left. Left: 3 black bars ("###" placeholder) with "Graph Title" and labels. Arrow to right side. Right: 6 colored bars (blue/lime-green, "###") with "Graph Title" and labels. "Subtitle" text under each bar section.  
**Placeholders to replace:** Title, 2 graph titles, bar labels, values (## placeholders)  
**Constraints:** Bar charts are template-based; values are simplified.  
**⚠ Accuracy warning:** bar heights are **fixed vector shapes** — they do NOT scale to the values you type into the "###" labels. Use only for qualitative before/after framing; if the bars must reflect real magnitudes, use slide 15 + `make_chart.py` instead.  
**Has image placeholder:** No.

### Slide 34 — timeline_process
**Purpose:** Gantt chart / project timeline with months.  
**Best for:** Roadmap, project schedule, or timeline visualization.  
**Visual:** Light bg. "Slide Title" top-left. Timeline header: months (NOV–DEC), colored pills for phases. Below: 6 rows of stacked phase bars, overlapping groups, yellow "PRIME DAY" and "REMI" labels.  
**Placeholders to replace:** Phase names, milestone labels  
**Constraints:** Month row is fixed; phase bars are editable.  
**Has image placeholder:** No.

### Slide 35 — timeline_process
**Purpose:** Horizontal timeline with multiple layers and milestones.  
**Best for:** Showing project phases, product lifecycle, or multi-track initiatives.  
**Visual:** Light bg. "Slide Title" top-left. Timeline: dots/periods on horizontal line, 3 parallel timeline bars (color-coded: lime, blue, orange) with "Time Period" labels, "Callout" notes and branching callouts with bullet text.  
**Placeholders to replace:** Title, timeline phase names, 2 sets of bullet descriptions  
**Constraints:** Timeline is complex; text callouts are ~50 words each.  
**Has image placeholder:** No.

### Slide 36 — data_table
**Purpose:** Numbered list with icon/stat grid on right.  
**Best for:** Correlating text insights with visual metrics.  
**Visual:** Light bg. Left: 4 numbered items ("Lorem ipsum..."), circles (1, 2, 3, 4). Right: table (light yellow bg) with "TITLE" header, 5 columns (icon + percentage pairs): different app icons, "0%" each.  
**Placeholders to replace:** Title, 4 left items, 5 platform labels, 5 percentages  
**Constraints:** Left items are ~30 words each; right grid is compact.  
**Has image placeholder:** No.

### Slide 37 — quote_or_callout
**Purpose:** Funnel/pyramid infographic with stage labels.  
**Best for:** Illustrating customer journey, sales funnel, or process stages.  
**Visual:** Light bg. "Slide Title" (italic). Stacked trapezoid/funnel shapes (lime-green), 4 stages labeled: "Awareness", "Consideration", "Purchase", "Loyalty". Horizontal lines on sides.  
**Placeholders to replace:** Title, 4 stage names (fixed in image)  
**Constraints:** Funnel shape is fixed; stage labels are editable.  
**Has image placeholder:** No.

### Slide 38 — data_table
**Purpose:** Diverging bar chart (red/green, left/right).  
**Best for:** Showing sentiment, performance ranges, or bipolar metrics.  
**Visual:** Light bg. "Slide Title" top-left. Chart: 5 rows of labels, centered circles, left bars (red–orange gradient, "Needs Help" to "Below Average"), right bars (yellow-green gradient, "Above Average" to "Doing Great").  
**Placeholders to replace:** Title, 5 row labels, bar data  
**Constraints:** Chart layout is fixed; labels are ~20 chars each.  
**Has image placeholder:** No.

### Slide 39 — company_intro
**Purpose:** Code3 company values/mission slide.  
**Best for:** Introducing Code3 or company values in presentation.  
**Visual:** Dark charcoal bg. "Hey. We're Code3." (white, large italic). Multi-paragraph body text (white, 8–10pt). Greenish-yellow left border accent.  
**Placeholders to replace:** Entire body paragraph (full mission/values text)  
**Constraints:** Body is ~250–300 words; all text is white on dark; left border is fixed.  
**Has image placeholder:** No.

### Slide 40 — company_intro
**Purpose:** Code3 values breakdown with DNA spiral graphic.  
**Best for:** Detailing company pillars or differentiators.  
**Visual:** Light gray bg. Title: "It's in our DNA" (italic, with underline). Left: 4 bullet sections (bold headers + descriptions). Right: black/white DNA spiral helix graphic (fixed).  
**Placeholders to replace:** Title (optional), 4 section headers, 4 section descriptions  
**Constraints:** Headers are 2–3 words; descriptions are ~50 words each.  
**Has image placeholder:** No (DNA is fixed).

### Slide 41 — capabilities
**Purpose:** Integrated approach diagram with circular center and 3 quadrants.  
**Best for:** Showing how 3 capabilities connect around a core (data, business model).  
**Visual:** Light gray bg. Left: "OUR INTEGRATED APPROACH" (large italic). Center: blue circle "YOUR DATA". Around it: 3 quadrants with section titles (CONNECTIONS, CREATIVE, COMMERCE), body text (40–60 words each), callout bubble (green, ~20 words).  
**Placeholders to replace:** Center label, 3 section titles, 3 section descriptions, callout text  
**Constraints:** Center label is 1–2 words; sections are 40–60 words each.  
**Has image placeholder:** No.

### Slide 42 — company_intro
**Purpose:** Business value statement with supporting details.  
**Best for:** Explaining company approach to data and value creation.  
**Visual:** Light gray bg. Top: "Data Matters." (italic, lime-green underline). Left: "We drive business value with a seat at the table:" (large italic heading). Right: 3 sections (bold headers + body): "Analysis", "Planning", "Perspective", each ~60 words.  
**Placeholders to replace:** Opening phrase, main heading, 3 section headers, 3 section descriptions  
**Constraints:** Headings are 2–4 words; descriptions are ~60 words each.  
**Has image placeholder:** No.

### Slide 43 — company_timeline
**Purpose:** Company history timeline with key milestones and stats.  
**Best for:** Showcasing company growth, founding, and major events.  
**Visual:** Light gray bg. Large italic title: "An industry leader since there's been an industry." Left: body text (80–100 words). Right: vertical timeline (2009–2023) with milestones (small stats in circles: "80+", "100B", "$5B"), logo evolution (Facebook, Twitter/Instagram/TikTok, Amazon logo icons), product screenshots (mobile app mockups bottom right).  
**Placeholders to replace:** Title, left body text, timeline stat labels  
**Constraints:** Body is ~100 words; timeline is mostly fixed; stats are editable.  
**Has image placeholder:** Yes (app screenshots on right).

### Slide 44 — capabilities
**Purpose:** End-to-end capabilities showcase (two category columns).  
**Best for:** Listing all services or platform offerings.  
**Visual:** Light gray bg. "Our End-to-End Capabilities" (large). Left column (blue pills): "CONNECTIONS & COMMERCE" label + 5 category pills (E-Retail, Programmatic & Direct Partnerships, Paid Social, Paid Search, Influencer & Affiliates), each with icon row below. Right column (orange pills): "CREATIVE" label + 5 services (Branding, Production, Transcription, Content, Technology).  
**Placeholders to replace:** Category/service names (mostly fixed)  
**Constraints:** Names fit in pills; icons are fixed graphics.  
**Has image placeholder:** No.

### Slide 45 — closing
**Purpose:** Campaign/product case study slide with phone mockups.  
**Best for:** Presenting a project outcome or upcoming initiative.  
**Visual:** Light gray bg. Top: lime-green banner "LOOKING FORWARD". Title: "New Restaurant Openings" (italic). Left: body text in 2 sections ("A New Opening Look" + Overview/Recommendation). Right: 2 phone mockups side-by-side, labeled "Customized per location" and "Newly Refresh Canada NFOs...". Blue pill callout "What We Recommend" above right phones.  
**Placeholders to replace:** Title, 2 body sections (Overview/Recommendation), callout label, phone labels  
**Constraints:** Body sections are ~80 words each; phone mockups are fixed.  
**Has image placeholder:** No (phones are fixed).

---

## Dense / high-density layouts (46–49)

These pack several slides' worth of content onto one canvas. **Off by default** — use only on explicit request or under a hard constraint (e.g. a slide-count cap). They are real template slides promoted from the full Code3 library and blanked; clone and fill like any other.

**Citing on dense layouts (no source slot on 46/47/49).** Only **slide 48** has a built-in source-citation line. Slides **46, 47, and 49 have no citation slot** — so when you put data or stats on them, carry the source in the **`SECTION TITLE` eyebrow** run (e.g. `SEARCH STRATEGY · SOURCE: IPSOS; SEMRush, Mar–May 2026`). Do **not** add a new text box for it (no-new-shapes rule). If the eyebrow can't hold it, flag the citation gap in the delivery note. This keeps Code3's "always cite" rule satisfied without breaking the no-new-shapes rule.

### Slide 46 — dense_battlecard
**Purpose:** Two-column "battlecard" comparing two parallel groups of items side by side. The highest-utility dense layout — the closest fit for a "strategy on a page."  
**Best for:** Quick Wins vs. Long-Term, Us vs. Them, Channel A vs. Channel B — any two sets of three items with a what/why structure, under a slide-count cap.  
**Visual:** Light bg. Italic "Slide Title" + "SECTION TITLE" eyebrow. Two lime-green header pills ("Group One/Two"). Under each: "What?"/"Why?" sub-labels, 3 numbered charcoal cards (1–3 left, 4–6 right), each with an item title, a 1–2 line description, an arrow, and an italic so-what line.  
**Placeholders to replace:** 2 group headers, 6 item titles, 6 descriptions, 6 so-what lines.  
**Constraints:** Exactly 3 items per column (6 total). Item titles 1–3 words; descriptions ≤2 lines; so-what ≤1 line. The dark cards are **title cards, not image slots.** Don't add a 4th row — the column won't hold it. No source-citation slot — carry any source in the eyebrow (see "Citing on dense layouts" above); a clean way to keep stats here is to fold the proof number into the italic so-what line.  
**Has image placeholder:** No (arrows are fixed graphics).

### Slide 47 — dense_intent_matrix
**Purpose:** Search-intent / category matrix mapping an audience to clusters across demand tiers.  
**Best for:** Search / SEM / SEO strategy — how a **single** segment's keyword or category clusters map across funnel tiers and search-volume bands. Fits a one-audience intent-cluster view (e.g. the "intent clusters we own" column of the OUAI search slide) — **not** a two-channel battlecard; for a Google-vs-Social / Channel-A-vs-B comparison use slide 46.  
**Visual:** Light bg. Italic title + script subhead + magnifier icon. Left: a triangle framework ("CORE CONCEPT" center, three rotated edge labels "Input One/Two/Three") + a short supporting note. Right: a top "Audience / Segment" bar feeding a grid of colored cells ("Cluster 1–14") by row tier (Higher/Lower Search Volume, Demand) with right-hand tier labels (Awareness/Consideration/Purchase). Three gray image placeholders sit above the grid for product/category thumbnails.  
**Placeholders to replace:** title, subhead, 3 triangle inputs + center label, supporting note, segment bar, up to 14 cluster cells, 3 thumbnail images.  
**Constraints:** Cluster cells hold 1–4 words — keep them short. Tier labels (Awareness/Consideration/Purchase, etc.) are reusable scaffolding. Replace or leave the 3 gray image slots.  
**Has image placeholder:** Yes (3 small thumbnail slots above the grid).

### Slide 48 — dense_data_table
**Purpose:** Two-section comparison data table with a supporting narrative.  
**Best for:** Side-by-side ranked data (two keyword groups, two segments) with 2–3 metric columns each, plus a left framing note and a product visual.  
**Visual:** Light bg. Italic title + script subhead + target icon. Left: a "Section heading", body copy with a highlighted term, two blue pills ("Pill One/Two") with a small arrow, and a gray image placeholder with an "Image caption". Right: a two-section table ("SECTION ONE/TWO"), each with KEYWORD PHRASE / ORGANIC POSITION / SEARCH VOLUME columns and rows; a source-citation line beneath.  
**Placeholders to replace:** title, subhead, section heading + body, 2 pills, image + caption, 2 section headers, column headers, row triples, source citation.  
**Constraints:** **Edit the table with `scripts/refresh_text.py` (position-aware), NOT the `Edit` tool** — repeating "0"/"000"/"Keyword phrase" cells corrupt under first-match replacement. The table comfortably holds **~6 rows**; a 7th sits tight against the source-citation line (inherited from the source design) — prefer ≤6 rows. Always fill the citation (Code3 cites).  
**Has image placeholder:** Yes (gray product/visual slot, left-center).

### Slide 49 — dense_case_study
**Purpose:** Case-study / results slide — full-height image, a two-column insight/strategy narrative, and a stat row.  
**Best for:** A single case study or campaign recap on one slide: what we saw, what we did, the numbers.  
**Visual:** Left: full-height image placeholder (gray) under a lime-green corner swoosh. Right: "SECTION TITLE" eyebrow + italic title; two columns ("The Insight" / "The Strategy") of body copy; "By the Numbers" with four blue stat circles — three numeric ("00"/"0x" + label) and one text-only ("Short stat phrase").  
**Placeholders to replace:** title, eyebrow, 2 body columns, 4 stat circles (3 numeric + label, 1 text), left image.  
**Constraints:** Body columns 2–4 lines each. Stat numerals are large; labels 1–2 short words. The 4th circle is a **text statement by design** (no numeral). Left image is a replaceable full-bleed photo. No source-citation slot — carry any source in the eyebrow (see "Citing on dense layouts" above).  
**Has image placeholder:** Yes (full-height left photo).

---

## Variety & extra layouts (50–63)

Same-shape alternates for the high-recurrence slides (covers, agendas, dividers) so a deck that leans on them doesn't go stale, plus a few layout gaps. All blank, clone-and-fill.

### Slide 50 — title_cover (blue)
**Purpose / best for:** Alternate cover, solid-blue background. A clean blue-themed opener.
**Placeholders:** title (2 lines), month/year. **Image:** No.

### Slide 51 — title_cover (blue swirl)
**Purpose / best for:** Cover with a dynamic 3D blue-swirl graphic at right. A bold, energetic opener.
**Placeholders:** title, month/year. **Image:** No (graphic is fixed).

### Slide 52 — title_cover (photo)
**Purpose / best for:** Cover with a lifestyle/people photo at right. A warmer, human opener.
**Placeholders:** title, month/year, photo. **Image:** Yes (replaceable photo).

### Slide 53 — agenda (dark)
**Purpose / best for:** "What you'll see today" agenda, dark background. Alternate to slides 5–6.
**Placeholders:** 5 agenda items (4–10 words each). **Image:** No.

### Slide 54 — agenda (light)
**Purpose / best for:** Same agenda, light background. Rotate with 5, 6, 53 across decks.
**Placeholders:** 5 agenda items. **Image:** No.

### Slide 55 — section_divider (dark pill)
**Purpose / best for:** Section break — "SECTION TITLE" in a dark rounded pill on light. Adds a dark divider option.
**Placeholders:** section title (1–3 words). **Image:** No.

### Slide 56 — section_divider (orange)
**Purpose / best for:** Section break — orange pills on dark. A warm divider variant; rotate with 7–10, 55.
**Placeholders:** section title. **Image:** No.

### Slide 57 — big_statement
**Purpose / best for:** Full-bleed oversized italic statement with a two-tone highlight + arrow. The thesis / manifesto / punchy transition line (the story-first beat).
**Placeholders:** the statement, split into a dark lead and a highlighted closing phrase.
**Constraints:** keep it to one punchy line, ~6–12 words. **Image:** No.

### Slide 58 — content_fourcol
**Purpose / best for:** Four parallel items (the core otherwise caps at three columns).
**Placeholders:** title, 4 subtitles, 4 body blocks. **Constraints:** ~40–50 words/column. **Image:** No.

### Slide 59 — content_fivecol
**Purpose / best for:** Five parallel items.
**Placeholders:** title, 5 subtitles, 5 body blocks. **Constraints:** five columns are tight — keep body ~35–45 words. **Image:** No.

### Slide 60 — timeline_process (5-step)
**Purpose / best for:** A 5-step sequence (longer than slides 24–26 hold).
**Placeholders:** title, 5 step labels + descriptions. **Constraints:** ~30–40 words/step. **Image:** No.

### Slide 61 — logo_wall ("The Company We Keep")
**Purpose / best for:** Client / brand proof — a wall of logos. Standard in pitches and capabilities decks.
**Placeholders:** title, subhead, ~12 logo image slots (gray `#C9C9C9` placeholders — drop brand logos in).
**Constraints:** logos vary in size by design. **Image:** Yes (12 logo slots).

### Slide 62 — positioning_map (2×2)
**Purpose / best for:** A two-axis positioning / perceptual map or 2×2 matrix — competitive positioning, prioritization, "where we play." The core has no other matrix layout.
**Visual:** Two crossed axes with high/low labels on each end and a soft lime plot area; drop dots, logos, or labels to plot.
**Placeholders:** title, 4 axis labels (AXIS X/Y high & low). **Constraints:** add your own plotted markers (text boxes / shapes are fine *as overlays on the existing plot* — do not rebuild the axes). **Image:** No.

### Slide 63 — pricing_table
**Purpose / best for:** A pricing / scope / feature-comparison table — line items down the left, 2 options across the top, checkmarks and prices in the cells. For proposals, SOWs, plan tiers.
**Visual:** Two blue option pills as column headers; 8 line-item rows with ✓ marks and price cells.
**Placeholders:** title, 2 option headers + descriptions, 8 line-item labels, cell marks/prices.
**Constraints:** **edit cells with `scripts/refresh_text.py` (position-aware)** — the repeating ✓ and price cells corrupt under first-match replacement. Keep ✓ for "included," clear a cell for "not included." **Image:** No.

### Slide 64 — audience_matrix (DENSE — off by default)
**Purpose / best for:** A 3-persona × 3-category research matrix — e.g. how three audiences differ on discovery channels, shopping preferences, and brand sets. Survey/GWI-style ranked lists with index scores.
**Visual:** Three horizontal persona bands, each with a dark/gray persona tab (left edge), a circular photo slot, and three pill-headed columns (blue / light blue / lime) of ranked `item (XXX)` lists.
**Placeholders:** 1-line title (~45 chars max — longer wraps into the source line), source eyebrow, 3 persona names, 3×3 category pills + survey-question subheads, 4–6 ranked items + index scores per cell, 3 circular photo slots (gray placeholders).
**Constraints:** DENSE — explicit request / hard cap only. Title must stay on one line. Keep items to ≤6 per cell. **Image:** Yes (3 persona photos).

### Slide 65 — chart_canvas_landscape ⭐ (THE landscape chart canvas)
**Purpose / best for:** A full-width trend/line chart with takeaway cards — the canonical home for 12-month rollup trends in generate mode. Resolves the logged "wide landscape chart canvas" gap (miss log 2026-06-09).
**Visual:** Light-blue background, white rounded panel holding a **landscape raster image box ~8.74×2.34 in at (0.62, 1.24)** (srcRect already stripped — swap `make_chart.py` PNGs straight in by rId), 4 blue takeaway cards below.
**Placeholders:** title, eyebrow, chart PNG (aspect-match ~8.74:2.34 → e.g. `--width 1311 --height 351`), 4 takeaway card headers + one-liners, source line.
**Constraints:** takeaway cards hold ~1 header + 1–2 lines each. **Image:** Yes (1 chart canvas).

### Slide 66 — before_after_comparison
**Purpose / best for:** A then-vs-now comparison — budget/strategy changes, period-over-period shifts — with proof cards below.
**Visual:** Split background (white top / gray bottom). Light card (before) → green arrow → blue card (after) + lime circle badge for the delta. Below: 3 dotted-outline cards (header + one-liner + 3 bullets each).
**Placeholders:** title, eyebrow, before/after period labels + 2 metric lines each + captions, delta badge (+XX + label), 3 card headers + summaries + 3 bullets each, source.
**Constraints:** metric lines are short (`Metric: value`); badge holds ~6 chars + 2-word label. **Image:** No.

### Slide 67 — three_pillar_columns
**Purpose / best for:** Three named strategies/workstreams with proof under each — a richer alternative to plain 3-column (22–23): color-coded pill headers (lime / blue / orange), dotted body cards, optional big-stat callouts.
**Placeholders:** title, subtitle, eyebrow, 3 pillar pill labels, per-pillar: bold lead-in + context line + 3 arrow bullets (middle pillar instead carries two big `~XX%` stats + labels above its bullets).
**Constraints:** pillar labels 2–4 words; bullets ~8 words. **Image:** No.

### Slide 68 — brand_metric_stat_matrix
**Purpose / best for:** One metric story across 3 brands/products × 3 metric rows — "we made the bet, every brand paid off."
**Visual:** Narrative text block left (bold blue claim lead-in + interpretation paragraph); right: 3×3 grid of rounded stat tiles (cream → lime by row) under 3 brand-logo slots (gray placeholders), rotated metric-row labels on the left edge, footnote bottom.
**Placeholders:** title, eyebrow, claim + context paragraph ×2, 3 logo slots, 9 stat tiles (big `XX%` + sub-lines), 3 row labels, footnote.
**Constraints:** tile sub-lines ~3 short lines max. **Image:** Yes (3 brand logo chips).

### Slide 69 — sidebar_dual_chart_canvas (2 landscape canvases)
**Purpose / best for:** Attribution stories needing two stacked trend charts — drivers on the left, evidence right.
**Visual:** Cream sidebar (~3.5 in) with multi-line title (blue italic accent runs) + source; right: **two raster chart canvases — ~6.04×2.84 in at (3.60, 0.15) and ~5.47×2.37 in at (3.69, 2.99)** (srcRect stripped), with Kalam-style highlight annotation + period/annotation labels overlaid.
**Placeholders:** title (2 runs: plain + blue italic), eyebrow, source, 2 chart PNGs, highlight annotation (`XXX% YoY in headline metric`), 2 period + annotation label pairs.
**Constraints:** sidebar title ~10–14 words across ~7 lines. Aspect-match each canvas separately. **Image:** Yes (2 chart canvases).

### Slide 70 — chart_stat_pills_canvas (landscape canvas)
**Purpose / best for:** One hero trend chart + a row of 4 corroborating stat pills with platform icons — "every data source agrees."
**Visual:** White panel with lime outline holding a **raster chart canvas ~6.75×2.63 in at (0.90, 1.14)** (srcRect stripped) with left/right axis labels; lime circle callout top-right; 4 lime stat pill cards below, each over a platform icon chip (Amazon/Walmart/TikTok/Meta icons kept); sources footer.
**Placeholders:** title, eyebrow, chart PNG, 2 axis labels, circle callout (context + `XX% faster` + benchmark), 4 pills (label + big stat + context + period), sources.
**Constraints:** pill stats ~6 chars; callout ~12 words. **Image:** Yes (1 chart canvas + 4 icon chips).

### Slide 71 — staircase_path
**Purpose / best for:** A compounding 4-step strategy ramp toward a goal — sequence + momentum in one visual.
**Visual:** Four ascending blocks (blush → deep orange) with a blue curve arrow sweeping over them; black goal label chip on the left ("Path to $XXM…").
**Placeholders:** title, eyebrow, goal label, 4 step titles + 1–3 line descriptions (later steps hold more text).
**Constraints:** step titles ~3–6 words; descriptions grow left→right (1–2 lines steps 1–2, 2–3 lines steps 3–4). **Image:** No.

### Slide 72 — test_one_pager (DENSE — off by default)
**Purpose / best for:** A complete test/study design + readout on one slide: hypothesis, questions, KPIs, milestone timeline, performance screenshots.
**Visual:** Left column: lime "Overview" band + gray sub-bands (Hypothesis/Objective, Questions, Prioritization-KPIs-Duration). Right: lime "Timeline & Design" band with a 6-milestone dot tracker (status/owner under each), "Performance" band + 2 screenshot slots (gray placeholders).
**Placeholders:** test name + subtitle, objective/hypothesis text, 3 questions, KPI lines, duration/feasibility, 6 milestone labels + `MM/DD` + owner per dot, 2 screenshot images.
**Constraints:** DENSE — explicit request / hard cap only. Milestone owner cells fit ~6 chars (use "Owner", "Code3" — "Partner" overflows). **Image:** Yes (2 screenshot slots).

### Slide 73 — annotated_screenshots
**Purpose / best for:** Two stacked exhibits (platform screenshots, competitor charts) interpreted by a big left headline and on-image annotations. This is a text+image layout, **not** a chart canvas — use it when the exhibits are captured, not generated.
**Visual:** Big multi-line headline left; right: 2 landscape image boxes (~5.1×2.3 and ~5.1×2.6 in) each with a red rotated pill label on its left edge and a bold annotation + hand-drawn arrow on the image.
**Placeholders:** headline, 2 rotated pill labels, 2 annotations, 2 images, source.
**Constraints:** annotations ~8 words. **Image:** Yes (2 exhibit slots + 2 small legend chips).

### Slide 74 — funnel_stages
**Purpose / best for:** Funnel-shaped allocation/spend story across 3 stages with platform icons — "we're over/under-invested at the wrong stage."
**Visual:** Big stat circle left (XX% + persona behavior) with dotted arrow to a second stat; right: 3 tapering funnel bands (light → vivid blue), each with stage name, `XX% → XX%` transition, platform icon chips (Reddit/TikTok/Pinterest/Meta icons kept) on the edges.
**Placeholders:** title, eyebrow, setup line, circle stat + description, secondary stat, 3 stage names + transitions.
**Constraints:** stage names 1–2 words; icons are decorative chips — keep or remove per story. **Image:** Yes (icon chips only).

### Slide 75 — split_stat_chart_panel
**Purpose / best for:** A half-white / half-blue split: hero donut-gauge stat on the left, supporting segment bar chart in a white panel on the right. **Both charts are native vector shapes** — fill text/number slots; the donut arc and bar heights are fixed decorations (qualitative only; for data-true charts use a canvas slide).
**Visual:** Left: title, social icon chips, lime/blue donut with `X.X%` center + prior/YTD lines, Kalam annotation with arrow. Right blue panel: lime-highlighted supporting headline, white chart card (title, 3 vector bars with `XX%` chips, legend), client logo chip placeholder bottom-right.
**Placeholders:** title, eyebrow, donut center stat + 2 context lines + metric label, annotation (lead-in + KEY FACT + rest), panel headline, chart title, 3 segment labels + `XX%` chips, 2 legend labels, source.
**Constraints:** donut/bars don't scale with data. **Image:** Yes (2 social icon chips + 1 logo chip).

### Slide 76 — creative_audit (DENSE — off by default)
**Purpose / best for:** A 4-column creative/content audit — numbered findings over evidence screenshots with handwritten-style callouts.
**Visual:** 4 columns split by thin rules, each headed by a lime-highlighted numbered finding (bold + italic emphasis runs) over 1–5 ad screenshot slots (gray placeholders); Kalam handwritten annotations under columns 3–4. Contains a **table** (column scaffold) — `tableStyles.xml` carries its style; edit cells with `refresh_text.py` if values repeat.
**Placeholders:** title (2 runs: plain + italic persona), eyebrow, 4 numbered finding headers, ~10 screenshot slots, 2 handwritten annotations.
**Constraints:** DENSE — explicit request / hard cap only. Finding headers ~6–8 words or they clip at column edges. **Image:** Yes (~10 screenshot slots).

---

## Category Summary

**title_cover (7 slides):** 1–4, 50–52  
**agenda (4 slides):** 5–6, 53–54  
**section_divider (6 slides):** 7–10, 55–56  
**key_takeaways / executive_summary (4 slides):** 11–14  
**content_text / content_text_image (6 slides):** 15–20  
**content_twocol (1 slide):** 21  
**content_threecol (2 slides):** 22–23  
**timeline_process (6 slides):** 24–26, 34–35, 60  
**content_grid (2 slides):** 27–28  
**big_stat / data_chart (6 slides):** 29–33  
**data_table (2 slides):** 36, 38  
**quote_or_callout (1 slide):** 37  
**company_intro (4 slides):** 39–40, 42–43  
**capabilities (2 slides):** 41, 44  
**closing (1 slide):** 45  
**dense / high-density (4 slides):** 46–49 *(off by default — explicit request / constraint only)*  
**big statement (1 slide):** 57  
**multi-column (2 slides):** 58–59  
**logo wall (1 slide):** 61  
**positioning / 2×2 map (1 slide):** 62  
**pricing / comparison table (1 slide):** 63  
**audience matrix (1 slide, dense):** 64 *(off by default)*  
**chart canvas — landscape (3 slides):** 65, 69, 70 ⭐ *(real-data charts via make_chart.py; srcRect pre-stripped)*  
**before/after comparison (1 slide):** 66  
**3-pillar color columns (1 slide):** 67  
**brand × metric stat matrix (1 slide):** 68  
**staircase / ascending path (1 slide):** 71  
**test/study one-pager (1 slide, dense):** 72 *(off by default)*  
**annotated screenshots (1 slide):** 73  
**funnel (1 slide):** 74  
**split stat + chart panel (1 slide):** 75  
**creative audit (1 slide, dense):** 76 *(off by default)*

---

## Design Notes

- **Color scheme:** Lime-green (#C3D600 range), dark charcoal, light gray, blue, coral/salmon, white. Lime-green is the primary brand accent.
- **Typography:** **Barlow** throughout — Light (display / ALL-CAPS eyebrows), ExtraBold (titles, key ideas), Regular/Medium (body); plus **Kalam** for small hand-script accents only. These are the **only two brand fonts**; the core was cleaned to enforce it (no Arial/Montserrat/Lato/Rubik/etc.), and `lint_deck.py` flags any other font. The template handles weights automatically — don't restyle.
- **Shapes:** Rounded pills, circles, trapezoids, curved connectors, arrows, geometric patterns.
- **Fixed graphics:** Slides 1–4, 7–8, 20, 27–28, 37, 39–40, 43, 45 have non-replaceable images/illustrations.
- **Image placeholders:** Slides 3, 7, 15, 43, 45, 52 accept custom photos (office, lifestyle, product). Dense slides 47, 48, 49 and the logo wall (61) carry gray `#C9C9C9` image placeholders (thumbnails / product / full-bleed photo / brand logos) — replace or leave as neutral boxes.
- **Chart slides 32–34 are vector, not image boxes.** The data-chart layouts (positions 32–34), stat grids, and the slide-75 donut/bars are built from native shapes/icons, **not** a swappable chart picture — fixed decorations whose proportions don't change with your numbers. Regenerated chart PNGs from `make_chart.py` go on the **chart canvases**: slide 15 (portrait, 4.8×5.6) and slides **65, 69, 70 (landscape — see their entries for box geometry)**. The landscape canvases ship with srcRect crops already stripped, so PNG swaps are drift-proof; always aspect-match `--width/--height` to the box.
- **Table styles:** slide 76 contains a real `<a:tbl>`; its `tableStyleId` is defined in the core's `ppt/tableStyles.xml`. If you ever transplant another slide that carries a table, **copy its `<a:tblStyle>` definition into `tableStyles.xml` too** — a dangling tableStyleId crashes LibreOffice rendering outright.
- **Variety for high-recurrence slides:** covers (1–4, 50–52), agendas (5–6, 53–54), and section dividers (7–10, 55–56) each have several interchangeable styles. Rotate them within a deck so repeated dividers/covers don't look monotonous (and to satisfy the "don't repeat a layout 3× in a row" rule).
- **Constraint:** Layouts are tight; adding excessive text will overflow. Stick to 1–2 lines per callout, ~40–60 words per text block.
- **Dense layouts (46–49, 64, 72, 76):** Off by default. The skill should still prefer simpler layouts and only reach for these on explicit request or when a hard constraint (e.g. a 20-slide cap) requires packing several slides' worth of content onto one. Even then, they are clone-and-fill template slides — never built from scratch.
- **Image placeholders on slides 64–76:** all client imagery was neutralized to gray `#C9C9C9` boxes (persona photos on 64, brand logos on 68, screenshots on 72/73/76, chart canvases on 65/69/70). Platform icon chips (Amazon/Walmart/TikTok/Meta/Reddit/Pinterest/FB/IG) were **kept** — they're generic and part of the layouts' value.
