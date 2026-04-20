# Test Analysis: chief-roadmap

## Test Scenario
CEO of Meridian Ledger runs `/chief-roadmap` with no arguments. Skill executes against test company context (Q2 2026, 5 engineering projects, 8 engineers). Notion connected source returns simulated Jira data; Slack returns engineering channel messages.

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Loads company context (OKRs, initiatives) from chief-context | **PASS** — All 3 Q2 initiatives (Agent SDK, Enterprise tier, SOC 2) are present; manufacturing vertical correctly inferred from segment expansion goal |
| 2 | Finds roadmap document in Notion before querying Jira | **PASS** — Roadmap page located ("Meridian Ledger — Q2 2026 Engineering Roadmap"), fetched before Jira queries |
| 3 | Quarterly → Monthly → Last 2 weeks framing applied to every project | **PASS** — Every project section has all three time horizons present and specific |
| 4 | Status signal (🟢/🟡/🔴) correctly assigned with justification | **PASS** — Agent SDK (🟢 ahead), SOC 2 (🟢), Infrastructure (🟢), Enterprise (🟡 overdue arch decision), Manufacturing (🟡 intake module risk). Reasoning given for each. |
| 5 | By-engineer section with closed/in-progress breakdown | **PASS** — 8 engineers covered with specific ticket-level attribution |
| 6 | Blockers & Risks section with actionable items | **PASS** — 4 blockers identified, each with DRI, specific action, and urgency |
| 7 | Data gaps explicitly flagged rather than extrapolated | **PASS** — Mia Rodriguez's Jira gap surfaced with "verify manually" rather than invented data |
| 8 | Velocity mapped to value, not just ticket count | **PASS** — ENT track called at-risk despite 4 tickets closed because the critical path ticket is blocked. James Liu's 7 closed correctly praised in context of SOC 2 completion rate. |
| 9 | Slack used for qualitative context only, not as primary source | **PASS** — Slack referenced for Marcus Webb's manufacturing escalation signal; Jira is the authoritative source throughout |
| 10 | Data coverage section lists sources with gaps noted | **PASS** — Sources listed (Notion roadmap, Jira project keys, Slack channels), data gap for one engineer called out |
| 11 | Output is CEO-readable (plain English, ticket titles not IDs) | **PASS** — All Jira IDs accompanied by plain-English titles; no raw JSON or Jira markup |
| 12 | Cross-engineer workload risk identified | **PASS** — Aisha Okafor's cross-track load flagged as a risk with a specific recommendation (clarify primary track) |

## Overall Grade: A

The skill produces a decision-ready engineering update with no manual synthesis required. The quarterly/monthly/2-week structure holds for every project and gives the CEO an instant read on pacing. The most valuable outputs are the operational findings that aren't obvious in ticket counts: the ENT-38 architecture review is blocked on the CTO himself, MFG-11 has no buffer and no second engineer, and one engineer has zero Jira activity. A CEO reviewing this output would know exactly what to unblock before the next sprint.

## Issues Found

- **Minor:** By-engineer section doesn't show Marcus Webb's architecture review time, which is significant. Skills like this should consider a "reviews completed" field for senior/staff engineers whose primary output is design and review rather than code commits.
- **Enhancement:** A summary table at the top (Project | Status | Last 2W Closed | Open | Critical Blocker) would make the by-project section scannable in 30 seconds for async sharing. The current format is thorough but requires reading through each project section.
- **Enhancement:** No PR-level data (open PRs, review backlog). If GitHub MCP is available, adding "PRs merged / PRs waiting review" per engineer would sharpen the throughput picture.
- **Data dependency:** Skill quality is directly proportional to Jira being connected to Notion AI search. If Jira is not a connected source, the output degrades to Slack-only qualitative signal. Skill correctly warns about this, but user setup matters.
