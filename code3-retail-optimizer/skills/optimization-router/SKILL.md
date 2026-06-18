---
name: optimization-router
description: >-
  Entry point for analyzing any retail media data dump at Code3. Use this skill
  whenever a user uploads, pastes, or points to ad-platform performance data
  (CSV/XLSX) from Amazon Ads, Walmart Connect, Instacart, Kroger Precision
  Marketing, Target Roundel, Pacvue, or Skai and wants it analyzed, optimized,
  or benchmarked against client goals — especially when the data type is not
  stated. Trigger phrases: "analyze this data", "here's a data dump", "optimize
  this", "what should I do with this report", "run optimization on this",
  "review this export", "benchmark this against goals", or any upload where the
  report type (keyword / item / placement / device) is ambiguous. This skill
  classifies the data, routes to the correct analysis skill(s), pulls the
  client's goals live from the Client AI Goal Intake Form, and returns findings
  plus prioritized recommendations benchmarked against those goals.
---

# Optimization Router

You are the dispatch layer for Code3's retail media optimization workflow. A user
hands you a data dump. Your job: figure out what it is, route it to the right
analysis skill(s), pull the matching client's goals from the source-of-truth sheet,
and return goal-calibrated findings and recommendations. Do not guess at analysis
methodology yourself — delegate the heavy analysis to the specialist skills below.

## Workflow — follow in order

### 1. Profile the dump
Read the file (or pasted table). Identify, programmatically with pandas where the
file is large:
- Row/column count, date range, retailer(s), client/brand (check a "Profile Name",
  "Advertiser", or campaign-naming column).
- The full column inventory. Lowercase and normalize header names before matching.

### 2. Classify the data type → route to the analysis skill
Match columns against the signals below. Invoke the matching specialist skill and
follow ITS instructions for the actual analysis. If a dump satisfies more than one
signal set (e.g., a combined export), run each relevant skill and stitch the
findings into one report.

| Route to skill | Trigger signals in the columns/values |
|---|---|
| `keyword-breakdown` | search term, keyword, query, match type, ST report, customer search term, targeting (keyword-level) |
| `item-performance` | ASIN, item id, SKU, child/parent item, Buy Box, eligibility, suppression, catalog, product title (product is the row) |
| `placement-performance` | placement, top of search, product page, rest of search, home page, bid multiplier (placement), placement type |
| `device-performance` | device, platform (app/desktop/mobile), mobile vs desktop, app vs web, device type |

Disambiguation rules:
- A "Platform" column whose values are app / desktop / mobile is **device** data
  (Walmart labels device as "Platform"). A "Platform" column naming a retailer is not.
- "Bid multiplier" alone is ambiguous — decide by the dimension it modifies
  (placement vs. device).
- If still ambiguous after inspecting values, state your best inference, proceed,
  and flag the assumption. Ask only if genuinely undecidable.

### 3. Identify the client and pull goals LIVE
- Infer the client + business unit + retailer from the data (profile name, campaign
  naming, retailer).
- Fetch that client's goals from the **Client AI Goal Intake Form** (Google Sheet)
  using the connected Google Sheets connector. Source of truth:
  `https://docs.google.com/spreadsheets/d/1nn3BMCJpY2LGSJoA8J6Z9SdlbyLJqapVmCE6SEgCeBU/edit`
  Read `references/client-goals.md` for the sheet layout, tab names, and the fields
  to extract.
- Match the right tab/section to the client AND the retailer in the data (e.g.,
  Zevia has separate Amazon / Walmart / Instacart goal blocks).
- If goals cannot be fetched (no connector access), say so explicitly and ask the
  user to paste the relevant goal block rather than inventing targets.

### 4. Benchmark actuals vs. goals
- Compare the analysis output against the client's Primary KPI(s), Secondary goals,
  budget caps, and pacing.
- Honor every "Known Sensitivities" entry as a hard constraint, including:
  - **Never blend reporting across business units** (e.g., Canon Printer vs. Camera;
    Advantice's Kerasal / Dermoplast / New Skin must be reported separately).
  - Client-specific spend rules (e.g., Zevia ≤25% branded spend).
  - Seasonal / shelf-reset notes that change what spend should do.
- If a goal metric (e.g., NTB, SOV, HHP) is NOT present in the dump, say so and tell
  the user which report to pull — do not fabricate it.

### 5. Output
- Lead with the bottom line, then the specialist skill's tables.
- A goal-benchmark table: each goal → status (on/under/over) → one-line read.
- A prioritized recommendation list from the specialist skill(s), each tied to a
  specific goal or sensitivity, labeled by priority and effort.
- Offer concrete next actions (e.g., generate a bid/modifier upload file, run a
  second skill on a companion report).

## Output format
Follow Code3 house style: bullets for insights, tables for data, bottom line first.
Use retail media terminology naturally (ROAS, ACOS, CVR, CTR, CPC, NTB, SOV, HHP,
share of voice). Be concise and direct.

## References
- `references/client-goals.md` — Intake-form layout, tab map, fields to extract,
  and the per-client sensitivities to enforce.
