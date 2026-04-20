---
name: chief-pipeline
user-invocable: false
description: CEO-level pipeline briefing focused on active open deals — stage distribution, deal health, forecast close dates, and weighted pipeline. Use when the user asks about pipeline, forecast, deal status, revenue outlook, quota attainment, deal velocity, "pipeline update", "forecast update", "where are we on revenue", "how's the pipeline", "deal update", or "what's closing this quarter". Scope is deals only — for lead flow, qualification rates, and top-of-funnel analysis use /funnel instead.
---

# Pipeline Update — CEO Briefing

You produce a CEO-level pipeline briefing covering **active open deals** — stages, amounts, forecast close dates, deal health, and revenue outlook. You do not analyze lead flow or qualification rates; that belongs to `/funnel`.

Pull live deal data from HubSpot, deal-related context from Slack, and forecast/strategy context from Notion.

## Before Starting

1. Read `chief-context/company.yaml` for current pipeline totals, segments, quarterly projections, and ARR
2. Read `chief-context/org.yaml` for sales team structure and deal owners
3. Determine the reporting period: default to current month + current quarter unless the user specifies otherwise

## Data Pipeline

### Step 1 — Pull Deal Data from HubSpot (Primary Source)

Load HubSpot tools via ToolSearch, then execute the following queries. **Run all four queries in parallel:**

**Query A — Active Pipeline (all open deals):**
Search `deals` where `dealstage` NOT IN closed won/lost stages. Properties to pull:
- `dealname`, `amount`, `hs_arr`, `hs_acv`, `dealstage`, `closedate`, `hubspot_owner_id`, `pipeline`, `createdate`, `notes_last_updated`

**Query B — Closed Won this quarter:**
Search `deals` where `dealstage` IN [`22273577`, `52262058`] AND `closedate` GTE start of current quarter.
Same properties as above.

**Query C — Closed Lost this quarter:**
Search `deals` where `dealstage` IN [`22273578`, `52262059`] AND `closedate` GTE start of current quarter.
Same properties as above.

**Query D — Deals closing this month:**
Search `deals` where `closedate` GTE start of current month AND `closedate` LTE end of current month AND `dealstage` NOT IN closed lost stages.
Same properties as above.

**Pagination:** Check `total` in every response. If total > limit, paginate with `offset` to get all results.

**Owner resolution:** Use `search_owners` to map `hubspot_owner_id` to names for display.

### Step 2 — Pull Deal Context from Slack

Search Slack for recent deal-related discussions. Run searches in parallel:

- Search for deal names from the top 5-10 active deals by amount (use `slack_search_public_and_private`)
- Search channels likely to contain deal discussions: look for channels matching patterns like `#sales`, `#deals`, `#revenue`, `#pipeline`
- Search for recent messages containing "close", "contract", "signed", "slipped", "push", "lost", "won" in sales-related channels
- Time range: last 14 days

Extract: deal momentum signals (positive/negative), blockers mentioned, CEO involvement needed, competitive mentions.

### Step 3 — Pull Forecast Context from Notion

Search Notion for pipeline/forecast-related documents:

- Query for pages matching "pipeline", "forecast", "revenue", "quota", "bookings"
- Query for recent meeting notes from pipeline review meetings
- Time range: last 30 days

Extract: forecast commitments, pipeline review decisions, deals discussed as at-risk or upside.

### Step 4 — Synthesize the Briefing

Combine all data into the output format below. Cross-reference:
- HubSpot deal amounts with Slack sentiment (is the team confident or concerned?)
- Close dates with Slack signals (any mentions of deals slipping?)
- Active deals with Notion pipeline review notes (was this deal flagged?)
- Compare current pipeline totals against `company.yaml` projections

## Deal Stage Reference

### Sales Pipeline
| Stage | Internal Value | Funnel Position |
|-------|---------------|-----------------|
| Pre Qualification | 1026803210 | Top |
| Nurture | 100506807 | Top |
| New Opportunity | 22858163 | Top |
| Stalled | 174693016 | Stalled |
| Discovery | 22787919 | Mid |
| Post-Demo Activation | 22273575 | Mid |
| Engaged | 22273576 | Mid |
| Qualified Evaluation | 22170791 | Bottom |
| Walk to Close | 22170792 | Bottom |
| Closed Won | 22273577 | Closed |
| Closed Lost | 22273578 | Closed |

### Channel/Partner Pipeline
| Stage | Internal Value |
|-------|---------------|
| New Channel Opportunity | 52262053 |
| Partnership Scoping | 52262054 |
| Presentation Scheduled | 52262055 |
| Contract Sent | 52262057 |
| Closed Won | 52262058 |
| Closed Lost | 52262059 |

### Funnel Groupings for Reporting

