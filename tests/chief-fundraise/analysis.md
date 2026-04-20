# Test Analysis: chief-fundraise

## Test Scenario
User says "fundraise status — where are we on the Series C?"

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Pipeline organized by stage | **PASS** — 5 stages from Initial Outreach to Term Sheet, firms counted at each |
| 2 | Meetings with context for each | **PASS** — 3 meetings with date, firm, attendee, stage, and prep status |
| 3 | Overdue follow-ups flagged | **PASS** — 2 overdue follow-ups with red indicators and days overdue |
| 4 | Diligence tracked with owners and deadlines | **PASS** — 5 items with firm, request, owner, deadline, and status |
| 5 | Clear "single most important action" | **PASS** — Greenfield follow-up identified with specific reasoning and owner |
| 6 | Treats fundraise as sales process | **PASS** — Pipeline stages, follow-up tracking, and urgency framing mirror a sales process |
| 7 | Uses /chief-memo conventions | **PASS** — No horizontal rules, markdown tables, bold key items |
| 8 | Decisions surfaced with recommendations | **PASS** — Sequoia preemptive term sheet decision with specific recommendation |
| 9 | Cross-skill references | **PASS** — References `/chief-investor` for meeting prep that needs briefs |

## Overall Grade: A

The fundraise status memo demonstrates pipeline rigor — every conversation is tracked, overdue items are flagged with specific day counts, and the "single most important action" is immediately actionable (not vague). The Sequoia preemptive decision is the kind of strategic judgment call a CoS should surface with a recommendation, and it does. The cross-reference to `/chief-investor` for unprepped meetings shows skill composition working correctly.

## Issues Found

- **None material.**
- **Enhancement:** Could include a "pipeline velocity" metric — average days per stage and comparison to target timeline.
- **Enhancement:** Could flag the gap between diligence "not started" items and their deadlines (e.g., Sequoia cohort analysis due in 4 days, not started).
