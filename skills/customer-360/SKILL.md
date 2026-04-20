---
name: customer-360
description: >-
  Build a comprehensive 360-degree view of a customer by searching all connected services —
  CRM (HubSpot), Slack conversations, Jira tickets, Notion docs, support data (Pylon),
  error tracking (Sentry), email (Gmail), calendar meetings, and the web.
  Use this skill whenever the user wants to understand the full picture of a customer relationship,
  investigate what led to an escalation, prep for an executive call, review account health,
  or asks things like "what's going on with [customer]?", "pull everything on [customer]",
  "customer deep dive", "customer 360", "interaction history", or "what do we know about [customer]?".
  This is the go-to skill for any request that involves looking across multiple sources to
  understand a customer's situation holistically.
---

# Customer 360: Full Interaction Analysis

Build a complete picture of a customer's relationship by searching every connected service and synthesizing findings into a single report. The primary use case is escalation investigation — understanding the full arc of interactions that led to the current situation — but it works equally well for call prep, account reviews, and QBRs.

## Input

The user provides:
- **Customer name** (required) — e.g., "Acme Retail", "thriving-center", "accomplish"
- **Time range** (ask every time) — e.g., "last 30 days", "last 90 days", "since January", "all time"
- **Focus area** (optional) — e.g., "billing issues", "onboarding", "technical problems", "full evaluation"

If the user doesn't specify a time range, ask before proceeding. Don't assume a default — different investigations need different windows.

## Privacy Rules

These rules are non-negotiable:
- **No DMs or private messages.** Never include content from direct messages or private 1:1 conversations. Only use public/shared channels and group conversations.
- **No Notion task lists.** Do not pull or reference any task lists, to-do lists, or personal task databases from Notion. Customer board entries, meeting notes, and internal docs are fine.
- **No sensitive internal-only commentary.** Summarize internal Slack discussions by theme and finding — do not quote verbatim messages that contain personal opinions about individuals or HR-sensitive content.

## Workflow

### Step 1: Identify the Customer

Resolve the customer name to actionable search terms:
- **Company name** — for CRM, Slack, Notion, Calendar, Gmail searches
- **Company domain** — for email/calendar filtering, web searches
- **Key contact names** — for meeting search, email lookup, Slack user lookup
- **CRM record IDs** — for HubSpot lookups

If the name is ambiguous, search HubSpot first to confirm the company record, then use that as the anchor for all other searches.

### Step 2: Gather CRM Context (HubSpot) — RUNS FIRST

CRM data is the commercial backbone of the report. Pull this first because it provides the ARR, deal stage, renewal dates, and contacts that contextualize everything else.

Load HubSpot tools first:
```
ToolSearch({ query: "select:mcp__claude_ai_HubSpot__search_crm_objects,mcp__claude_ai_HubSpot__get_crm_objects,mcp__claude_ai_HubSpot__get_properties,mcp__claude_ai_HubSpot__search_owners" })
```

Search for:
1. **Company record** — search companies by name to get the master record
2. **Associated deals** — all deals tied to the company (open, closed won, closed lost)
3. **Associated contacts** — key contacts at the customer, with titles and roles
4. **Tickets** — any HubSpot tickets associated with the company
5. **Deal owner** — who internally owns the relationship

**What to extract:**
- Current deal stage, ARR/ACV, contract dates
- Deal history (when they became a customer, any expansions, any at-risk signals)
- Key contacts and their roles
- Renewal date and contract terms
- Historical deal notes or activity

### Step 3: Search All Other Sources in Parallel

Launch searches across all remaining services simultaneously. Use subagents where possible to parallelize.

**The goal is speed** — don't search sources sequentially when they can run at the same time.

#### Source A: Public Profile & Web Search

Search the web for the customer's public profile — company overview, funding, press coverage, partnerships, and growth signals. This provides essential context that internal data alone cannot.

1. `WebSearch` — search for the company name + "funding", "series", "fintech", etc.
2. `WebSearch` — search for recent news or press coverage
3. `WebFetch` — fetch the company's website homepage for mission/product description

