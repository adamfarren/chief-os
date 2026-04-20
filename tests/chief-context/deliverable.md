# Deliverable — Scenario 1: View Context

**Generated:** 2026-04-08

## Company

**Meridian Ledger** — AI-powered accounting and financial close platform for mid-market businesses
**Stage:** Series B, preparing Series C

## Key Metrics

| Metric | Value |
|--------|-------|
| ARR | $12.5M |
| ARR Growth YoY | 110% |
| Customers | 87 |
| Burn Rate | $750K/mo |
| Runway | 14 months |

**⚠ Metrics last updated 2026-03-15 (24 days ago).** Recommend refreshing ARR and customer count — these may have changed since last update.

## Strategy

**Annual Goals:**
1. **Hit $20M ARR** (DRI: Sarah Chen) — Grow from $12.5M to $20M through expansion and new logos
2. **Launch AI Agent Platform** (DRI: Marcus Webb) — Ship the agent SDK and marketplace for third-party financial workflows
3. **Expand into manufacturing and professional services** (DRI: Sarah Chen) — Add two new segment verticals beyond e-commerce and SaaS

**Active Initiatives:**

| Initiative | DRI | Status |
|-----------|-----|--------|
| Agent SDK | Marcus Webb | ✅ On Track |
| Enterprise tier | Sarah Chen | ⚠️ At Risk |
| SOC 2 Type II | Devon Park | ✅ On Track |

## Product

**Architecture:** Cloud-native SaaS. React frontend, Python/FastAPI backend, PostgreSQL, deployed on AWS. AI inference via Claude API.

**Key Products:** Ledger OS (core general ledger + close), Agent SDK (developer platform), Customer Portal

**Differentiators:** AI-native from day one, segment-specific workflows, agent extensibility

## Positioning

**Competitive Lanes:**
- vs. Legacy ERPs (NetSuite, Sage Intacct): modern architecture, AI-native, faster implementation
- vs. Vertical finance SaaS (Ramp, Brex): deeper accounting capabilities, agent platform
- vs. AI accounting startups (Numeric, Campfire): full platform, not point solution

**Key Narratives:**
- "The month-end close is broken. The agent-powered ledger is next."
- "We don't sell software, we sell back 2 hours per controller per day."
- "Every segment deserves purpose-built intelligence, not generic templates."

## Fundraising

**Series C** — Target: $40M — Status: **Active**

Key metrics for investors: 110% YoY ARR growth, 130% net dollar retention, 87 customers (40% multi-entity), $145K average ACV

## Organization

**Leadership:** Jordan Rivera (CEO), Marcus Webb (CTO), Sarah Chen (CRO), Devon Park (VP Ops), Priya Sharma (VP Product)

**Teams:** Engineering (18), Sales (11), Customer Success (6), Product (5)

**Board:** Sequoia (lead), a16z (observer), independent seat

## Voice

**Tone:** Direct, conviction-led, analytical. Short declarative sentences.
**Formatting:** Numbered lists (1/ 2/ 3/), bold key claims. No em-dashes, no bullets in LinkedIn posts.
**Banned phrases:** "flexible", "AI-first", "modern", "leveraging", "synergy"

## Flags

- ⚠️ **Metrics are 24 days stale** — update ARR, customer count, and burn rate
- ⚠️ **Enterprise tier is at-risk** — check with Sarah Chen on blockers
- ℹ️ **Fundraise is active** — Series C pipeline should be tracked in chief-fundraise

---

# Deliverable — Scenario 2: Update Metrics from Financial Model

**User prompt:** "update context with the most recent financial model" + three Google Sheets URLs

**Sources read (in parallel):**
```
gws sheets +read --spreadsheet <GROWTH_FORECAST_ID> --range "Dashboard!A1:CQ80"   → ok
gws sheets +read --spreadsheet <MRR_BY_CUSTOMER_ID> --range "customer MRR/ARR!A1:AQ200" → ok
gws sheets +read --spreadsheet <USAGE_METRICS_ID>   --range "Usage per Customer!A1:BB200" → ok
```

**Most recent actual month:** March 2026

## Proposed Changes to company.yaml

| Field | Was | Now | Source |
|-------|-----|-----|--------|
| `metrics.arr` | $12.5M | $13.8M | Growth Forecast — Ending ARR Mar 2026 |
| `metrics.customers` | 87 | 94 | MRR by Customer — Paying Customers Mar 2026 |
| `metrics.burn_rate` | $750K/mo | $620K/mo avg (Q1 2026) | Growth Forecast — Net Cash Burn |
| `metrics.gross_margin` | — | 79% | Growth Forecast — Gross Margin % Q1 2026 |
| `metrics.arr_per_employee` | — | $460K | Growth Forecast — ARR per Employee Mar 2026 |
| `metrics.nrr` | — | 108% | Growth Forecast — NRR Q1 2026 |
| `metrics.cash_on_hand` | — | $4.2M (Mar 2026) | Growth Forecast — Ending Cash |
| `metrics.usage_total` | — | 142,000 (Mar 2026) | Usage Metrics — Total row |
| `metrics.last_updated` | 2026-03-15 | 2026-04-14 | (today) |

**No changes to:** strategy, product, positioning, fundraising, org, voice

Write these updates? (yes / edit / skip)
