# Client Goals — Source of Truth

Goals live in the **Client AI Goal Intake Form** (Google Sheet). Always fetch the
current values at run time via the connected Google Sheets connector — do not rely
on the snapshot below for live benchmarking. The snapshot exists only to document
structure and known sensitivities.

**Sheet:** `https://docs.google.com/spreadsheets/d/1nn3BMCJpY2LGSJoA8J6Z9SdlbyLJqapVmCE6SEgCeBU/edit`

## How to read it
- One tab per client. Some clients have multiple goal blocks (one per retailer or
  business unit) stacked on a single tab — match BOTH the client and the retailer
  found in the data dump.
- Fields to extract per block: Client Name, Brand / Business Unit, Retailer(s),
  Primary KPI Goal(s), Secondary Goals, North Star Metric + Target Value,
  Monthly Budget Cap, Budget Pacing, Restricted Categories, Known Sensitivities,
  Competitors, Notes, Last Updated.
- If "Last Updated" is stale relative to the data period, flag it.

## Tab map & hard constraints (verify live; structure as of 2026-06)
- **Zevia** — blocks for Amazon, Walmart, Instacart. Primary: ROAS, Units, NTB
  (NTB is the stand-in for Household Penetration / HHP). Hard rule: **≤25% branded
  spend** (Walmart especially). Watch the **7/1/26 shelf reset** removing
  distribution for Orange Creamsicle, Peaches & Cream, Cream Soda — shift spend to
  other flavors and 1P. Competitors: Olipop, Poppi, Coca-Cola, Pepsi, Dr. Pepper.
- **Advantice Health** — three brands: Kerasal, Dermoplast, New Skin. Primary:
  Balanced; North star Portfolio ROAS ≥ 3.5; ACOS ≤ 22%. Hard rule: **never blend
  the three brands** — report each separately. Seasonality: Kerasal peaks Q4,
  Dermoplast steady, New Skin spikes summer. No unapproved OTC/medical claims.
- **Canon USA — Printer** — Efficiency; North star ACOS ≤ 15%; SOV ≥ 30%; ROAS ≥ 5.0.
  Hard rule: **never blend Printer and Camera BUs**; do not bid on camera terms.
- **Canon USA — Camera** — Efficiency; North star ACOS ≤ 12%; SOV ≥ 25%; ROAS ≥ 6.0.
  Hard rule: **never blend Camera and Printer BUs**; do not bid on printer terms.
  Back-loaded pacing around holiday/gifting.

## When a goal metric is missing from the dump
NTB, SOV, and HHP are frequently NOT in a standard campaign/keyword/item export.
If a client's primary goal references one and it's absent, state that and name the
report needed (e.g., Amazon "New-to-Brand" report, a share-of-voice/category report)
rather than estimating it.
