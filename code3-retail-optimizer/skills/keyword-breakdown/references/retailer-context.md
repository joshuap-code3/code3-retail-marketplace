# Retailer Context

Apply these platform-specific considerations automatically when the data source is
identifiable.

## Amazon

- Match types: exact, phrase, broad, auto (close variant, loose variant, substitute,
  complement)
- Key metrics: spend, sales, ACOS, ROAS, impressions, clicks, CTR, CVR, orders, NTB%,
  NTB orders, NTB sales
- Auto campaign segments (close variant vs. loose variant) behave differently — flag
  when auto terms are cannibalizing exact targets
- ACOS benchmarks vary significantly by category — flag outliers but don't apply a
  single threshold across all terms

## Walmart Connect

- Match types: exact, phrase, broad (auto campaigns also available)
- Key metrics: spend, sales, ROAS, impressions, clicks, CTR, CVR, orders
- Attribution windows differ from Amazon — note when comparing cross-retailer
- Walmart search data is often less granular than Amazon — flag when data density
  is low

## Instacart

- Keyword-level data may be limited depending on campaign type
- Key metrics: spend, sales, ROAS, impressions, clicks, CTR, attributed purchases
- Category-level dynamics are important — note when a term is generic to a category
  vs. specific to a brand

## Kroger Precision Marketing

- Data exports may have different column naming conventions — adapt automatically
- Key metrics: spend, sales, ROAS, impressions, clicks, household reach

## Target Roundel

- Data structure may differ — adapt column mapping as needed
- Key metrics: spend, sales, ROAS, impressions, clicks, orders
