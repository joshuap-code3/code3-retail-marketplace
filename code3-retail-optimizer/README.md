# Code3 Retail Optimizer

An optimization agent for Code3's retail media team. Drop in any ad-platform data
dump and it figures out what kind of report it is, runs the right analysis, pulls
the client's goals from the shared intake sheet, and hands back findings plus
prioritized optimization recommendations measured against those goals.

## What it does
1. **Classifies** the data dump (keyword / item / placement / device) by inspecting columns.
2. **Routes** to the matching analysis skill and runs the full analysis.
3. **Pulls client goals live** from the Client AI Goal Intake Form (Google Sheet).
4. **Benchmarks** actuals vs. Primary/Secondary goals and enforces each client's
   known sensitivities.
5. **Recommends** prioritized actions tied to goals (bid/modifier changes, negatives,
   harvests, creative/structural moves).

## Skills included
| Skill | Handles |
|---|---|
| `optimization-router` | Entry point — classification, routing, goal benchmarking |
| `keyword-breakdown` | Search-term / keyword reports |
| `item-performance` | ASIN / SKU / item reports |
| `placement-performance` | Placement / top-of-search reports |
| `device-performance` | Device (app / desktop / mobile) reports |

## How to use
Upload or paste a report and say "analyze this" or "optimize this." You don't need
to name the report type — the router detects it. Name the client/retailer only if
it isn't obvious from the file.

## Requirements
- **Google Sheets connector** — each user authenticates their own; must have access
  to the Client AI Goal Intake Form. The router reads goals from it live.
- Source data exports from Amazon Ads, Walmart Connect, Instacart, Kroger, Target
  Roundel, Pacvue, or Skai (CSV/XLSX).

## Dependencies & gotchas
- **Goal-sheet layout is a dependency.** The router parses the intake form's tab and
  field structure. If the sheet is reformatted, update
  `skills/optimization-router/references/client-goals.md` to match.
- **Goals are read live**, so they're only as current as the sheet. Keep "Last
  Updated" current per client block.
- **Hard sensitivities are enforced**: never blend Canon Printer/Camera; report
  Advantice's three brands separately; Zevia ≤25% branded spend.

## Versioning
Semver in `.claude-plugin/plugin.json`. Bump on every change and note it below.

### Changelog
- **0.1.0** — Initial release. Router + 4 analysis skills. Walmart device-modifier
  ("Platform") support reflected in device-performance reference.
