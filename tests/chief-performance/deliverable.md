# Claude Code Adoption Analysis: Engineering Team

**2026-04-08 | Period: Weeks 1-6**

## Executive Summary

**Overall adoption is healthy but polarized.** 7 of 10 engineers are actively using Claude Code with growing engagement. However, 2 engineers are declining sharply (James Liu and Mia Rodriguez) and require immediate coaching. The CTO (Marcus Webb) has lower adoption than 6 of his 8 direct reports — this is a leading indicator that should be addressed before it signals to the team that adoption is optional. Top recommendation: pair James and Mia with Elena Vasquez (highest adopter) for structured pairing sessions this week.

**Data caveat:** Spend and session counts reflect Claude Code usage only. They do not capture total engineering output — engineers may be productive through other tools or direct coding. Tier assignments should inform coaching conversations, not performance reviews.

## Team Overview

| Metric | Value | Trend |
|--------|-------|-------|
| Total Active Users (≥1 session/week) | 8 of 10 | → Stable |
| Avg Weekly Spend | $52.37 | ↑ Growing |
| Avg Weekly Sessions | 17.8 | ↑ Growing |
| Top Quartile Threshold | $88+/week | |
| Bottom Quartile Threshold | $15/week | |
| Team Accept Rate | 0.72 avg | |

## Tier Breakdown

### Tier 1: Heavy Adoption (3 people)

| Name | Avg Spend/Wk | Trend (W1→W6) | Sessions/Wk | Accept Rate | Notable |
|------|-------------|---------------|-------------|-------------|---------|
| David Chang | $105.43 | $92→$115 ↑ | 34.8 | 0.83 | **Highest output quality.** Consistent heavy usage with highest accept rate on the team. Model user. |
| Elena Vasquez | $101.22 | $85→$126 ↑ | 34.2 | 0.81 | **Fastest accelerator.** 47% spend increase over 6 weeks. Highest absolute spend in Week 6. |
| Ryan Kim | $81.52 | $68→$96 ↑ | 26.8 | 0.78 | **Steady climber.** Consistent week-over-week growth. No dips. Reliable adoption pattern. |

### Tier 2: Moderate Adoption (3 people)

| Name | Avg Spend/Wk | Trend (W1→W6) | Sessions/Wk | Accept Rate | Notable |
|------|-------------|---------------|-------------|-------------|---------|
| Tom Bennett | $63.70 | $56→$72 ↑ | 21.2 | 0.76 | Steady, moderate growth. Consistent usage without spikes or drops. |
| Aisha Okafor | $55.92 | $46→$71 ↑ | 18.8 | 0.72 | Growing steadily. Approaching Tier 1 threshold — likely to cross over in next 2-3 weeks. |
| Marcus Webb (CTO) | $59.18 | $43→$86 ↑ | 17.5 | 0.74 | **⚠️ Manager flag:** Ranked 5th of 10 in adoption despite being the CTO. Accelerating (doubled from W1→W6) but still behind 3 of his reports. |

### Tier 3: Light Adoption (2 people)

| Name | Avg Spend/Wk | Trend (W1→W6) | Sessions/Wk | Accept Rate | Notable |
|------|-------------|---------------|-------------|-------------|---------|
| Nina Patel | $32.17 | $15→$49 ↑ | 10.8 | 0.71 | **Fastest ramp (Jr Engineer).** Started lowest, tripled spend in 6 weeks. Expected trajectory for a junior engineer — on track to reach Tier 2 in 2-3 weeks. |
| Sofia Petrov | $17.72 | $6→$36 ↑ | 5.8 | 0.68 | **Late bloomer.** Near-zero in Weeks 1-2, then accelerated sharply. Something changed in Week 3 — worth understanding what unblocked her. |

### Tier 4: Minimal/Declining Adoption (2 people)

| Name | Avg Spend/Wk | Trend (W1→W6) | Sessions/Wk | Accept Rate | Notable |
|------|-------------|---------------|-------------|-------------|---------|
| James Liu | $5.58 | $12→$2 ↓↓ | 2.0 | 0.45 | **Sharp decline.** Started with some usage, dropped to near-zero. Lowest accept rate (0.45) suggests frustration with output quality. Needs intervention. |
| Mia Rodriguez | $20.03 | $35→$8 ↓↓ | 7.0 | 0.52 | **Active decline.** Was a moderate user in Week 1, usage has dropped 77% over 6 weeks. Something is actively pushing her away from the tool. |

## Patterns

**Accelerators (5 people):** Elena Vasquez, Ryan Kim, Aisha Okafor, Nina Patel, and Sofia Petrov all show consistent upward trends. Elena and Nina are the standouts — Elena for absolute volume, Nina for rate of improvement relative to starting point. Both are worth profiling as internal champions.

**Decelerators (2 people):** James Liu and Mia Rodriguez are actively declining. James's low accept rate (0.45) suggests the tool isn't producing useful output for his work — likely a workflow or prompt engineering issue, not a motivation issue. Mia's decline is steeper and started from a higher base — worth investigating whether a project change, frustration, or external factor is driving it.

**Manager signal:** Marcus Webb's adoption (Tier 2, rank 5/10) is lower than David Chang, Elena Vasquez, and Ryan Kim. While he's accelerating (doubled from W1→W6), the team sees what the CTO uses. If he's not a visible power user, adoption becomes "optional" in the team culture. This is the single highest-leverage coaching opportunity.

**Cost outlier:** David Chang's $115/week in Week 6 is the highest on the team. At this rate, he'd be ~$500/month. Worth understanding what he's building — this could be a best-practice workflow worth replicating, or it could indicate inefficient usage.

## Recommendations

1. **Pair James Liu and Mia Rodriguez with Elena Vasquez for structured pairing sessions.** Owner: Marcus Webb. James's low accept rate suggests a skill gap, not a motivation gap. Two 1-hour sessions this week where Elena demonstrates her workflow could unblock both. Expected impact: move both to Tier 3 within 3 weeks.

2. **Marcus Webb should publicly share his Claude Code usage in the next team standup.** Owner: Marcus Webb. Show specific examples of what he's building with it. The team needs to see the CTO as a power user, not just an advocate. Expected impact: normalizes heavy adoption as the team standard.

3. **Investigate Sofia Petrov's Week 3 inflection point.** Owner: Marcus Webb. Something changed — a project, a tip from a colleague, a workflow breakthrough. If we can identify it, we can replicate the trigger for James and Mia. Expected impact: create a replicable onboarding pattern.

4. **Profile David Chang's workflow as an internal case study.** Owner: Priya Sharma (Product). His 0.83 accept rate at $105/week means the tool is producing high-quality output for him. Document his prompts, use cases, and workflow. Share with the team. Expected impact: raise team-wide accept rates by giving people a playbook.

5. **Set a 4-week check-in to re-tier the team.** Owner: Marcus Webb. Re-run this analysis in 4 weeks to measure whether James and Mia have improved, whether Sofia and Nina have crossed into Tier 2, and whether Marcus's own usage has increased. Expected impact: accountability and trend tracking.
