---
name: chief-board
description: Assemble board meeting materials, board memos, and board updates. Use this skill when the user mentions board meeting, board deck, board memo, board update, board materials, or is preparing for a board meeting. Also use when compiling cross-functional status updates that span metrics, engineering, sales, support, and hiring. This skill pulls live data from HubSpot (pipeline), GitHub/Jira (engineering), Pylon (support), Notion (initiatives), and Google Calendar (timeline) to build comprehensive board-ready documents.
user-invocable: false
---

# Board Materials Builder

You assemble board meeting materials by pulling live data from across the company's tools.

## Before Starting

1. Read `chief-context/company.yaml` for current metrics, goals, and initiatives
2. Read `chief-context/org.yaml` for DRIs and team structure
3. Determine what the user needs: full board package, single memo, or specific section

## Data Sources

Pull from these tools when available:

| Source | MCP | What to Pull |
|--------|-----|-------------|
| **HubSpot** | `mcp__hubspot__*` | Pipeline value, deal flow, win/loss rates, new customers, churn |
| **Jira** | Notion AI (`query_type="internal"`) | Sprint completion rates, initiative progress by epic, blockers |
| **Pylon** | `mcp__pylon__*` | Support ticket volume, resolution times, trending issues, CES |
| **Notion** | `mcp__notion__*` | Initiative status pages, hiring pipeline, key decisions log |
| **GitHub** | ToolSearch (`+github`) | Commits, PRs merged, releases shipped (secondary to Jira) |
| **Google Calendar** | ToolSearch | Board meeting date, upcoming milestones, key deadlines |

## Board Memo Structure

Use `/chief-memo` for formatting conventions. The board memo follows this structure:

1. **Executive Summary** — 1 paragraph: what happened, what's changing, what we need
2. **Key Metrics Dashboard** — Table with: Metric, Current, Prior Period, Target, Trend (↑↓→)
3. **Initiative Updates** — For each active initiative from company.yaml:
   - Status: On Track / At Risk / Blocked
   - Progress summary (3-4 sentences)
   - Key milestones hit / missed
   - Next milestones and dates
4. **Pipeline & Revenue** — From HubSpot: new pipeline, deals closed, churn, expansion
5. **Product & Engineering** — From Jira (via Notion AI): what shipped, velocity trends, blockers. For a full breakdown by project and engineer, compose with `/chief-roadmap`.
6. **Customer Health** — From Pylon: support trends, escalations, at-risk accounts
7. **Team** — Hiring status, org changes, notable wins
8. **Risks & Decisions** — Issues requiring board awareness or input
9. **Asks** — Specific things we need from the board (introductions, approvals, guidance)

## Rules

- Lead every section with the conclusion, then the supporting data
- Flag risks honestly — boards respect candor more than optimism
- If a data source is unavailable, state what's missing and proceed with what's available
- Include specific customer names, deal sizes, and dates — boards want specificity
- Keep the full memo under 4 pages. Supporting data can go in appendices.
- Use `/chief-memo` to write the actual output
