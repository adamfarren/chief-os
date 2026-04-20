# Test Analysis: chief-1-1

## Test Scenario
User says "what should I talk to Jordan about today?" — Jordan Chen is a Support team member at Meridian Ledger.

Two sub-tests:
- **Test A (gate pass):** Pylon is connected → full brief produced
- **Test B (gate block):** Pylon is unavailable → skill blocks before pulling any data

## Success Criteria

| # | Criterion | Test A | Test B |
|---|-----------|--------|--------|
| 1 | Resolves employee from roster (name, role, pillar, function, start date) | **PASS** | **PASS** |
| 2 | Identifies Pylon as the critical MCP for Support | **PASS** | **PASS** |
| 3 | **Gate block:** stops immediately if Pylon is DOWN, outputs ⚠️ message with MCP name, function, and re-auth instruction | n/a | **PASS** |
| 4 | **Gate block:** asks "Proceed anyway? (yes/no)" before continuing | n/a | **PASS** |
| 5 | Calendar event found and meeting time anchored in header | **PASS** | n/a |
| 6 | Pylon ticket data appears in Impact This Week (volume, open states, priority breakdown) | **PASS** | n/a |
| 7 | "Waiting on you" tickets surfaced as blockers requiring action | **PASS** | n/a |
| 8 | Talking points prioritized by what requires the CEO's decision or attention | **PASS** | n/a |
| 9 | Non-critical MCPs (Figma, HubSpot) noted in Sources but never block | **PASS** | n/a |
| 10 | Sources line cites Pylon ticket count | **PASS** | n/a |
| 11 | Output fits on one screen | **PASS** | n/a |

## Overall Grade: A

**Test A** produces a complete, data-grounded brief. The Pylon ticket volume section is the most valuable addition — surfacing "waiting on you" tickets that need the employee's action is exactly the kind of operational grounding a 1-1 needs. The gate correctly identifies Pylon as blocking for Support before pulling any data.

**Test B** demonstrates the correct blocking behavior. The skill resolves the employee, identifies their function, checks Pylon, and stops with a clear message — it does not produce a partial brief that silently omits the most important data.

## Issues Found

- **Simulated data noted:** Without live MCP connections (Pylon, Grain, Slack, Notion), all ticket and message data is simulated. In production, this is pulled from live sources.
- **Enhancement:** The gate block message could include a direct link to re-auth rather than a generic instruction, if the MCP server provides one.
- **Enhancement:** When the user proceeds anyway (gate bypassed), the ⚠️ Missing Data block should estimate what percentage of the employee's work is unobservable — e.g., "Support ticket volume and resolution rate (est. 70% of observable work) are unavailable."
