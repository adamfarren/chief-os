# Skill Test Results

Last updated: 2026-06-23

Each skill was tested with a generic scenario using fictional company data ("Horizon Health"). Each test directory contains:
- **deliverable.md** — The output the skill produced
- **analysis.md** — Performance assessment against the skill's success criteria

## Test Context

All tests use the same fictional company context in `test-context/`:
- **Horizon Health** — AI-powered practice management platform, Series B ($12.5M ARR, 87 customers)
- 5 leadership team members, 4 functional teams
- Active Series C fundraise ($40M target)
- 3 strategic initiatives (Agent SDK, Enterprise tier, SOC 2)

## Results Summary

| Skill | Test Scenario | Grade |
|-------|--------------|-------|
| chief-1-1 | 1-1 prep: gate block when Pylon DOWN (Support employee); full brief when connected | A |
| chief-context | (1) View context, flag staleness; (2) update metrics from three Google Sheets (Growth Forecast, MRR, Usage) | A |
| chief-memo | Strategy memo on enterprise expansion | A |
| chief-investor | Investor brief for Greenfield Ventures meeting | A |
| chief-deal | Venture debt comparison (Summit vs. Westbridge) | A |
| chief-board | Q1 2026 board materials | A |
| chief-performance | Claude Code adoption analysis (10 engineers, 6 weeks) | A |
| chief-linkedin | LinkedIn post about Agent SDK launch | A |
| chief-escalation | Weekly escalation digest | A |
| customer-360 | Full 360-degree customer view (Cascade Wellness, last 90 days) | A |
| chief-event | Creative brief for developer conference (150 attendees) | A |
| chief-fundraise | Series C fundraise pipeline status | A |
| chief-competitive | Battle card for MedCore Systems | A |
| chief-partnerships | Partnership PRD for ChronoAudit (documentation auditing) + Notion publish | A |
| chief-initiative | Business case for a new managed services LOB | A |
| chief-roadmap | Q2 2026 roadmap progress (5 projects, 8 engineers, Jira + Slack) | A |
| chief-style | Brand color tokens, Figma fallback, component patterns | — |
| chief-org | Org tree query, extended team lookup, new hire update + Notion sync proposal | A |
| chief (router) | 5 routing scenarios (single, multi-skill, setup, ambiguous) | A |
| prof | 8 routing scenarios (single-skill, direct answer, no-args, multi-skill, ambiguous, disambiguation) | A |
| whiteboard | Flowchart with brand colors (patient enrollment), sequence diagram (API auth) | A |
| claude-usage | Weekly usage ingestion: Slack canvas → Sheets tab + tiered adoption analysis (12 engineers, 6 weeks, Horizon Health) | A |
| company-update | Weekly company-wide update (Horizon Health, 4/13–4/17/2026): Notion SQL meeting query, Pylon fallback for empty Support tables, plugin scorecard, status-indicator prefixed customer narratives, LinkedIn roundup, OOO coverage flags | A |
| funnel | 45-day lead funnel comparison: lead volume, qualified conversion (activity + cohort views), qualified→deal rate, source breakdown | A |

## Common Strengths

- All skills correctly read from and reference `chief-context` data
- Voice rules (direct tone, no banned phrases, no horizontal rules) followed consistently
- Deliverables are specific (names, numbers, dates) rather than vague
- Cross-skill composition patterns work as documented

## Common Enhancement Opportunities

- Skills that depend on MCP data (HubSpot, Slack, Pylon, etc.) produce simulated data in test — real-world quality depends on MCP connection quality
- Some skills could benefit from explicit cross-skill suggestions (e.g., chief-context suggesting `/chief-fundraise` when a raise is active)
- Templates could include more guidance on the "analysis memo" type, which is the least structured

## How to Run These Tests

These tests were executed by following each skill's SKILL.md instructions against the test context data. To re-run:

1. Read the relevant SKILL.md
2. Read the test context files in `test-context/`
3. Execute the test scenario described in the analysis file
4. Compare output against the success criteria
