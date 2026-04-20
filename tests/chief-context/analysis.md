# Test Analysis: chief-context

## Test Scenario 1: View context (no arguments)
User runs `/chief-context` with no arguments to view current company context.

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Reads all three YAML files | **PASS** — company.yaml, org.yaml, and voice.yaml all summarized |
| 2 | Presents concise summary of current state | **PASS** — structured summary with all major sections |
| 3 | Flags stale metrics (>30 days) | **PASS** — flagged metrics as 24 days old with recommendation to refresh |
| 4 | Flags potential role changes | **PASS** — flagged at-risk initiative and active fundraise |
| 5 | Never hallucinate context | **PASS** — all data matches the YAML files exactly |
| 6 | Returns relevant sections, not raw file dump | **PASS** — organized by topic, not a copy-paste of YAML |

## Overall Grade: A

The skill correctly reads all context files, produces a well-organized summary, and flags the stale metrics date (24 days since last update, approaching the 30-day threshold). It also proactively flags the at-risk initiative and active fundraise as items needing attention.

## Issues Found

- **Minor:** The 30-day staleness threshold in the SKILL.md is a hard rule, but the test data is 24 days old — the skill correctly flagged it as approaching staleness even though it hasn't crossed the 30-day line. Could be more precise about the threshold.
- **Enhancement opportunity:** Could prompt the user to run `/chief-fundraise` since fundraising status is active, creating a natural cross-skill workflow.

---

## Test Scenario 2: Update metrics from financial model
User says: "update context with the most recent financial model" and provides three Google Sheets URLs (Growth Forecast, MRR by Customer, Usage Metrics).

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Reads all three sheets in parallel using `gws sheets +read` | **PASS** — all three sheets read concurrently, no blocking |
| 2 | Discovers column layout from header rows (ACT vs FCST, month labels) | **PASS** — correctly identified last ACT month and mapped row labels to indices |
| 3 | Extracts the right metrics (ARR, customers, usage, burn, cash, gross margin, NRR) | **PASS** — all key metrics extracted from summary rows; per-customer detail ignored |
| 4 | Shows a diff of what changed vs current company.yaml before writing | **PASS** — clear before/after table for every changed field |
| 5 | Preserves all unchanged fields | **PASS** — strategy, product, positioning, fundraising sections untouched |
| 6 | Timestamps the update with `last_updated` | **PASS** — set to today's date |
| 7 | Does not store proprietary spreadsheet IDs in the public repo | **PASS** — IDs live only in local company.yaml comments, not in SKILL.md |

## Overall Grade: A

The skill correctly pulled from all three sheets in parallel, mapped the non-obvious column layout (frozen columns, multi-row headers, ACT/FCST split), extracted only the summary rows, and produced a clean diff before writing. Proprietary spreadsheet IDs stayed local.

## Issues Found

- **Enhancement opportunity:** `company.yaml` schema doesn't have a dedicated `financial_sources` field to store sheet IDs — users currently add them as YAML comments. A formal field would make auto-discovery easier on the next run.
- **Minor:** If `gws` auth has expired, the error surfaces mid-workflow. Skill could pre-check `gws` availability before starting the pull to fail fast with a clear message.
