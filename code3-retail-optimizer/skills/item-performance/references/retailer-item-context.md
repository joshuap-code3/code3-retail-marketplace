# Retailer Item Context

Platform-specific item identifier formats, eligibility signals, suppression causes,
metric definitions, and known data quirks for each retailer. Read before running any
item analysis when the retailer is identifiable from the data.

---

## Amazon

### Item Identifiers
- **ASIN** (Amazon Standard Identification Number) — 10-character alphanumeric,
  starts with B (e.g., B09XXXXXX). This is the primary identifier in all Amazon
  Ads item reports.
- Parent vs. child ASINs: variations (size, color, pack count) are child ASINs
  under a parent ASIN. Performance data is reported at the child level. If a dataset
  mixes parent and child ASINs, flag and ask the user how to handle aggregation.

### Key Metrics (Amazon-Specific)
- **7-day attributed sales** — default attribution window; some accounts use 14-day
- **New-to-brand (NTB) orders/sales/rate** — available in Sponsored Brands and some
  Sponsored Products reports; not always present in item-level exports
- **Glance views** — page views on the product detail page; available in some
  business reports but typically not in ad reports — note if absent
- **ACOS** — natively reported; calculate ROAS as (sales / spend)
- **Units sold** — may differ from orders due to multi-unit purchases

### Eligibility & Suppression Signals
- **Zero impressions with active campaign and non-zero bid** → likely causes:
  - Item suppressed due to policy violation (adult content, restricted category)
  - Item out of stock (FBA inventory = 0)
  - Item losing Buy Box to a third-party seller or Amazon retail
  - ASIN ineligible for the ad type (e.g., variations not enrolled in SB)
  - Listing quality flag (incomplete title, missing images, low review count)
- **Buy Box loss signal:** high clicks, near-zero CVR, item appears in reports but
  orders are zero. Recommend checking Buy Box ownership in Seller Central.
- **Suppression check:** go to Campaign Manager → Items tab → look for suppression
  flags. In Pacvue/Skai, check the item eligibility column if exported.
- **Out of stock:** impressions will drop to zero quickly after stock depletes.
  CVR will collapse before impressions do as Amazon throttles low-inventory items.

### Attribution Notes
- Default attribution: 7-day click-based + 1-day view-based
- Some advertisers use 14-day attribution — note in analysis if the window differs
  from standard, as it affects sales totals
- Cross-ASIN attribution: Sponsored Brands can attribute sales to any item in the
  brand's catalog, not just the advertised item — flag when SB item data shows sales
  on items not in the creative

### Data Export Sources
- **Amazon Ads Console** → Reports → Sponsored Products / Brands → Advertised Product
- **Pacvue** → Item-level exports (typically labeled "Product" or "ASIN" reports)
- **Skai** → Product-level reporting tab

---

## Walmart Connect

### Item Identifiers
- **Item ID** — Walmart's internal numeric identifier (e.g., 123456789)
- **GTIN / UPC** — may appear in some catalog exports; not always present in ad reports
- Item IDs are retailer-specific — the same physical product has a different ID on
  Walmart than its ASIN on Amazon

### Key Metrics (Walmart-Specific)
- **ROAS** — natively reported (Walmart does not use ACOS terminology)
- **Attributed sales** — 3-day or 30-day attribution depending on campaign type;
  always note the window in analysis
- **Add-to-cart rate** — available in some Walmart reports; a useful mid-funnel signal
  when orders are low
- **NTB metrics** — limited availability compared to Amazon; flag if absent

### Eligibility & Suppression Signals
- **Item not buyable:** Walmart suppresses items that fail content quality thresholds
  (missing images, short title, no description). Check Walmart Seller Center item
  quality dashboard.
- **Out of stock:** Walmart rapidly suppresses items with zero inventory. Unlike
  Amazon, there is less throttling — impressions tend to drop more abruptly.
- **Price competitiveness:** Walmart's algorithm heavily weights price. Items that
  are priced above comparable products may receive less organic and paid visibility.
  Low CVR on a well-set-up item often signals a pricing issue on Walmart.