**What to extract:**
- Company overview (founded, location, leadership, investors)
- Total funding and recent rounds
- Product/service description and target market
- Public growth metrics (if available)
- Recent press coverage (positive or negative — especially regulatory or compliance news)
- Competitive positioning

#### Source B: Meeting & Calendar History

Search Google Calendar for meetings with the customer's contacts.

Load calendar tools:
```
ToolSearch({ query: "select:mcp__claude_ai_Google_Calendar__gcal_list_events" })
```

Search for calendar events mentioning the customer name or key contacts.

**What to extract:**
- Meeting timeline (dates, titles, attendees)
- Meeting frequency and cadence
- Who from your team attends most often
- How meeting topics have evolved over time

#### Source C: Email History (Gmail)

Search Gmail for correspondence with the customer.

Load Gmail tools:
```
ToolSearch({ query: "select:mcp__claude_ai_Gmail__gmail_search_messages,mcp__claude_ai_Gmail__gmail_read_message,mcp__claude_ai_Gmail__gmail_read_thread" })
```

Search for emails to/from the customer's domain. Read the most relevant threads.

**What to extract:**
- Key email threads and topics
- Commitments made over email
- Tone and sentiment in recent exchanges
- Any escalation emails or executive-level correspondence

#### Source D: Slack Conversations

Search Slack for recent discussions about the customer. Use private search to catch internal-only channels.

Load Slack tools:
```
ToolSearch({ query: "select:mcp__plugin_slack_slack__slack_search_public_and_private,mcp__plugin_slack_slack__slack_read_thread" })
```

1. Search for the customer name (try both the company name and common abbreviations)
2. For the top 5-10 most relevant threads, read the full thread

**Privacy:** Only search shared/group channels. Never include content from DMs or 1:1 private conversations. Summarize findings by theme — do not quote verbatim messages containing personal opinions about individuals.

**What to extract:**
- Internal discussions about the customer (concerns, plans, decisions)
- Direct communications if any shared channels exist
- Escalation threads or urgent conversations
- Who internally is most engaged with this customer
- Any crisis or reputational discussions

#### Source E: Jira / Support Tickets

Search for customer-related support tickets and issues.

Load Jira tools if available:
```
ToolSearch({ query: "+atlassian search" })
```

1. Search for tickets mentioning the customer name
2. Look for open vs. recently closed tickets
3. Note ticket severity, age, and resolution status

**What to extract:**
- Open tickets (count, severity, age)
- Recently resolved tickets (what was fixed, how long it took)
- Recurring themes (same type of issue coming up repeatedly?)
- Any P1/P2 incidents

#### Source F: Support Platform (Pylon)

Search Pylon for customer support conversations and account data. Pylon MCP tools are available directly — no ToolSearch needed.

**Workflow:**

1. **Find the account** — `mcp__pylon__search_accounts` with the customer name (partial match supported)
   - Extract the account ID, owner, tags, and any custom fields
   - If no match, try alternate names or the company domain
2. **Search open issues** — `mcp__pylon__search_issues` with:
   - `account`: customer name or account ID
   - `states`: `["new", "waiting_on_you", "waiting_on_customer", "on_hold"]`
   - Increase `limit` to 100 for high-volume accounts
3. **Search recently closed issues** — `mcp__pylon__search_issues` with:
   - `account`: customer name or account ID
   - `states`: `["closed"]`
   - `created_after`: start of the requested time range (RFC3339 format)
4. **Deep-dive on critical issues** — For any high-priority or escalation-relevant issues, call:
   - `mcp__pylon__get_issue` with the issue ID for full details (body, custom fields, metadata)
   - `mcp__pylon__get_issue_messages` with the issue ID for the full conversation thread
5. **Get contact details** — If key requester contacts appear, use `mcp__pylon__get_contact` to get their full profile

**What to extract:**
- Total open issues vs. resolved in the time range
- Issue breakdown by state (new, waiting_on_you, waiting_on_customer, on_hold)
- Issue types (conversation vs. ticket)
- Tags and categories — what themes dominate?
- Average age of open issues
- Responsiveness pattern — how many are "waiting_on_you" (your team) vs. "waiting_on_customer"?
- Key requester contacts and their volume
- Full conversation history on any escalation-relevant issues
- Account owner and tags from the Pylon account record

