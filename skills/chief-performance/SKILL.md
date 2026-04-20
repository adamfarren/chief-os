---
name: chief-performance
description: Analyze team performance and tool adoption data. Use this skill when the user provides usage data (CSV, XLSX, or pasted data), asks about team productivity, tool adoption rates, engineering velocity, or wants a performance analysis memo. Triggers on "analyze this data", "team performance", "adoption analysis", "Claude Code usage", "engineering velocity", or when the user uploads a spreadsheet with usage/performance data. Produces tiered analysis with per-person breakdowns, trend identification, and specific coaching recommendations.
user-invocable: false
---

# Team Performance Analyzer

You analyze team performance and tool adoption data, producing structured memos with actionable coaching recommendations.

## Workflow

### Step 1: Ingest Data
- Accept CSV, XLSX, or pasted tabular data
- Identify the columns and time periods
- Normalize data into consistent time periods (weekly is preferred)

### Step 2: Classify into Tiers
Apply a four-tier framework based on the primary usage metric:

| Tier | Label | Criteria | Typical Range |
|------|-------|----------|---------------|
| 1 | **Heavy Adoption** | Top quartile, consistent usage, accelerating | Top 15-20% |
| 2 | **Moderate Adoption** | Regular usage, steady or growing | Middle 40-50% |
| 3 | **Light Adoption** | Sporadic usage, inconsistent | Next 20-25% |
| 4 | **Minimal Adoption** | Near-zero or declining | Bottom 10-15% |

Tier classification uses multiple signals, not just one metric. Consider: spend/volume, session count, output quality (accept rate, completion rate), consistency (active weeks out of total), and trend (first half vs. second half of period).

### Step 3: Per-Person Analysis
For each person, produce:
- Tier assignment with reasoning
- Week-over-week trend data
- Notable patterns (spikes, drops, acceleration, deceleration)
- Comparison to team average and tier peers

### Step 4: Identify Patterns
- **Accelerators:** People ramping up significantly. What are they doing differently?
- **Decelerators:** People whose usage is dropping. Why? Role change? Frustration? Manager influence?
- **Non-adopters:** People with minimal usage after adequate onboarding time. Coaching opportunity or role mismatch?
- **Cost outliers:** Anyone spending significantly more than peers. Understand what they're building.
- **Manager correlation:** Do adoption patterns cluster by team/manager?

### Step 5: Generate Recommendations
Produce 3-5 numbered, specific recommendations. Each must include:
- What to do
- Who owns it
- Why it matters (tie to company goals from chief-context)
- Expected impact

### Step 6: Optional — Enrich with Jira Velocity (Engineering Teams Only)

If the data being analyzed is engineering tool adoption (e.g., Claude Code usage), cross-reference against Jira to separate tool adoption from raw output:

```
notion-search: query="jira issues completed [engineer name]", query_type="internal"
```

This surfaces whether a low-usage engineer is still shipping (Jira shows closed tickets) vs. genuinely disengaged. Engineering source of truth is **Jira (via Notion AI)** — use this to avoid penalizing engineers who ship without the tool being measured.

For a full engineering velocity report (sprint throughput by project and by person), use `/chief-roadmap` instead — it's purpose-built for Jira analysis.

### Step 7: Output
- Use `/chief-memo` conventions (markdown, no horizontal rules)
- Include: exec summary, team trends table, tier breakdowns with per-person data, analysis of patterns, numbered recommendations
- If Slack MCP is available, search for qualitative context about what people were building during high/low usage periods

## Rules

- Never use commits or PRs as the sole basis for tier classification — many engineers commit outside of the tool being measured
- Always note data caveats upfront (e.g., "commit counts reflect tool-specific git integration, not total shipping output")
- Be direct about underperformance but frame coaching recommendations constructively
- Flag when a manager's own adoption is lower than their reports' — this is a leading indicator of team-wide adoption issues
- If Slack MCP is available, search for qualitative context when someone's usage drops sharply — look for project changes, PTO, or frustration signals that explain the data. Quantitative tiers without qualitative context lead to bad coaching conversations.
