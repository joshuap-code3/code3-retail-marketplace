# Retailer Device Context

Platform-specific device breakout availability, device taxonomies, bid control
mechanics per device type, data granularity limits, and known performance norms
per retailer. Read before any device analysis — especially before making any
modifier or bid recommendations — when the retailer is identifiable from the data.

---

## Critical Read First: Device Bid Control Availability

Device-level bid modifiers are NOT available on most retail media Sponsored Products
placements. Before running any bid modifier recommendation, confirm the campaign type
and platform against this table:

| Platform | Campaign Type | Device Bid Control | Notes |
|----------|--------------|-------------------|-------|
| Amazon | Sponsored Products | ❌ Not available | No device-level modifiers for SP |
| Amazon | Sponsored Brands | ❌ Not available | No device-level modifiers for SB |
| Amazon | Sponsored Display | ⚠️ Limited | Some audience tactics allow device targeting at setup, not modifier |
| Amazon | DSP | ✅ Available | Device bidding available in Amazon DSP |
| Walmart Connect | Sponsored Products | ✅ Available | "Platform" modifier in Walmart Connect UI — supports Desktop, Mobile, App |
| Walmart Connect | Display / Video | ✅ Available | Device targeting and modifiers available |
| Instacart | All ad types | ❌ Limited | Primarily app-based; limited device controls |
| Kroger KPM | Display / Programmatic | ✅ Partial | Device targeting available in programmatic |
| Target Roundel | Display / Programmatic | ✅ Partial | Device targeting available in some campaign types |

**Default rule:** If the dataset comes from Sponsored Products on Amazon, there are
no device-level bid modifiers to recommend. Walmart Connect is an exception —
it supports device-level bid modifiers via the "Platform" setting in the UI.
For all other retailers on SP, pivot to creative, UX, and structural recommendations.

---

## Amazon

### Device Breakout Availability
- **Sponsored Products:** Device data is available in reporting (desktop vs. mobile
  vs. tablet) but no device-level bid modifier exists for SP campaigns
- **Sponsored Brands:** Device data available in reporting; no device modifier
- **Sponsored Display:** Limited device breakout; some audience targeting options
  allow device specification at campaign setup but not as an ongoing modifier
- **Amazon DSP:** Full device targeting and bid adjustment available — mobile app,
  mobile web, desktop, tablet, connected TV (CTV)

### Device Types in Amazon Reports
- Desktop
- Mobile (may include both app and mobile web — check if broken out)
- Tablet
- Note: Amazon does not always distinguish Mobile App from Mobile Web in SP reports
  — if this distinction is needed, it requires DSP or third-party data

### Performance Norms (Amazon SP)
- Desktop typically shows higher CVR than mobile for most categories — cross-device
  shopping behavior (browse mobile, buy desktop) is common
- Mobile typically drives more impressions and clicks but lower CVR
- Tablet often performs similarly to desktop in conversion rate
- App users (where measurable via DSP) tend to have higher CVR than mobile web —
  they are logged in, have saved payment info, and are typically existing Amazon
  customers

### Data Export Notes
- Amazon Ads console: Reports → Sponsored Products → device-level report
- Device column label: "Device" — values typically "Desktop", "Mobile", "Tablet"
- Pacvue and Skai preserve Amazon device labeling
- Note: Amazon device reports are campaign-level — no ad group or keyword device
  breakout in native reporting

### Key Analytical Implication
For Amazon SP, device analysis is primarily a diagnostic and creative strategy tool,
not a bid optimization tool. Use it to understand audience behavior, identify CVR
gaps, and inform creative or PDP prioritization. Direct bid action requires moving
to Amazon DSP where device controls exist.

---

## Walmart Connect

### Device Breakout Availability
- **Sponsored Products:** Device data available in reporting; Walmart Connect
  supports device-level bid modifiers via the **"Platform" setting** in the campaign
  UI — this is Walmart's term for device type targeting and bid adjustment
- **Display / Video:** Device targeting and modifiers available

### Platform (Device) Modifier Mechanics
- Walmart's device modifier is labeled **"Platform"** in the Walmart Connect UI —
  not "device" — note this when cross-referencing with exported data column names
- Modifier is applied at the campaign level
- Supported platform segments: **Desktop**, **Mobile**, **App**
- When data includes a "Platform" column, treat it as the device breakout
- Modifier recommendations for Walmart SP follow the same CVR-based logic as
  any other platform with device controls — flag which platform segment warrants
  an increase or decrease based on CVR vs. account average and the client's goal

### Device Types in Walmart Reports
- Desktop
- Mobile (mobile web)
- App (Walmart app — significant channel; treat as distinct from mobile web)
- Column label in exports may read "Platform" rather than "Device" — normalize
  to canonical device labels before cross-retailer comparison

### Performance Norms (Walmart)
- Mobile shopping is significant on Walmart — Walmart's app has high engagement
  among its core customer base