#### Source G: Notion / Internal Docs

Search Notion for customer-related documentation. **Do NOT pull task lists or to-do databases.**

Load Notion tools:
```
ToolSearch({ query: "select:mcp__notion__notion-search" })
```

1. Search for the customer name
2. Check any customer board or account database for the customer's entry
3. Look for meeting notes, internal docs, and relationship context

**What to extract:**
- Customer profile and account details (classification, key contacts, contract info)
- Internal notes, runbooks, or playbooks
- Historical context (onboarding notes, implementation decisions)
- Relationship context (customer tier, internal owner assignments, sentiment notes)

#### Source H: Error Tracking (Sentry)

If there's a technical dimension to the investigation, check Sentry for recent error spikes related to the customer.

Load Sentry tools if relevant:
```
ToolSearch({ query: "+sentry search" })
```

Search for issues related to the customer's project or environment.

**What to extract:**
- Unresolved errors and recent spikes
- Platform stability signals
- Any customer-reported technical issues correlated with error data

Only include this if there's a platform/technical dimension. Skip for purely relationship-focused analyses.

### Step 4: Synthesize the Report

Combine all findings into a structured report. Use the CRM data from Step 2 as the commercial backbone and the meeting/email history as the qualitative backbone — together they provide the narrative arc that all other data sources support and contextualize.

**Important:** Read source data before describing it. Never summarize something you haven't actually seen. If a source returned no results, say so — don't fill gaps with assumptions. State each finding once in its primary section — do not duplicate context across sections.

## Output Format

Use numbered Roman numeral sections. Include data tables wherever possible — they're easier to scan than prose.

```markdown
# Customer 360: [Customer Name]

**Date:** [today]
**Time Range:** [specified range]
**Focus:** [if specified, otherwise "General review"]

---

## Executive Summary

[3-5 sentences capturing the overall state of the customer relationship. Lead with the most important finding. Include key metrics: ARR if known, deal stage, renewal date, engagement level. If this is an escalation investigation, start with what appears to have gone wrong and when.]

---

## I. Public Profile & Growth Drivers

### Company Overview

| Detail | Value |
|--------|-------|
| **Founded** | [year, location] |
| **Leadership** | [key executives] |
| **Website** | [url] |
| **Total Funding** | [amount and rounds] |
| **Investors** | [key investors] |

### What They Do

[2-3 paragraph description of the company's product, target market, and business model]

### Public Growth Metrics

[Bullet points of publicly reported metrics]

### Key Public References

[Links to press coverage, funding announcements, etc.]

---

## II. CRM / Account Overview

### Deal Summary

| Detail | Value |
|--------|-------|
| **Current Stage** | [stage] |
| **ARR / ACV** | [amount] |
| **Contract Start** | [date] |
| **Renewal Date** | [date] |
| **Deal Owner** | [name] |
| **Pipeline** | [pipeline name] |

### Deal History

| Date | Event | Details |
|------|-------|---------|
| [date] | [closed won / expansion / renewal / etc.] | [context] |

### Key Contacts

| Name | Title | Email | Role in Relationship |
|------|-------|-------|---------------------|
| [name] | [title] | [email] | [champion / decision maker / user / etc.] |

### CRM Notes & Activity

[Summary of recent CRM activity, logged calls, notes]

---

## III. Meeting & Communication History

### Meeting Timeline

| Date | Meeting Title | Your Team | Their Team | Source |
|------|--------------|-----------|------------|--------|
| [date] | [title] | [names] | [names] | [Calendar/Notion] |

### Key Meeting Summaries

[For each significant meeting, summarize topics, decisions, and sentiment. Group by strategic importance.]

### Email Highlights

[Key email threads, commitments made, tone of recent exchanges]

### Communication Pattern Analysis

[Meeting cadence, who attends, how topics evolve, email responsiveness]

---

## IV. Internal Discussions (Slack)

[Summarize key internal conversations by theme. Do not include DMs or quote individuals' personal opinions verbatim.]

### [Theme 1 — e.g., "Pricing Concerns"]
[Summary of relevant discussions]

### [Theme 2 — e.g., "Technical Escalation"]
[Summary]

---

## V. Support Activity

### Jira Tickets ([N] found)

| Ticket | Summary | Status | Created | Assignee |
|--------|---------|--------|---------|----------|
| [linked ticket ID] | [summary] | [status] | [date] | [name] |

### Support Platform (Pylon)

| Metric | Value |
|--------|-------|
| **Open Issues** | [N] |
| **Waiting on You** | [N] |
| **Waiting on Customer** | [N] |
| **On Hold** | [N] |
| **Resolved (in time range)** | [N] |
| **Account Owner** | [name] |

### Recent Pylon Issues

| # | Title | State | Created | Requester | Tags |
|---|-------|-------|---------|-----------|------|
| [num] | [title] | [state] | [date] | [name] | [tags] |

### Key Takeaways

[Patterns, critical open issues, resolution trends, recurring themes]

---

## VI. Internal Docs & Relationship Context (Notion)

[Customer classification/tier, key relationship dynamics, account ownership, internal concerns or strategic notes — sourced from Notion customer board and internal docs. Do NOT include task lists.]

---

## VII. Technical Signals (Sentry)

[Only if relevant. Unresolved errors, error spikes, stability signals. Skip entirely for relationship-only analyses.]

---

## VIII. Risk Signals & Key Findings

### HIGH RISK
[Numbered findings with evidence from specific sources]

### MEDIUM RISK
[Numbered findings]

### WATCH
[Numbered findings]

---

## IX. Proactive Recommendations

### Immediate (This Week)
[Numbered, concrete actions]

### Short-Term (Next 30 Days)
[Numbered actions]

### Medium-Term (Next 90 Days)
[Numbered actions]

---

## X. Sources Searched

| Source | Results | Notes |
|--------|---------|-------|
| Web Search | [N] articles | [coverage notes] |
| HubSpot (CRM) | [details] | [notes] |
| Google Calendar | [N] events | [notes] |
| Gmail | [N] threads | [search terms used] |
| Slack | [N] threads | [search terms used] |
| Jira | [N] tickets | [notes] |
| Pylon | [N] issues | [notes] |
| Notion | [N] pages | [notes] |
| Sentry | [N] issues | [or "skipped"] |
```

