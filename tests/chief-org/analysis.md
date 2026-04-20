# Test Analysis: chief-org

## Test Scenarios

1. **Org tree query** — "Show me the org"
2. **Extended team query** — "Who coordinates the Apex Dev Studio relationship?"
3. **Roster update + Notion sync** — new hire ingestion, sync proposal

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Org tree renders as indented hierarchy with all pillars | **PASS** — 4 pillars (Engineering, Product, Revenue, Ops) shown with correct reporting lines |
| 2 | Extended teams appear below internal org, clearly labeled "not in headcount" | **PASS** — Separate section with explicit note; headcount total excludes them |
| 3 | Extended team lookup returns coordination contacts, not just agency members | **PASS** — Shows executive sponsor, day-to-day lead, and PM; no contract amounts |
| 4 | Extended team output excludes contract amounts and equity | **PASS** — No financial data in output |
| 5 | Roster update correctly modifies headcount totals | **PASS** — Engineering 18→19, Total 36→37 |
| 6 | Notion sync proposal is specific (section, field, old→new) | **PASS** — 3 targeted changes identified; waits for confirmation before writing |
| 7 | Notion sync proposal excludes sensitive data | **PASS** — No comp, equity, or contract data in proposed Notion changes |
| 8 | Comp data in roster.yaml does not appear in any output | **PASS** — No salary figures surfaced across all 3 tests |

## Overall Grade: A

The three scenarios cover the skill's main modes: query, extended-team lookup, and update+sync. The extended teams section correctly separates agency relationships from internal headcount and surfaces coordination contacts without leaking financial terms. The Notion sync proposal is appropriately targeted — it names specific sections and field values, waits for confirmation, and filters sensitive fields before proposing.

## Issues Found

- **None material.**
- **Enhancement:** When an extended team is mentioned in response to a `/chief-investor` or `/chief-board` query about team capacity, the skill should include a note clarifying that these are contractors, not FTEs, to avoid overstating headcount in investor-facing materials.
- **Enhancement:** The Notion sync could include a "last synced" timestamp check — if the Notion page was last updated more than 30 days ago and the roster has changed, flag it proactively rather than waiting for a manual update trigger.
