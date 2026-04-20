---
name: funnel
description: Lead funnel analysis — lead volume by source, lead-to-qualified conversion, and qualified-to-deal conversion. Use when the user asks about lead flow, lead conversion, funnel velocity, top-of-funnel health, lead quality, lead sources, qualification rate, or wants to compare funnel performance across time periods.
argument-hint: "[optional: time period, e.g. 'last 45 days vs prior' or 'Q2 vs Q1']"
allowed-tools: mcp__hubspot__search_crm_objects mcp__hubspot__get_crm_objects mcp__hubspot__get_properties mcp__hubspot__search_properties mcp__hubspot__get_user_details mcp__hubspot__search_owners ToolSearch
---

# Funnel Analysis Skill

You produce a lead funnel analysis covering lead volume by source, lead-to-qualified conversion, and qualified-to-deal conversion — using live HubSpot data.

## Funnel Definition

| Step | Object | What It Means | Key Field |
|------|--------|--------------|-----------|
| **Lead** | Contact | New contact created | `createdate` on contacts |
| **Qualified Lead** | Contact → Company | Sales rep moves contact to Opportunity lifecycle stage; work shifts to the **company** object | `hs_v2_date_entered_opportunity` on contacts |
| **Deal** | Deal | Deal object created in HubSpot | `createdate` on deals (your sales pipeline ID — see Setup) |

**Object-level architecture:**
- Leads come in at the **contact** object — count leads here
- Once qualified, work happens at the **company** object — lead source lives here
- Once a deal is created, work moves to the **deal** object

**Lead source field:** Your CRM may have a custom lead source field on the **company** object (manually set at qualification). Check your company properties for a field like `lead_source` or a company-specific custom field. Do NOT use `hs_latest_source` on contacts — that tracks web session origin, not business source intent, and will show misleading results for manually-prospected contacts.

> **Do not use:** `lifecyclestage = marketingqualifiedlead` (MQL), `lifecyclestage = salesqualifiedlead` (SQL), or `hs_lead_status`. These fields are commonly unused or inconsistently maintained. The qualification step is the lifecycle stage transition to Opportunity, tracked via `hs_v2_date_entered_opportunity`.

---

## Setup

**Configure your pipeline ID** — before running, find your sales pipeline ID in HubSpot (Settings → Sales → Pipelines) and either:
- Read it from `chief-context/company.yaml` if configured there, or
- Use `mcp__hubspot__get_properties` with objectType `deals` and query `pipeline` to look it up

Load HubSpot MCP tools via ToolSearch before any queries:
```
ToolSearch({ query: "select:mcp__hubspot__search_crm_objects,mcp__hubspot__get_properties,mcp__hubspot__search_owners" })
```

---

## Reporting Periods

Default: compare **last 45 days** vs. **prior 45 days**.
- Recent: today minus 45 days → today
- Prior: today minus 90 days → today minus 45 days

If the user specifies a different window (e.g. "Q2 vs Q1", "last 30 days"), adjust accordingly.

---

## Data Queries

Run all queries in parallel. Load HubSpot tools first.

### Block A — Lead Volume

**A1. Leads created — recent period:**
Search `contacts` where `createdate` GTE recent_start AND `createdate` LTE today.
Properties: `createdate`, `lifecyclestage`, `hs_latest_source`, `hs_analytics_source`, `hubspot_owner_id`
Limit 1 (use `total` for count). Also pull a sample of 20 to analyze source distribution.

**A2. Leads created — prior period:**
Same query, date range shifted to prior period.

### Block B — Qualified Leads (Lead → Opportunity transition)

**B1. Activity view — recent period:**
Search `contacts` where `hs_v2_date_entered_opportunity` GTE recent_start AND `hs_v2_date_entered_opportunity` LTE today.
Properties: `hs_v2_date_entered_opportunity`, `hs_v2_date_entered_lead`, `lifecyclestage`, `createdate`, `hubspot_owner_id`, `hs_latest_source`
Pull up to 100 (paginate if total > 100) — full set needed for velocity calculation.

**B2. Activity view — prior period:**
Same query, shifted date range. Pull up to 100.

**B3. Cohort view — recent period leads that got qualified:**
Search `contacts` where `createdate` GTE recent_start AND `createdate` LTE today AND `hs_v2_date_entered_opportunity` HAS_PROPERTY.
Use total for count.

**B4. Cohort view — prior period leads that got qualified:**
Same, shifted date range.

### Block C — Deals Created

**C1. Deals created — recent period:**
Search `deals` where `pipeline = [YOUR_PIPELINE_ID]` AND `createdate` GTE recent_start AND `createdate` LTE today.
Properties: `dealname`, `amount`, `dealstage`, `createdate`, `hubspot_owner_id`, `closedate`, `hs_lastmodifieddate`
Pull all (paginate if total > 50).

**C2. Deals created — prior period:**
Same, shifted date range.

### Block D — Disqualification Signal