## Cross-Referencing for Risk Detection

When synthesizing, actively cross-reference data across sources to identify risk patterns:

- **High support volume + upcoming renewal** = at-risk flag
- **High support volume + new customer** = onboarding issue flag
- **Escalation emails + Slack urgency threads** = active crisis
- **Low meeting cadence + open tickets** = disengagement risk
- **Expansion deal in CRM + elevated support volume** = expansion at risk (needs save-and-grow strategy, not just retention)
- **Recent press about funding/layoffs + reduced engagement** = business health risk

Quantify everything. "Several customers are frustrated" is useless. "4 open P2 tickets, 12 Slack mentions in the last 7 days, and a renewal in 45 days" is actionable.

## Tips

- **Parallelism matters.** The biggest time sink is searching 8+ services sequentially. Use subagents to search multiple sources at the same time. The synthesis step at the end is where you connect the dots — the searches themselves are independent.
- **CRM is the commercial backbone.** HubSpot data provides the ARR, deal stage, and renewal dates that anchor the entire report. Pull this first.
- **Meetings and emails are the qualitative backbone.** They provide the narrative arc that the rest of the report supports. Start your synthesis from communications and layer in other sources.
- **Slack reveals internal sentiment.** What the team says about a customer internally (concerns about churn, frustration with requests, excitement about expansion) is often the most honest signal.
- **Connect, don't just list.** A Jira ticket about "API errors" + a Slack thread about "reliability concerns" + an email where the customer mentioned "evaluating alternatives" = a pattern. The value of this skill is in connecting dots across sources.
- **If a source fails or is unavailable, note it and move on.** Don't let one failed API call block the whole analysis. Document what couldn't be searched and why. If an MCP isn't connected, say what's missing and what the user would get by connecting it.
- **For escalation investigations, work backwards.** Start from the most recent event and trace the thread back through earlier interactions.
- **Analyze, don't just report.** Every data table should be followed by a key observation explaining what the data means in context.
- **Always include deal size and renewal date** when discussing risk or recommendations — these provide the commercial stakes.