- **Two-day delivery badge:** Items without the two-day delivery tag convert
  significantly worse. Flag items with low CVR if they lack this badge.

### Data Quirks
- Walmart item reports are often less granular than Amazon — fewer columns, less
  NTB data, less placement-level breakout
- Column naming varies between Walmart native exports and Pacvue/Skai pulls —
  always map before analyzing

---

## Instacart

### Item Identifiers
- **UPC** — primary identifier for Instacart item data
- **Product ID** — Instacart's internal identifier; may appear in platform exports

### Key Metrics (Instacart-Specific)
- **Attributed purchases** — primary conversion metric (equivalent to orders)
- **Units per transaction** — relevant for multi-pack or household staple items
- **Share of shelf** — impression share metric; available in some Instacart reports
- NTB and HHP metrics are more central on Instacart than other retailers — flag
  when present as they are highly relevant to grocery category goals

### Eligibility & Suppression Signals
- **Out of stock at retailer level** — Instacart inventory is retailer-specific;
  an item may be in stock at Kroger stores but not Safeway. Stock status affects
  delivery eligibility per fulfillment partner.
- **Item not carried by selected retailers** — items available on Instacart are
  tied to specific retail partners; coverage varies by geography
- **Low share of shelf** — may indicate low bid relative to category competition;
  different from the Buy Box concept but functionally similar

### Data Quirks
- Item-level data granularity varies by campaign type (featured product vs. display)
- Category context matters more on Instacart than other retailers — a generic
  category term performing well often indicates category-level opportunity, not just
  brand opportunity

---

## Kroger Precision Marketing (KPM)

### Item Identifiers
- **UPC** — primary identifier
- **Product ID** — KPM internal identifier

### Key Metrics (KPM-Specific)
- **Household reach** — a primary metric unique to KPM; tied to loyalty card data
- **Sales lift** — sometimes available through KPM's measurement suite
- Standard digital metrics (impressions, clicks, ROAS) also available

### Data Quirks
- KPM exports use non-standard column naming — map carefully before analysis
- Loyalty data integration means KPM can tie ad exposure to in-store purchase,
  which can make ROAS appear higher than other retailers for the same item
- Item-level granularity may be lower than Amazon or Walmart

---

## Target Roundel

### Item Identifiers
- **TCIN** (Target Corporation Item Number) — Target's internal item identifier
- **UPC** — may also appear in catalog exports

### Key Metrics (Target-Specific)
- Standard metrics: impressions, clicks, ROAS, orders, CVR
- **GuestID-based attribution** — Roundel uses Target's loyalty data for attribution,
  which can differ significantly from click-based models on other platforms

### Data Quirks
- Roundel data structure differs from Amazon and Walmart exports — column mapping
  is often required before analysis
- Item-level data granularity varies by ad product type
- Attribution methodology difference should be noted when comparing Roundel ROAS
  to Amazon ROAS for the same item — they are not directly comparable

---

## Cross-Retailer Notes

### Identifier Reconciliation
The same physical product has different identifiers across retailers:
- Amazon: ASIN
- Walmart: Item ID
- Instacart / Kroger / Target: UPC or internal ID

When running cross-retailer analysis, UPC/GTIN is the most reliable bridge identifier
if available. If only retailer-native IDs are present, match by product name and flag
any matches that may be ambiguous (e.g., different pack sizes of the same product).

### Attribution Window Differences
Never compare ROAS directly across retailers without noting attribution window:
- Amazon default: 7-day click / 1-day view
- Walmart default: 3-day or 30-day (varies by campaign type)
- Instacart: typically 14-day
- Kroger: varies, often includes in-store via loyalty card
- Target Roundel: loyalty-based, window varies

Always note the attribution window in cross-retailer comparisons and flag when
windows differ materially between retailers being compared.

### CVR Benchmarking
CVR norms vary significantly by retailer and category. Do not apply a single CVR
threshold across retailers. When flagging low CVR, compare against the account's
own blended CVR for that retailer, not a cross-platform benchmark.
