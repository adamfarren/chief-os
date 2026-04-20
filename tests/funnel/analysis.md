# Test Analysis: funnel

## Test Scenario

CEO of Meridian Ledger runs `/funnel` with no arguments. Skill executes the default 45-day comparison (Mar 1 – Apr 15 vs. Jan 15 – Mar 1, 2026) using live HubSpot data. All HubSpot MCP queries (Blocks A–E) return real data. This is a live-data test, not a simulated test.

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Loads HubSpot tools via ToolSearch before any query | **PASS** — ToolSearch called first; all MCP tools loaded before data queries |
| 2 | Runs all Block A–E queries in parallel, not sequentially | **PASS** — A1/A2/B1/B2/B3/B4/C1/C2/D1/D2 queries issued in parallel batches |
| 3 | Uses `hs_v2_date_entered_opportunity` for qualified leads — NOT MQL lifecycle stage or `hs_lead_status` | **PASS** — All B-block queries filter on `hs_v2_date_entered_opportunity`; MQL never referenced |
| 4 | Presents both cohort and activity views for qualification rate | **PASS** — Both rates shown in comparison table with clear labeling |
| 5 | Calls out recency bias explicitly when recent cohort rate is lower | **PASS** — Note included in table and explained in Conversion Analysis section |
| 6 | Queries correct pipeline ID for deal counts | **PASS** — Deals queried against correct sales pipeline |
| 7 | Correctly identifies the qualified→deal rate drop as the primary signal | **PASS** — 28.1% → 19.0% drop flagged as the key finding; connects to deal-creation backlog hypothesis |
| 8 | Lead source breakdown surfaces dominant source and flags concentration risk | **PASS** — Company-level `lead_source` breakdown shown (free_trial 32%, website_form 22%, untagged 34%); growing untagged rate flagged as admin gap |
| 9 | Stops at deal creation — does not bleed into deal stage / forecast analysis | **PASS** — Skill correctly defers deal-stage breakdown to `/chief-pipeline` |
| 10 | Every number is actionable, not just reported | **PASS** — "79 contacts entered Opportunity, only 15 deals created" tied directly to specific admin action for the AE |
| 11 | Output follows funnel-report.md template structure | **PASS** — All 7 sections present: Headline, Funnel Comparison, Lead Sources, Conversion Analysis (with velocity sub-section), Deal Quality, Flags & Recommendations |
| 12 | Headline is one sentence and calls the funnel health accurately | **PASS** — "qualified-to-deal conversion fell sharply" is the correct diagnosis given the data |

## Overall Grade: A

The skill correctly identifies the real problem in the funnel: not lead volume (up 30%), not qualification rate (essentially flat at 22%), but the qualified-to-deal gap (79 qualified contacts, only 15 deals). The actionable recommendation — audit Opportunity-stage contacts and create missing deal records — is specific and immediately executable. The recency bias explanation prevents a false alarm on the cohort rate drop.

Two issues were caught and fixed post-test: (1) lead source was queried from the wrong HubSpot object (contacts vs. companies), and (2) velocity was undersold as "~0 days" instead of computing the batch/active/zombie breakdown. Both corrections are now in the skill, template, and this deliverable.

## Issues Found (Post-Test Corrections Applied)

The following issues were found and fixed in the skill after this test run:

- **Lead source field (fixed):** Initial test used `hs_latest_source` on contacts, which returned 100% OFFLINE — a misleading result for manually-prospected contacts. Correct field is `lead_source` on the **company** object. Skill updated to query companies (Block E), template updated to show company-level source breakdown. Deliverable updated with correct data.
- **Velocity calculation (fixed):** Initial report showed "~0 days (batch-dominant)" with no further breakdown. Skill now computes a 5-metric velocity table: total qualified, % batch-qualified, mean active-lead velocity (excl. zombie leads with lag > 90 days), median, and zombie count. Zombie leads (contacts created years ago being re-qualified) distort the raw mean and must be excluded. Real velocity: recent 4.7 days (active leads), prior 8.3 days — velocity is improving.
- **B1/B2 record limit (fixed):** Skill previously limited B1/B2 to 50 records "for source breakdown," insufficient for computing velocity across full periods. Limit raised to 100 with pagination instruction.
- **Enhancement (open):** A per-owner breakdown would be useful when multiple AEs work the funnel. Consider adding an owner breakdown to Block B if `hubspot_owner_id` is available.
- **Note (by design):** Deal Quality section (Section 6) requires a follow-on `/chief-pipeline` query for stage distribution. This is correct composition behavior, but the template now explicitly pre-prompts the user to run `/chief-pipeline`.
