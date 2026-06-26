# QA Checklist

Run through this before delivering any deck. Failures in this list are what separate "looks like Code3 built it" from "an LLM built it." The v1 skill shipped decks with most of these issues — don't repeat them.

## Critical — will embarrass if missed

- [ ] No Lorem ipsum anywhere. Search every slide XML for `Lorem`.
- [ ] No "Click to add" placeholder text. Search for `Click to`.
- [ ] No `[CALLOUT: …]` or `[DRAFT …]` human-fill markers remain if the deck is going to a **client**. They're expected in an account-team handoff draft, but must be cleared before client delivery — `finalize.py` lists any that are still in the deck.
- [ ] No "SECTION TITLE" eyebrow left unchanged. Every eyebrow names the actual section.
- [ ] No "Slide Title" or "Subtitle" placeholder text.
- [ ] No "Subtext" or "0%" or "xx" left in stat placeholders.
- [ ] Default "Month Year" on cover is replaced with actual month + year.
- [ ] Client name is spelled consistently and correctly throughout.
- [ ] Deck title on the cover is the actual title, not a stub.
- [ ] No blank columns, grid cells, or bullet slots. Either filled or layout swapped.

## Layout integrity

- [ ] No overlapping text or shapes.
- [ ] No text clipped or overflowing its box.
- [ ] No text so long it wraps into or through a decorative element.
- [ ] Consistent margins — no slide is noticeably crammed when the rest have breathing room.
- [ ] Title lines don't wrap awkwardly (a 3-word line followed by a 1-word line looks bad).

## Code3 house style

- [ ] Every chart, table, or stat has a source citation and a date range. *(Exceptions: pill/divider/takeaway layouts with no caption slot inherit the source from their section's data slide; in refresh mode, preserve the source deck's existing citation state and flag missing ones in the delivery note rather than adding citation shapes. See content_guidelines.md.)*
- [ ] Eyebrow labels (ALL CAPS above titles) name the current section, not "SECTION TITLE".
- [ ] Slide titles are assertions, not descriptions ("X drove Y" not "X Overview").
- [ ] Body copy is in sentence case, not Title Case.
- [ ] Bullets have parallel structure and similar length.
- [ ] Numbers show direction/comparison: "+27% YoY", not "27%".
- [ ] Acronyms are used naturally where appropriate (ROAS, CTR, NTB%) but not spelled out pedantically.
- [ ] No em-dash-heavy writing. (A few are fine, many is an AI-tell.)
- [ ] No "AI-tell" words: delve, navigate the landscape, leverage, unlock potential, journey, embark, at the end of the day.

## Narrative integrity

- [ ] Each section opens with a divider slide (for decks > 8 slides).
- [ ] Each section has a clear beginning, middle, and end — doesn't just trail off.
- [ ] The Problem → Response → Results pattern shows up where applicable (findings sections).
- [ ] Multi-brand content uses the same brand order consistently (e.g. Amlactin | Kerasal | Triple Paste).
- [ ] The closing slide states what's next or invites action — doesn't just say "Thank you" or "Questions?"
- [ ] The opening title slide conveys the point of the deck, not just its category.

## Layout variety

- [ ] Same layout isn't used 4+ times in a row.
- [ ] Deck mixes text-forward slides, data/stat slides, and image slides.
- [ ] Section dividers visually break up dense runs of content slides.

## Visual / render

- [ ] Render the deck to JPGs (via `finalize.py`) and view every slide.
- [ ] Use a subagent with fresh eyes to do a critical pass — ask it to find problems.
- [ ] Nothing low-contrast (light text on light background, dark text on dark background).
- [ ] Pie/donut charts are perfectly circular, not stretched into ellipses. (A regenerated chart PNG must match its image box's aspect ratio — see the chart rule in `modes.md`.)
- [ ] All photo/image placeholders either replaced intentionally or left with template's default (not half-broken).

## Final sanity

- [ ] Total slide count matches the plan you agreed with the user (or within a close delta).
- [ ] Client logo on the cover is either the correct client logo, a clean placeholder, or omitted if not available.
- [ ] Speaker notes, if present in original template, don't contain internal instructions that shouldn't ship to the client.
- [ ] Saved to the user's workspace folder (not the scratch dir) and `computer://` link works.

---

## How to run the check

```bash
# Text search for leftover scaffolding — fastest way to catch misses.
python -m markitdown path/to/deck.pptx | grep -iE "\blorem\b|\bipsum\b|click to|SECTION TITLE|Slide Title|\bSubtitle\b|\bSubtext\b|\bxx\b|\[insert|\[CALLOUT|\[DRAFT|lorem ipsum"

# If that returns any results, fix them before proceeding.

# Then render for visual inspection:
python /path/to/pptx/scripts/office/soffice.py --headless --convert-to pdf path/to/deck.pptx
pdftoppm -jpeg -r 150 path/to/deck.pdf qa-slide

# View each qa-slide-*.jpg critically — or hand them to a subagent with the
# prompt in SKILL.md's step 7.
```
