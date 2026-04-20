# Test Analysis: chief-investor

## Test Scenario
User says "prep me for my meeting with Greenfield Ventures tomorrow. I'm meeting with Rachel Torres, Partner."

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | All 8 required sections present | **PASS** — Meeting Details, Executive Summary, Firm Profile, Investment History, Attendee Profiles, Pitch Customization, Questions to Ask, Post-Meeting Playbook |
| 2 | Sports/athletics rapport flags included | **PASS** — Division I track and field at Stanford flagged with emoji |
| 3 | Specific dollar amounts, dates, names | **PASS** — $35M Series C, $500M Fund III, 2024 vintage, named portfolio companies |
| 4 | Investment history includes relevance column | **PASS** — Each investment has specific relevance note explaining why it matters for the pitch |
| 5 | Pitch customization maps firm thesis to company narratives | **PASS** — Maps Rachel's "platforms not apps" thesis to Agent SDK narrative, with specific emphasize/de-emphasize guidance |
| 6 | Actionable — CEO can skim and walk in prepared | **PASS** — Executive summary provides the key angle in 3 sentences. Pitch approach is concrete. |
| 7 | Questions are tailored to firm and attendees | **PASS** — 6 questions reference specific investments, blog posts, and portfolio dynamics |
| 8 | Post-meeting playbook with timing | **PASS** — 24-hour and 1-week actions with specific materials and connections |
| 9 | Simulated data clearly marked | **PASS** — [SIMULATED] tags throughout |
| 10 | Saved as markdown | **PASS** |

## Overall Grade: A

The brief is comprehensive, actionable, and specific. The pitch customization section is particularly strong — it doesn't just list the firm's thesis, it maps it to specific Meridian Ledger narratives with concrete guidance on what to emphasize and what to skip. The rapport flags section found a sports connection (track) and a mutual connection (Jamie Smith). The questions are genuinely tailored to Rachel's investment history, not generic.

## Issues Found

- **Limitation noted:** Without real web search, HubSpot, Clay, or Calendar MCP, all data is simulated. In production, the skill would pull real data from these sources. The [SIMULATED] tagging is appropriate.
- **Minor:** Could include a "Risks/Red Flags" section — things that might make this firm a bad fit (e.g., if they have a portfolio conflict).
- **Enhancement:** The template includes a "duration" field for the meeting that wasn't populated.
