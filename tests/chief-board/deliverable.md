# Board Update: Q1 2026

**2026-04-08 | Meridian Ledger**

## Executive Summary

Q1 was a strong execution quarter. ARR grew from $10.8M to $12.5M (+16% QoQ). We added 14 new customers and expanded 8 existing accounts. The Agent SDK is on track for a June beta. The enterprise tier is behind schedule — we underestimated the complexity of multi-entity admin — and we've restructured the team to recover. Series C fundraising is active with 4 first meetings completed and 2 in diligence. We need board help with two enterprise reference introductions and guidance on the Series C timeline.

## Key Metrics

| Metric | Q1 2026 | Q4 2025 | Target | Trend |
|--------|---------|---------|--------|-------|
| ARR | $12.5M | $10.8M | $12.0M | ↑ Beat |
| Customers | 87 | 73 | 80 | ↑ Beat |
| Net Dollar Retention | 130% | 125% | 120% | ↑ |
| ACV (New) | $145K | $132K | $140K | ↑ |
| Burn Rate | $750K/mo | $720K/mo | $700K/mo | ↑ Over |
| Runway | 14 months | 17 months | 18 months | ↓ Watch |
| Gross Margin | 78% | 76% | 75% | ↑ |

[SIMULATED — metrics derived from test context]

## Initiative Updates

### Agent SDK — ✅ On Track
**DRI:** Marcus Webb

The SDK architecture is complete and 3 internal agents are running in production. External developer documentation is 80% done. Two design partners (an e-commerce retailer and a SaaS company) are testing pre-release builds. Beta launch remains on track for June 2026.

**Milestones hit:** API finalized, authentication system shipped, first external design partner onboarded.
**Next:** Public beta (June 2026), 10 external developers building agents by July.

### Enterprise Tier — ⚠️ At Risk
**DRI:** Sarah Chen

Multi-entity admin is 4 weeks behind the original timeline. The permissions model for cross-entity access was more complex than scoped. We've moved 2 engineers from the platform team to accelerate. The revised ship date is end of June (was end of May).

**Impact:** 6 enterprise deals ($2.1M combined pipeline) are waiting on this feature. Sarah Chen is managing expectations with prospects and has not lost any deals yet.

**Milestones missed:** Admin console MVP (was March 31, now May 15).
**Next:** MVP to design partner by May 15, GA by June 30.

### SOC 2 Type II — ✅ On Track
**DRI:** Devon Park

Audit period began in February. All 47 controls are documented. The auditor (Vanta-facilitated) has completed the first evidence review with no findings. On track for certification by August 2026.

**Next:** Second evidence collection (May), final audit report (August).

## Pipeline & Revenue

[SIMULATED]

**New pipeline created in Q1:** $4.2M across 22 opportunities.
**Deals closed:** 14 new logos ($1.9M new ARR), 8 expansions ($650K expansion ARR).
**Key wins:** Coastal Commerce (12 entities, $280K ACV), Summit Manufacturing (8 entities, $210K ACV).
**Churn:** 2 customers ($85K ARR) — both single-entity businesses that outgrew their need. Not competitive losses.
**Q2 pipeline:** $3.8M weighted, including 3 enterprise deals above $200K.

## Product & Engineering

[SIMULATED]

**Shipped in Q1:** 2 major releases (v3.4, v3.5). Key features: AI-powered transaction categorization, redesigned reconciliation module, Agent SDK developer preview.
**Velocity:** 142 PRs merged (up from 118 in Q4). Sprint completion rate: 87%.
**Technical debt:** Migrated the inference pipeline from OpenAI to Claude API, reducing latency by 40% and cost by 25%.
**Open blockers:** None P0. Two P1 issues in the reconciliation module being addressed in v3.6 (April).

## Customer Health

[SIMULATED]

**CES:** 4.3/5.0 (up from 4.1 in Q4).
**Support volume:** 342 tickets (down 8% from Q4 despite 19% customer growth). Resolution time: 4.2 hours average.
**At-risk accounts:** 1 — Pacific Software ($180K ACV, renewal August 2026). Elevated ticket volume around bank feed integrations. Amy Torres assigned as dedicated CSM. Action plan in place.
**Positive signal:** Coastal Commerce (new Q1 win) submitted 0 support tickets in their first 45 days. Best onboarding experience we've had.

## Team

**Headcount:** 44 (was 38). Hired 6 in Q1: 3 engineers, 2 AEs, 1 CSM.
**Open roles:** 4 (2 senior engineers for Agent SDK, 1 SE, 1 PM for manufacturing vertical).
**Org changes:** Promoted Amy Torres to CS Lead. Added Priya Sharma as VP Product (started February).
**Notable:** Marcus Webb's engineering team delivered the Claude API migration 2 weeks ahead of schedule.

## Risks & Decisions

1. **Enterprise tier delay.** 4 weeks behind. If it slips further, we risk losing $2.1M in pipeline to competitors who can serve multi-entity groups today. We've added resources but this is the biggest execution risk this quarter.

2. **Runway compression.** 14 months at current burn. If the Series C takes 6+ months, we enter a window where runway drops below 10 months before close. Devon Park is modeling a contingency budget that extends runway to 18 months without headcount cuts.

3. **Manufacturing expansion timing.** The annual goal includes manufacturing and professional services expansion. We haven't started either. Recommend deferring professional services to 2027 and focusing solely on manufacturing in H2 2026. Decision needed.

## Asks

1. **Enterprise reference introductions.** Sequoia — can you connect us with [specific multi-entity finance organizations in your portfolio]? We need 2-3 enterprise design partners for the admin console beta.

2. **Series C timing guidance.** We're active in market. Current plan is to close by Q3. Given the enterprise tier delay and the runway math, should we accelerate the timeline or wait until enterprise GA ships for a stronger story?

3. **Manufacturing advisor.** Jamie — can you recommend a manufacturing CFO to advise on segment-specific accounting workflows? We need domain expertise before building.
