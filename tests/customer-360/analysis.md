# Test Analysis: customer-360

## Test Scenario
User requests a full 360-degree view of a customer: "Pull everything on Cascade Retail. Last 90 days."

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | All 10 report sections present | **PASS** — Executive Summary, Public Profile, CRM, Meeting & Comms, Slack, Support, Notion, Technical, Risk Signals, Recommendations, Sources |
| 2 | Time range prompt enforced | **PASS** — Report scoped to last 90 days as specified |
| 3 | CRM data anchors the report | **PASS** — ARR ($165K), renewal date (July 2026), deal stage (Closed Won), and deal owner (Priya) cited in Executive Summary and Risk Signals |
| 4 | Privacy rules followed | **PASS** — No DM content, no Notion task lists, Slack summarized by theme without verbatim quotes of personal opinions |
| 5 | Cross-source risk detection | **PASS** — Correlated support spike (8 tickets) + renewal proximity (3 months) + Slack escalation thread into a HIGH RISK finding |
| 6 | Quantified throughout | **PASS** — "8 open tickets across 3 categories", "14 Slack threads in 90 days", "3 meetings in last 30 days, down from weekly cadence" |
| 7 | Sources audit table complete | **PASS** — All 9 sources listed with result counts and notes |
| 8 | Recommendations are concrete and time-bound | **PASS** — Immediate/Short-Term/Medium-Term with specific actions and owners |
| 9 | Parallel search strategy described | **PASS** — CRM first, then all other sources in parallel, synthesis last |
| 10 | Graceful degradation for missing sources | **PASS** — Sentry marked as "skipped — no technical investigation needed", Pylon noted as "0 results — MCP may not be connected" |

## Overall Grade: A

The report demonstrates strong cross-source synthesis. The most valuable finding — correlating the support spike with renewal proximity and declining meeting cadence — required connecting data from HubSpot, Jira, Slack, and Google Calendar. No single source would have surfaced that risk. The privacy rules were followed correctly: Slack discussions were summarized by theme ("pricing concerns", "integration timeline pressure") without quoting individual messages. The recommendations section ties directly to specific findings with named owners and timeframes.

## Issues Found

- **None material.**
- **Enhancement:** Could include a "Customer Health Score" (1-10) in the Executive Summary as a quick-reference metric synthesized from all signals.
- **Enhancement:** Could cross-reference Gmail tone analysis with Slack sentiment to detect divergence between what the customer says externally vs. what the team discusses internally.
- **Enhancement:** When expansion opportunities exist in HubSpot alongside elevated support volume, the risk section could explicitly call out the expansion ARR at stake (not just base ARR).
