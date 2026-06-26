# Throughline — find the story before you pick slides

**Generate mode.** A deck is an argument, not a slide container. Before any slide is chosen, agree on the single thing the deck proves and the beats that build it.

This step exists because the failure mode is the model inferring a message from the brief, baking it into slide titles, and shipping slides that look right but say nothing the room will remember. **Slide selection is downstream of an agreed story — never the reverse.** Refresh and re-skin don't run this step (refresh preserves an existing deck's story; re-skin maps existing slides onto Code3 layouts).

## The gate in one line

Analyze the data → propose one thesis + a 3–5 beat arc → pressure-test it with the account lead → get sign-off → *then* map beats to slides.

## Scale the conversation to the input — don't interrogate

The depth of this step tracks how much story the user already handed you. Read the room:

- **Thesis given.** The brief already states the point ("this QBR is about how we cut CPA 30% while scaling spend"). Restate it in one line, name the arc you'll use, confirm, move on. One exchange — running a full analysis dialogue here is friction the user will resent.
- **Data + direction.** Some steer, no spine ("here are the quarter's numbers, it's a performance QBR"). Analyze, propose a thesis + arc, ask 1–2 sharp questions, get sign-off.
- **Data dump.** A pile of numbers and "make me a QBR." Full pass: analyze, bring 2–3 candidate stories, recommend one, pressure-test hard.

The gate is always a real sign-off. Its *weight* is not always the same.

## Step 1 — Analyze the data (don't parrot it)

You want the handful of numbers that carry a story, not a full audit. Load the data in the sandbox (pandas; the `data` skills if available) and compute, as the data supports:

- **Movement** — period-over-period: MoM, QoQ, YoY. Direction and magnitude. The delta is the story; the absolute is the context.
- **Pacing** — actual vs. goal / budget / forecast. Ahead, behind, on track.
- **Efficiency** — ROAS, CPA, CPM, CTR, NTB%, etc. moving up or down, and vs. benchmark.
- **Mix shifts** — where spend and results concentrate, and how that changed: by platform, objective, audience, creative type. A shift in mix is often the real story.
- **Outliers** — top and bottom performers, anomalies, what broke or popped.
- **What changed** — tie movement to actions: launches, new tactics, budget moves, creative tests.

Output a compact **findings list**. Each finding = a number + its context + a candidate so-what:

- ✅ "CPA fell 31% (Q4 $42 → Q1 $29) while spend rose 18% — efficiency held as we scaled. *So-what:* the Q4 creative overhaul is paying off and is safe to scale."
- ❌ "CPA was $29." (a number with no movement and no so-what)

**Only compute what the data supports.** No prior-period column → no YoY; say so. Never infer a number to complete a story (a standing skill rule). Flag every gap.

## Step 2 — Find the thesis (the throughline)

The **thesis** is the one sentence the room should leave repeating. It's the deck-level so-what. Everything in the deck either sets it up or proves it.

A thesis earns the slot only if it is:

- **An assertion, not a topic.** "Q1 proved efficiency scales" — not "Q1 performance review." (Same rule as slide titles in `content_guidelines.md`.)
- **Backed by the data** you just analyzed — name the findings under it.
- **Consequential** — it implies a next action or decision.
- **Something the audience cares about** — tied to *their* goal, not our activity.

When the data supports more than one honest framing, that's not a problem to hide — it's the thing to pressure-test. Name the candidates:

> "Two true stories here: (a) an *efficiency* win — we cut CPA while scaling; (b) a *growth* story — new-to-brand customers up 40%. Same quarter, different headline. Which one does the client care about right now?"

## Step 3 — Build the arc (3–5 beats)

The arc is the ordered set of claims that build the thesis. Keep it to 3–5 beats; more and the room loses the thread. Pick the structure that fits the deck type:

- **QBR / performance:** Where we were (goal/context) → What happened (results) → Why (drivers) → What we learned → What's next (recommendation). Compressible to **Situation → Complication/Insight → Resolution**.
- **New-business / pitch:** Problem → Stakes → Our approach → Proof → The ask.
- **Capabilities / strategy:** Status quo → Gap or opportunity → Our POV → How it works → Proof → Next step.

Each beat carries a **claim** (the assertion it makes), its **evidence** (which finding backs it), and its **so-what**. A beat with evidence but no so-what is a context slide — Code3 doesn't ship those (`brand.md`: always answer "so what?").

## Step 4 — Separate fact from POV

You assert what the data says. You do **not** invent Code3's strategic opinion. When a beat's punch line is a judgment call — the recommended bet, the hot take, the "here's what we'd do" — mark it `[CALLOUT: human POV needed]` and leave the structure plus supporting facts around it for the strategy lead (the convention in `brand.md`). An arc can lay out three data-backed options; *which* to recommend is human.

Likewise flag **data gaps**: a beat the provided data can't support yet. Ask for the data, or mark it an assumption to confirm — never paper over it.

## Step 5 — The Narrative manifest + pressure-test (the gate)

Present the story compactly, **in chat** (exact format in `modes.md` → generate). Lead with the thesis, show the arc as a short table (Beat · claim/so-what · evidence), then the open questions and any POV / data gaps. Keep it tight — this is the cheap checkpoint, not a document (the anti-friction rule in `modes.md`).

Then actively pressure-test. You are bringing a POV to react to, not asking "what do you want?":

- "Is X the headline, or does the client care more about Y?"
- "This arc leads with efficiency; if the real story is scale, I'd reorder to open on Z and move CPA to support."
- "What will the client push back on? What's the uncomfortable number we should get ahead of?"
- "Beat 4 is a strategic call — I've marked it for your POV rather than guess it."

Get explicit sign-off on the thesis and arc before planning slides.

## Step 6 — Hand off to slide planning

Only after the story is signed off, map beats to slides against `slide_patterns.md` and `assets/SLIDE_INDEX.md`. One beat is usually 1–3 slides (a claim slide + its evidence). The generate manifest carries a **message / so-what** per slide naming the beat it serves — so every slide has a job in the argument. A slide that doesn't advance a beat shouldn't be in the deck.

## Guardrails

- **Don't interrogate when the thesis is given.** Collapse to a one-line confirm.
- **Don't pick slides before sign-off.** (Hard rule in `SKILL.md`.)
- **Don't propose a thesis the data can't back**, and don't invent the strategic opinion — that's `[CALLOUT: human POV needed]`.
- **Don't exceed ~5 beats.** If you need more, the thesis is too broad — split the deck or sharpen the point.
- **Keep the manifest compact.** A 200-line story doc is the friction that kills adoption.
