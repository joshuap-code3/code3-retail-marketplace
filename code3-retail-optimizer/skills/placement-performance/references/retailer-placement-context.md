# Retailer Placement Context

Platform-specific placement taxonomies, modifier mechanics, available ad locations,
modifier ranges, performance norms, and known data quirks per retailer. Read before
any placement analysis when the retailer is identifiable from the data.

---

## Amazon

### Placement Types (Sponsored Products)
Amazon Sponsored Products reports on three named placement tiers:

| Placement Name in Reports | Canonical Name | Description |
|--------------------------|---------------|-------------|
| Top of search (first page) | TOS | First row(s) of search results on page 1. Highest visibility, highest CPC. |
| Product pages | PDP | On competitor or complementary product detail pages, and below-the-fold on search. |
| Rest of search | ROS | All other search result positions — pages 2+, lower on page 1. |

**Performance norms:**
- TOS typically has the highest CTR and often the highest CVR due to shopper intent
  at the top of results. CPC is highest here.
- PDP traffic is often lower-intent (browsing vs. searching) — CVR is typically
  lower than TOS but CPC is also lower. Strong for competitive conquest and
  consideration-stage reach.
- ROS is the cheapest placement. CVR varies — page 2+ shoppers may be more
  deliberate but volume is lower.

**Modifier mechanics:**
- Modifiers are applied at the campaign level (not ad group level) for SP
- Range: 0% to 900% increase above base bid
- 0% modifier = no increase (not a suppression — the base bid still enters the
  auction at that placement)
- Setting a modifier does not guarantee winning that placement — it raises the
  bid submitted to the auction
- Modifiers compound with bid adjustments from rules if automated bidding is active

**Sponsored Brands placements:**
- Top of search (banner, video): banner appears above SP results; video appears
  in search results inline
- Product pages: SB display on PDPs
- SB placements are not modifier-controlled the same way as SP — budget and bid
  determine allocation; note this distinction if SB and SP data are mixed

**Sponsored Display:**
- On-Amazon: product detail pages, below-the-fold search, cart page
- Off-Amazon: external sites and apps (if audience targeting is enabled)
- Placement data for SD is structured differently — may show audience vs. contextual
  targeting segments rather than TOS/PDP/ROS naming

**Data export notes:**
- Placement reports in Amazon Ads console: Reports → Sponsored Products → Placement
- One row per placement per campaign — no ad group breakdown in native placement report
- Pacvue and Skai typically preserve Amazon's placement naming convention

---

## Walmart Connect

### Placement Types
Walmart Connect uses different placement terminology than Amazon. Naming in reports
may vary by export source.

| Placement Name in Reports | Canonical Name | Description |
|--------------------------|---------------|-------------|
| Search In-Grid | Search In-Grid / TOS equivalent | Appears within search results, top positions |
| Buy Box Banner | Buy Box | Appears on product detail pages in the Buy Box area |
| Home Page | Home Page | Walmart.com homepage — high reach, lower purchase intent |
| Browse In-Grid | Browse | Category browse pages, not search-triggered |
| Item Carousel | Carousel | "Customers also bought" and similar modules |

**Performance norms:**
- Search In-Grid is the closest equivalent to Amazon TOS — highest purchase intent
- Buy Box placement on PDPs can be highly effective for conquest and switching
- Home Page has high impression volume but lower CVR — better for awareness and
  NTB goals than direct conversion
- Browse placements serve a mid-funnel shopper — CVR varies by category

**Modifier mechanics:**
- Walmart Connect bid modifiers work differently from Amazon's — placement bid
  adjustments may be set at the campaign level
- Available modifier range and mechanics vary by campaign type and may change
  with platform updates — always verify current platform capabilities
- Note: Walmart's auction algorithm weights relevance and price competitiveness
  alongside bid, so modifier increases do not guarantee placement wins the same
  way they might on Amazon

**Data export notes:**
- Placement breakdown availability varies by campaign type and Walmart Connect
  UI version
- Column naming in Walmart native exports differs from Pacvue/Skai — map carefully
- Walmart placement data is often less granular than Amazon — some campaign types
  may not break out placement performance separately

---

## Instacart

