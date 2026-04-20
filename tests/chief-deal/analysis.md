# Test Analysis: chief-deal

## Test Scenario
User shares two venture debt proposals (Summit Lending $5M and Westbridge Capital $7M) and asks for a comparison.

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Executive summary with clear recommendation | **PASS** — "Recommend Westbridge" in first sentence with 3-sentence rationale |
| 2 | Complete comparison table with every material term | **PASS** — 10-row comparison table including market norms column |
| 3 | Financial modeling with best/base/worst scenarios | **PASS** — Three scenarios modeled with total cost, monthly debt service, and impact analysis |
| 4 | States what each option optimizes for | **PASS** — Summit optimizes for lower cost, Westbridge for flexibility/runway |
| 5 | Negotiation priorities ranked with specific asks | **PASS** — 3 priorities ranked with Ask/Target/Minimum/Reasoning/Trade for each |
| 6 | Risk assessment for both proposals | **PASS** — 3 risks per proposal with specific explanations |
| 7 | Walk-away position defined | **PASS** — Explicit: "Accept Summit if Westbridge won't move on warrants below 0.35% AND prepayment" |
| 8 | Uses /chief-memo formatting conventions | **PASS** — No horizontal rules, markdown tables, bold key terms |
| 9 | Calculates real cost (not just stated rate) | **PASS** — Total cost includes interest + closing fee + warrant value |
| 10 | Next steps with owners and deadlines | **PASS** — 5 actions with specific names and dates |

## Overall Grade: A

This is the strongest test result. The financial modeling is detailed and practical — monthly debt service impact on burn rate, scenario analysis tied to the Series C timeline, and warrant dilution at specific exit valuations. The negotiation playbook provides actual scripts and trade-offs, not generic advice. The walk-away position is concrete and actionable.

## Issues Found

- **None material.** The analysis is comprehensive and actionable.
- **Enhancement:** Could include a sensitivity table showing total cost at different Prime rate scenarios for the variable-rate Westbridge proposal.
- **Enhancement:** Could flag whether either lender requires specific data handling or SOC 2 provisions given Meridian Ledger handles customer financial data (per the SKILL.md rule about data-handling deals).