Use these groupings when categorizing deals:
- **Top of Funnel:** Pre Qualification, Nurture, New Opportunity, New Channel Opportunity
- **Mid Funnel:** Discovery, Post-Demo Activation, Engaged, Partnership Scoping, Presentation Scheduled
- **Bottom of Funnel:** Qualified Evaluation, Walk to Close, Contract Sent
- **Stalled:** Stalled (flag any deal here > 30 days)
- **Closed:** Closed Won, Closed Lost

## Forecast Methodology

### Monthly Forecast
- **Commit:** Bottom-of-funnel deals with close dates this month + Slack signals confirming momentum
- **Best Case:** Commit + mid-funnel deals with close dates this month that show positive signals
- **Pipeline:** All open deals with close dates this month

### Quarterly Forecast
- **Commit:** Closed won this quarter + bottom-of-funnel deals with close dates this quarter
- **Best Case:** Commit + mid-funnel deals with close dates this quarter
- **Pipeline:** All open deals with close dates this quarter
- **Attainment:** Closed won / quarterly target (from `company.yaml` q2_projected)

### Weighted Pipeline
Apply stage-based probability weights for weighted pipeline calculation:
| Funnel Position | Weight |
|----------------|--------|
| Top of Funnel | 10% |
| Mid Funnel | 30% |
| Bottom of Funnel | 70% |
| Stalled | 5% |

## Output Format

Use `/chief-memo` conventions. Follow the template in `templates/pipeline-update.md`.

### Required Sections

1. **Executive Summary** — 3-5 sentences: Where we are vs. plan, biggest deal movements, headline risk or opportunity, forecast confidence.

2. **Quarterly Scorecard** — Table: Closed Won (ARR), Quarterly Target, Attainment %, Pipeline Coverage, Weighted Pipeline, Win Rate, Avg Deal Size, Avg Days to Close.

3. **Monthly Forecast** — Table with Commit / Best Case / Pipeline rows showing deal count and total amount. Call out specific deals in each category.

4. **Key Deal Movements** — The 5-10 most important deal updates this period. For each:
   - Deal name, amount, owner
   - Stage movement (from → to)
   - Context from Slack/Notion (what's actually happening)
   - Next step and expected timing
   - Flag if CEO attention needed

5. **Pipeline by Segment** — Table breaking down pipeline by segment (E-commerce, SaaS, Manufacturing, Channel/Partner). Compare to `company.yaml` segment data.

6. **Pipeline by Stage** — Funnel visualization showing deal count and total amount at each stage grouping (Top / Mid / Bottom / Stalled).

7. **Risks & Flags** — Deals that need attention:
   - Deals with close dates that have passed (slipped)
   - Deals stalled > 30 days
   - Large deals (> $100K) in early stages with aggressive close dates
   - Deals where Slack signals conflict with HubSpot stage (team worried but deal shows progressing)
   - Pipeline coverage < 3x quarterly target

8. **Upside Opportunities** — Deals that could accelerate or expand:
   - Deals moving faster than typical velocity
   - Expansion signals from existing customers
   - Multi-product or platform deals

## Slack Output Format

When posting to Slack, use a condensed mrkdwn version:
- Lead with the quarterly scorecard as a code block
- Bullet the top 5 deal movements
- Flag risks with :warning:
- Flag wins with :white_check_mark:
- Keep under 2000 characters for readability

## Rules

- Lead with conclusions, not data. "We're tracking 15% behind plan" is better than a table the CEO has to interpret.
- Every deal mentioned must include the amount and owner name — no anonymous deals.
- Use ARR (`hs_arr`) when available, fall back to `amount`, and note which you're using.
- Compare current state to `company.yaml` projections. Call out divergence explicitly.
- If a deal appears in HubSpot but has no Slack activity in 14 days, flag it as potentially stale.
- If HubSpot data conflicts with Slack signals, flag the discrepancy — don't silently pick one.
- Do not fabricate deal data. If HubSpot returns no results, say so.
- If a data source is unavailable, state what's missing and proceed with what's available.
- Quantify everything. "Pipeline is healthy" means nothing. "$9.8M across 37 deals with 3.2x coverage" is useful.
- Round dollar amounts to nearest $K for deals, nearest $M for totals.

## MCP Dependencies

| MCP Server | Role | Required? |
|-----------|------|-----------|
| **HubSpot** | Primary source for all deal data, stages, amounts, owners | Required — skill cannot function without it |
| **Slack** | Deal context, momentum signals, risk flags from sales discussions | Optional — enriches the briefing but core data comes from HubSpot |
| **Notion** | Forecast docs, pipeline review notes, strategy context | Optional — provides qualitative overlay |

## Composition

- `/chief-board` can pull from this skill for the "Pipeline & Revenue" section of board materials
- `/chief-investor` can use the quarterly scorecard for investor meeting prep
- `/chief-fundraise` can reference pipeline health when updating fundraise materials
- `/chief-competitive` can cross-reference deal context with competitive intelligence
- `/chief-memo` handles the output formatting conventions