- App users on Walmart tend to be higher-intent and more loyal — App platform
  segment often shows stronger CVR than Mobile Web
- Desktop CVR may be higher for high-consideration purchases
- The mobile vs. desktop CVR gap on Walmart may be narrower than Amazon for
  grocery and household staples — Walmart's core customer base is more mobile-native

### Key Analytical Implication
Unlike Amazon SP, Walmart Connect SP supports direct device-level bid modifiers
via the Platform setting. Device analysis on Walmart should produce specific
Platform modifier recommendations where data is sufficient (10+ clicks per segment).
Apply the same CVR-based modifier logic used for placement modifiers.

---

## Instacart

### Device Breakout Availability
- Instacart is primarily an app-based platform — the vast majority of shopping
  occurs on the Instacart mobile app
- Desktop web exists but represents a small share of Instacart usage
- Formal device-level breakout in advertising reports is limited — flag when
  device data is not present or not meaningful due to app dominance

### Device Types
- Mobile App (dominant)
- Desktop Web (minor share)
- Note: If a dataset shows near-100% mobile app, this is expected — not a data error

### Performance Norms (Instacart)
- App-dominant platform — CVR norms are calibrated for app shoppers
- Desktop web users on Instacart may skew older or less frequent shoppers
- The concept of a "browse mobile, buy desktop" gap is less relevant on Instacart
  than Amazon — Instacart app users complete their purchase in-app

### Key Analytical Implication
Device analysis on Instacart is primarily about confirming audience context
(app-dominant shopping behavior) rather than identifying optimization levers.
If desktop web is underperforming, that is expected and not a bid problem.

---

## Kroger Precision Marketing (KPM)

### Device Breakout Availability
- On-site (Kroger.com / app): device data available; app vs. web distinction
  possible in some reporting configurations
- Off-site / programmatic: full device targeting and breakout available through
  KPM's programmatic stack
- Loyalty-based attribution may make device performance appear differently than
  click-based platforms — a mobile impression that leads to an in-store purchase
  may be attributed but the device of purchase was physical (in-store)

### Device Types
- Mobile App
- Mobile Web
- Desktop
- Off-site (programmatic — full device targeting available)

### Key Analytical Implication
KPM's loyalty data integration means device performance data may include in-store
attribution — a mobile ad may receive credit for a purchase made in-store, not on
the device. Note this when interpreting CVR by device on KPM.

---

## Target Roundel

### Device Breakout Availability
- Target.com / app: device breakout available in some reporting configurations
- Off-site programmatic: full device targeting and breakout available
- GuestID-based attribution — same cross-device and in-store attribution caveats
  as KPM apply here

### Device Types
- Mobile App (Target app is widely used)
- Mobile Web
- Desktop
- Off-site (device targeting available)

### Performance Norms (Target Roundel)
- Target's app has strong engagement — app users may show higher CVR similar to
  Amazon app users
- Target's in-store integration means some device-attributed conversions are
  actually in-store purchases driven by the ad — keep in mind when comparing CVR
  across devices

---

## Cross-Retailer Device Notes

### Normalizing for Comparison
When comparing device performance across retailers:
1. Normalize device labels first (see canonical mapping in SKILL.md)
2. Note attribution model differences — Amazon click-based, KPM loyalty-based,
   Roundel GuestID-based — these make direct CVR comparisons misleading
3. Note app dominance context — Instacart is nearly 100% app; comparing its mobile
   share to Amazon's mobile share is not meaningful

### The Browse-to-Buy Gap
A common cross-retailer pattern: mobile drives more impressions and clicks, desktop
drives more conversions. This is most pronounced on Amazon and less pronounced on
app-first platforms (Instacart, Walmart app users). When this pattern appears, it
typically indicates:
- Cross-device shopping behavior (not a platform problem)
- Mobile PDP experience friction (potential fix: mobile creative and page optimization)
- Audience segment difference by device (app users = existing customers = higher intent)

Quantify the gap (mobile CVR as % of desktop CVR) and compare across retailers.
A gap that exists on Amazon but not Walmart may indicate an Amazon mobile PDP issue
rather than a universal behavior pattern.

### CPC Differences by Device
CPC norms differ by device and retailer. On Amazon, mobile CPCs for SP tend to be
lower than desktop CPCs for the same terms — but with lower CVR. The cost-per-order
often ends up similar or in favor of desktop. Always evaluate CPC in the context
of CVR and cost-per-order, not CPC alone.

### Creative Asset Considerations by Device
Flag these creative implications when device data warrants it:
- Mobile (< 430px width): hero image dominant, title truncated — first 30 characters
  of product title matter most
- Desktop (> 1024px): more title visible, secondary image real estate matters
- App: navigation is touch-based — CTA clarity and product image quality are primary
- Tablet: often renders closer to desktop; can use desktop creative effectively
