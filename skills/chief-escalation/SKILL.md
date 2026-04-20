---
name: chief-escalation
user-invocable: false
description: Synthesize customer escalation data from support tools into actionable intelligence. Use this skill when the user asks about customer escalations, support trends, customer health, at-risk accounts, ticket volume, or the support-to-build pipeline. Triggers on "escalation digest", "support summary", "customer health", "at-risk customers", "what's happening in support", or when preparing board materials or customer reviews. Pulls from Pylon (tickets), Slack (support channels), Notion (customer docs), Jira (engineering issues), and HubSpot (deal/renewal data).
---

# Customer Escalation Synthesizer

You monitor and synthesize customer support data into CEO-level intelligence. Pylon is the primary data source — its MCP tools are available directly.

## Pylon MCP Workflow

Pylon tools are available directly — no ToolSearch needed.

### Data Collection Steps

1. **Get all open issues across all accounts** — `mcp__pylon__search_issues` with:
   - `states`: `["new", "waiting_on_you", "waiting_on_customer", "on_hold"]`
   - `limit`: 100
   - Page through results using the returned `cursor` if needed
2. **Get recently closed issues** (for resolution wins and trend analysis) — `mcp__pylon__search_issues` with:
   - `states`: `["closed"]`
   - `created_after`: 7 days ago (RFC3339 format, e.g., `"2026-04-03T00:00:00Z"`)
3. **Get issue details for escalations** — For any issue that needs CEO-level context:
   - `mcp__pylon__get_issue` for full details (body, custom fields, account info)
   - `mcp__pylon__get_issue_messages` for the full conversation thread
4. **Search accounts for context** — `mcp__pylon__search_accounts` to:
   - Identify accounts with the highest issue volume
   - Get account owner, tags, and custom fields
   - Use `mcp__pylon__get_account` for full details on flagged accounts
5. **Cross-reference with HubSpot** — For each flagged account, search HubSpot for:
   - Deal size (ARR/ACV), renewal date, expansion opportunities
   - This is what turns a support ticket into a CEO-level escalation

### Filtering for CEO Attention

Use Pylon issue states to triage:
- `waiting_on_you` issues aging > 48 hours = response SLA risk
- Multiple `new` issues from one account in a week = systemic problem
- `on_hold` issues aging > 7 days = stale escalation
- High issue volume on an account with an upcoming HubSpot renewal = at-risk

### Week-over-Week Comparison

To calculate trends:
- Run `mcp__pylon__search_issues` with `created_after`/`created_before` for the current week
- Run again for the prior week
- Compare: total volume, volume by account, volume by tag/category, state distribution

## Capabilities

### Weekly Escalation Digest
Pull from Pylon (primary) and cross-reference with HubSpot, Slack, Jira. Produce:
- Top issues by severity, customer, and category
- New escalations since last digest
- Aging escalations (unresolved > 7 days)
- Resolution wins (what got fixed)
- Trend vs. prior week: volume up/down, category shifts, emerging patterns

### Ticket-to-Build Pipeline
Identify support patterns that should become product:
- Issues that appear across multiple customers
- High-volume ticket categories that a plugin or feature could eliminate
- Quantify: "X tickets/week across Y customers" for prioritization
- Flag opportunities where CS/support could build the solution directly rather than triaging repeatedly
- Cross-reference with Jira: search Notion (Jira connected source) for existing engineering tickets that match the pattern. Avoids recommending work that engineering already has in flight.

### Customer Health Scoring
Cross-reference support data with business data:
- High ticket volume + upcoming renewal = at-risk flag
- High ticket volume + new customer = onboarding issue flag
- Low ticket volume + high engagement = healthy
- Search HubSpot for renewal dates, deal size, expansion opportunity
- **Expansion-at-risk detection:** If an at-risk account is also flagged as an expansion opportunity in HubSpot, escalate with a different playbook — this needs a save-and-grow strategy, not just a retention play. Note the expansion ARR at stake alongside the base ARR.

### At-Risk Customer Alert
Flag customers where:
- Support volume spiked >50% week-over-week
- Severity 1 tickets are open > 48 hours
- Multiple open tickets across different categories (systemic issue)
- Renewal is within 90 days AND support volume is elevated
- Expansion opportunity in HubSpot AND support volume is elevated (flag as "expansion at risk")

## Output

Use `/chief-memo` conventions. Structure:
1. **Summary** — 3-4 sentences: overall support health, biggest concern, biggest win
2. **Key Metrics** — Open issues (by state), closed this week, WoW trend, top accounts by volume
3. **Escalations Requiring CEO Attention** — Only the ones that matter at this level. Include Pylon issue number, account, state, age, and the HubSpot deal size + renewal date.
4. **At-Risk Accounts** — Table: account name, open issues, "waiting_on_you" count, deal ARR, renewal date, risk factor
5. **Build Opportunities** — Support patterns that should become product (tag/category clusters across accounts)
6. **Resolved This Week** — Wins worth knowing about

## Jira Cross-Reference (Engineering Source of Truth)

When surfacing ticket-to-build opportunities or escalations with a technical root cause, cross-reference against Jira via Notion's connected source:

```
notion-search: query="jira [issue keyword or component]", query_type="internal"
```

Use this to:
- Check if an engineering ticket already exists for the reported problem (avoids creating duplicate work)
- Find the assigned engineer and estimated fix timing
- Determine if an open Jira issue is causing the spike (and escalate with the ticket number)
- For P1-equivalent escalations, note the Jira issue status in the "Escalations Requiring CEO Attention" section

Engineering data source: **Jira (via Notion AI)** — not a direct Jira MCP. Query through Notion with `query_type="internal"`.

## MCP Dependencies

| MCP Server | Role | Required? |
|-----------|------|-----------|
| **Pylon** | Primary source for all support tickets, account data, issue states | Required — skill cannot function without it |
| **HubSpot** | Deal size, ARR, renewal dates for at-risk context | Required — needed to turn tickets into CEO-level escalations |
| **Notion** | Jira integration (engineering issues), customer docs, handbook context | Required for ticket-to-build and technical cross-reference |
| **Slack** | Support channel discussions, internal escalation threads | Optional — fallback if Pylon is unavailable; enriches context |

## Rules

- Only escalate to the CEO what genuinely needs CEO attention. Filter aggressively.
- Always include the customer name, deal size (from HubSpot), and renewal date for context
- If Pylon MCP is unavailable, search Slack support channels as a fallback. But Pylon is the primary source — always try it first.
- Quantify everything — "several customers are frustrated" is useless. "4 customers filed 12 tickets about lab ordering in the last 7 days" is actionable.
