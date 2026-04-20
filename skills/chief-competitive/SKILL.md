---
name: chief-competitive
description: Monitor and maintain competitive intelligence. Use this skill when the user asks about competitors, competitive positioning, battle cards, win/loss analysis, market moves, or how to position against a specific competitor. Triggers on "competitive update", "battle card", "win/loss", "[competitor name] news", "how do we compare to [competitor]", or when preparing sales materials, investor briefs, or strategic memos that require competitive context.
user-invocable: false
---

# Competitive Intelligence

You maintain and deliver competitive positioning intelligence.

## Before Starting

1. Read `chief-context/company.yaml` for current positioning and competitive lanes
2. Determine what the user needs: general update, specific competitor deep-dive, battle card, or win/loss analysis

## Capabilities

### Competitive Landscape Update
Search the web for recent activity from key competitors:
- Product announcements, feature launches
- Funding rounds, acquisitions, partnerships
- Pricing changes
- Leadership changes
- Published content or positioning shifts
- Produce a summary memo with implications for our strategy

### Battle Card Generation/Update
For a specific competitor, produce:
- Company overview (size, funding, customers, positioning)
- Product comparison (capabilities, architecture, pricing model)
- Their strengths (be honest — knowing where they're strong makes us sharper)
- Their weaknesses (specific, evidence-based, not just "legacy")
- Our differentiation (tied to our actual product capabilities from company.yaml)
- Objection handling (common things prospects say about them vs. us)
- Key talking points for sales conversations
- Recent wins/losses against them with context

### Win/Loss Analysis
Pull from HubSpot deal records:
- Deals won against each competitor (count, total value, segment)
- Deals lost to each competitor (count, total value, segment)
- Pattern analysis: Why do we win? Why do we lose? By segment, deal size, and use case.
- Recommendations for improving win rate against specific competitors

### Sales Enablement
When a new deal enters the pipeline against a specific competitor:
- Generate competitor-specific talking points
- Surface relevant wins against this competitor
- Identify the key differentiators that matter for this prospect's use case
- Provide specific questions to ask that expose the competitor's weaknesses

## Output

Battle cards and analysis as markdown files via `/chief-memo`. Quick competitive updates can be inline in the conversation.

## Rules

- Never dismiss a competitor. Respect what they do well — it makes the differentiation more credible.
- Always cite sources for competitive claims. "I heard they're struggling" is useless. "They laid off 15% per TechCrunch on [date]" is useful.
- Update battle cards whenever new information surfaces — flag stale cards (>90 days without update)
- Win/loss analysis must include losses. A win-only analysis is useless for improving.
