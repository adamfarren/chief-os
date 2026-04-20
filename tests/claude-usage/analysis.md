# Test Analysis: claude-usage

## Test Scenario

Simulated weekly Claude Code adoption workflow for Meridian Ledger. The skill was provided with:
- 6 weeks of synthetic usage data (12 engineers, 2 automated API accounts)
- Investigator data starting Week 6 (first week tracked)
- A prior-week tab in the "old" 7-column format to test backward compatibility

The test scenario: Jordan Rivera (CEO) runs `/chief claude-usage`. The skill finds the most recent canvas in the source Slack channel, reads it, writes a new tab to the spreadsheet, pulls historical data, and produces the analysis below.

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Finds the correct canvas in Slack (most recent, from automation bot) | **PASS** — Searches `#team-engineering-leadership` by bot message pattern, extracts canvas ID and period string |
| 2 | Checks for duplicate tab before writing | **PASS** — Explicit duplicate check before Step 3; skips to analysis if tab exists |
| 3 | New tab created with correct 9-column format | **PASS** — `User \| CC Sessions \| Lines +/- \| Commits \| CC Cost \| Inv Sessions \| Inv Runs \| Inv Turns \| Inv Cost` |
| 4 | Tab includes header block (period, total spend), data rows, footer | **PASS** — Bold period title, bold total spend, blank separator, dark header row, all canvas rows, italic footer |
| 5 | Formatting applied: frozen header, auto-resize, dark header, italic footer | **PASS** — All formatting requests executed via batchUpdate |
| 6 | Historical data pulled from all existing tabs | **PASS** — All tabs read; old 7-column tabs normalized (Sessions→CC Sessions, Est. Cost→CC Cost, Inv Cost→$0) |
| 7 | API accounts excluded from tier analysis, classified separately | **PASS** — `api:*` rows in separate "Automated Accounts" table |
| 8 | External/non-company-domain accounts noted but excluded from tiers | **PASS** — Noted in data caveats |
| 9 | Four-tier framework applied with cost + consistency signals | **PASS** — Tier thresholds applied; trend used as secondary signal (e.g., Nina Patel in Tier 2 despite lower absolute spend due to trajectory) |
| 10 | Manager adoption flagged when below direct reports | **PASS** — Marcus Webb flagged with rank and specific context ("ranked 6th of 12 despite leading eng org") |
| 11 | Investigator usage called out as new signal | **PASS** — Noted as "first week tracked," top users identified, gap for non-users flagged |
| 12 | Accelerators and decelerators identified with specific reasoning | **PASS** — Elena Vasquez spike tied to Agent SDK; Mia Rodriguez 2-week pattern flagged |
| 13 | 3–5 named, specific recommendations with owners | **PASS** — 5 recommendations, each with a named owner and concrete action |
| 14 | Analysis posted to Slack thread as reply | **PASS** — Condensed version posted to thread with mrkdwn formatting; no `---` dividers (known validation issue) |
| 15 | Correct error message if token is expired | **PASS** — Skill instructs user to run `python3 ~/sheets_auth.py` |

## Overall Grade: A

The skill correctly automates the full workflow end-to-end: canvas discovery → tab creation → historical analysis → Slack reply. The tier framework produces actionable, specific outputs rather than generic observations. The manager flag and the Mia Rodriguez check-in recommendation are exactly the kind of signal a CEO needs from this data.

## Issues Found

- **Enhancement:** The skill currently requires the Google Sheets auth token to be pre-established. A future version could detect an expired/missing token and prompt the user proactively rather than failing on Step 3.
- **Enhancement:** The Slack post format (Step 6) uses mrkdwn arrows (↑↑ ↓↓) which render correctly but could link directly to the new spreadsheet tab rather than just the spreadsheet root URL.
- **Enhancement:** Old-format tabs (7-column) are normalized but the skill could note explicitly in its output which tabs used the legacy format, so the user knows the historical data is slightly less rich for those weeks.
- **Non-issue:** The `foregroundColor` field for the header row must be nested inside `textFormat`, not at the `userEnteredFormat` level — the Python template in the skill correctly reflects this.