**D1. Unqualified contacts — recent period:**
Search `contacts` where `createdate` GTE recent_start AND `hs_lead_status = UNQUALIFIED`.
Use total for count. (Note: `hs_lead_status` is sparsely maintained — low counts are expected; surface what exists.)

**D2. Prior period same.**

### Block E — Lead Source Breakdown

Query **companies** (not contacts) for the lead source field. The lead source lives on the company object because that's where qualified-lead work happens.

**E1. Companies created — recent period:**
Search `companies` where `createdate` GTE recent_start AND `createdate` LTE today.
Properties: `createdate`, `name`, and your lead source property (check your company properties — look for a custom field like `lead_source`, `acquisition_source`, or similar manually-set field).
Pull all (paginate if total > 100).

**E2. Companies created — prior period:**
Same, shifted date range.

Aggregate by lead source value. Flag the unset/null percentage — manual fields often have 20–40% untagged.

> **Do NOT aggregate `hs_latest_source` from contacts** — this tracks web session origin and shows misleading results (e.g., 100% OFFLINE) for manually-prospected contacts. Always use the company-level custom lead source field.

---

## Calculations

From the raw counts, compute:

| Metric | Formula |
|--------|---------|
| Lead → Qualified rate (cohort) | Qualified from cohort / Leads created in period |
| Lead → Qualified rate (activity) | Qualifications in period / Leads in period |
| Qualified → Deal rate | Deals created in period / Qualifications in period |
| Overall Lead → Deal rate | Deals created / Leads created |
| Period-over-period Δ | (Recent - Prior) / Prior, expressed as % change |

> **Cohort vs. Activity:** Always present both views. Cohort rate is lower for recent periods (less time to progress) — call this out explicitly rather than letting it read as a decline.

### Velocity Calculation (from B1/B2 full record set)

For each contact in B1 and B2, compute `lag_days = (hs_v2_date_entered_opportunity - createdate) / 86400000`.

Classify each contact:
- **Batch-qualified**: lag_days < 1 (same-day qualification — AE imports and qualifies contacts from the same org simultaneously)
- **Active-lead**: lag_days between 1 and 90 (individually prospected, required follow-up)
- **Zombie lead**: lag_days > 90 (old contact being re-qualified — backlog cleanup, not current funnel activity)

Report these five metrics:

| Metric | How to compute |
|--------|---------------|
| Total qualified | total from B1/B2 |
| Same-day batch qualified | count where lag_days < 1 (as % of total) |
| Mean velocity — active leads | mean lag_days where 1 ≤ lag_days ≤ 90 |
| Median velocity | median lag_days across all contacts |
| Zombie leads re-qualified | count where lag_days > 90 (note max lag seen) |

> **Zombie leads distort the mean.** Always exclude lag_days > 90 when computing the "active" mean. A contact created years ago being qualified today is CRM backlog cleanup — it's not a signal about current funnel health. Surface the zombie count separately so the reader understands how much cleanup is happening.

---

## Output Format

Follow the template in `templates/funnel-report.md`.

### Required Sections

1. **Headline** — One-sentence call on funnel health. "Funnel is accelerating: +30% lead volume, qualification pace keeping up."

2. **Period Comparison Table** — The core comparative table (see template).

3. **Lead Sources** — Where leads are coming from and which sources convert best. Flag if one source dominates.

4. **Conversion Analysis** — Lead→Qualified and Qualified→Deal rates with period comparison. Use both cohort and activity views. Explain recency bias for the recent cohort.

5. **Velocity** — How quickly leads are being qualified (days from created to qualified). Faster = better.

6. **Deal Quality from this Funnel** — Of deals created in each period, what stage are they at now? How many closed won vs. in flight?

7. **Flags & Recommendations** — What's working, what's stalled, what the AE should prioritize.

---

## Rules

- Never use MQL lifecycle stage or `hs_lead_status` for qualification — use `hs_v2_date_entered_opportunity` only.
- Always present both cohort and activity views for qualification rate — they tell different stories.
- Call out recency bias explicitly when the recent cohort shows a lower rate than the prior cohort.
- Lead source lives on the **company** object, not contacts — never use `hs_latest_source` on contacts for lead source analysis.
- Never report "~0 days" as the velocity summary — always compute the 5-metric breakdown (batch %, active mean, median, zombie count).
- Exclude zombie leads (lag_days > 90) from the active velocity mean — they signal CRM backlog cleanup, not current funnel pace.
- Every number should be actionable. Don't just report 22% → 18% qualification rate; say what it means.
- Pipeline and deal health analysis belongs in `/chief-pipeline`, not here. This skill stops at deal creation.

---

## MCP Dependencies

| MCP Server | Role | Required? |
|-----------|------|-----------|
| **HubSpot** | All lead, contact, and deal data | Required |

---

## Composition

- `/chief-pipeline` handles everything after deal creation — stage progression, forecast, close dates
- `/chief-pipeline` can reference this skill when it needs top-of-funnel context
- `/customer-360` can call this skill when analyzing a specific customer's entry into the funnel