### Placement Types
Instacart placement taxonomy reflects its grocery delivery context.

| Placement / Ad Type | Description |
|--------------------|-------------|
| Search | Appears in search results on Instacart app/web |
| Featured Product | Featured placement at top of category browse pages |
| Display / Banner | Brand awareness placements across the app |
| Shoppable Display | Display units with direct add-to-cart capability |

**Performance norms:**
- Search placements have the highest purchase intent — shoppers are actively looking
  for a product type
- Featured Product placements are strong for NTB and HHP goals — intercepts browsing
  shoppers who may not have searched for the brand
- Display and banner placements are awareness-focused — CVR will be lower but
  reach and NTB rate can be high
- Attribution on Instacart is purchase-based (add to cart and completed order)

**Modifier mechanics:**
- Instacart uses bid-based auctions; placement-level modifier controls are more
  limited than Amazon's explicit modifier system
- Budget and bid level primarily drive placement allocation
- Note when placement data shows share of shelf metrics — these are impression share
  proxies unique to Instacart

---

## Kroger Precision Marketing (KPM)

### Placement Types
KPM placement data may appear as display, search, or on-site vs. off-site.

| Placement | Description |
|-----------|-------------|
| On-site search | Kroger.com and app search results |
| On-site display | Kroger.com and app display placements |
| Off-site / programmatic | External display via KPM's data-driven targeting |

**Performance norms:**
- KPM's strength is loyalty data integration — placements can be targeted to
  specific household purchase history segments regardless of placement type
- ROAS on KPM may appear elevated vs. other retailers due to in-store attribution
  via loyalty card — note this when comparing cross-retailer
- Off-site placements have lower CVR but can be effective for HHP/NTB goals given
  broad reach

**Modifier mechanics:**
- KPM placement modifier mechanics differ from Amazon/Walmart — bid and targeting
  segment selection drive placement allocation more than explicit modifiers
- Flag when placement-level modifier data is not available in the export

---

## Target Roundel

### Placement Types
Roundel placements span Target.com, Target app, and off-site inventory.

| Placement | Description |
|-----------|-------------|
| Search | Target.com and app search results |
| Browse / Category | Category page placements on Target.com |
| Home / Featured | Homepage and featured category modules |
| Off-site | External programmatic inventory via Roundel's data |

**Performance norms:**
- Roundel uses GuestID-based attribution linking ad exposure to in-store and online
  purchase — this can make ROAS appear differently than click-based models
- Never compare Roundel ROAS directly to Amazon ROAS for the same product without
  noting the attribution methodology difference
- Off-site placements have reach advantages but lower direct CVR

**Modifier mechanics:**
- Roundel's bid and placement controls differ from Amazon's explicit modifier system
- Placement allocation is driven by bid level and audience targeting selection
- Flag when explicit modifier data is not present in the export

---

## Cross-Retailer Placement Mapping

When comparing placements across retailers, use this canonical mapping to align
terminology before drawing comparisons:

| Canonical Placement Type | Amazon | Walmart | Instacart | KPM | Roundel |
|--------------------------|--------|---------|-----------|-----|---------|
| Top of Search / Search In-Grid | Top of search | Search In-Grid | Search | On-site search | Search |
| Product / Detail Page | Product pages | Buy Box Banner | — | — | Browse |
| Rest of Search / Lower Funnel | Rest of search | Browse In-Grid | — | — | — |
| Home / Awareness | — | Home Page | Display/Banner | Off-site | Home/Featured |
| Competitive / Cross-Sell | Product pages | Item Carousel | Featured Product | On-site display | — |
| Off-site / Programmatic | Sponsored Display (off) | — | — | Off-site | Off-site |

**Important notes for cross-retailer comparison:**
- Even when placement types are mapped to the same canonical category, performance
  benchmarks differ by platform — do not apply Amazon TOS CVR norms to Walmart
  Search In-Grid without qualifying the comparison
- Attribution windows differ across retailers — always note when comparing ROAS
  or CVR across platforms (see retailer-item-context.md for attribution window details)
- Modifier mechanics are not equivalent across platforms — a 100% TOS modifier on
  Amazon does not mean the same thing as a similar adjustment on Walmart Connect
