---
name: company-update
description: Get a comprehensive view of how the company is performing across all teams — product, engineering, revenue, customers, and ops. Use when you want to understand what's happening company-wide this week or quarter, where we stand on goals, key wins, and areas to watch. Searches Slack, Notion, and the strategy document. Good for staying informed without being in every meeting.
argument-hint: "[optional: time range or focus area — e.g. 'this week' or 'Q1 recap' or 'how is revenue doing']"
allowed-tools: mcp__plugin_slack_slack__slack_search_public mcp__notion__notion-search mcp__notion__notion-fetch mcp__notion__notion-query-data-sources ToolSearch Read Grep
---

# Company Update — Performance Overview

Give employees a clear, comprehensive view of how the company is performing across all areas.

## Configuration

This skill reads the following from `chief-context/company.yaml` — fill these in before running:

```yaml
company:
  name: ""

workspace:
  notion_workspace_slug: ""      # e.g., "acme" → https://www.notion.so/acme/...
  meetings_database_id: ""       # Notion data source ID for meeting notes DB
  weekly_update_parent_page_id: ""  # Notion page ID where weekly updates are created
  weekly_update_slack_channel: ""   # Slack channel ID for posting announcements

strategy:
  doc_path: ""                   # e.g., "strategy/strategic-context-q2-2026.md"
```

And from `chief-context/org.yaml`:

```yaml
leadership:
  - name: "CEO name"
    role: "CEO"
    slack_id: "U..."             # Slack user ID — used to search activity
    # ...
```

If any required config is missing, ask the user to fill it in before proceeding.

## Before Starting

1. Read the strategy doc at `strategy.doc_path` — this is the baseline. Pull current targets, recent actuals, and strategic initiatives.
2. Determine the time range: default to the current week (Monday–Friday) unless the user specifies otherwise. Express the date range explicitly as "April 13–17, 2026" (or equivalent Mon–Fri dates), not just "Week of [Friday]". All Slack and Notion searches should use `after:YYYY-MM-DD` filters anchored to Monday of the current week.
3. Load Notion and Slack tools upfront:
```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch,mcp__notion__notion-query-data-sources,mcp__plugin_slack_slack__slack_search_public" })
```

## Notion Sources

All meeting notes live in the configured Meetings database:
- Data source: read `workspace.meetings_database_id` from `chief-context/company.yaml`
- Key properties: `Name`, `Subtype`, `date:Meeting Date:start`
- Common subtypes: `WLM` (Weekly Leadership Meeting), `Support` (Support Working Session), `Implementation` (Implementation Status Review), `Alignment` (Eng Alignment), `Pipeline` (Pipeline Review)

**Do not use `notion-search` to find this week's meetings** — it returns results by keyword relevance, not date, and will surface prior weeks. Instead use `notion-query-data-sources` with a SQL query filtered to the current week's date range:

```sql
SELECT url, Name, "Subtype", "date:Meeting Date:start"
FROM "collection://<meetings_database_id>"
WHERE "date:Meeting Date:start" >= '<monday-of-week>'
  AND "date:Meeting Date:start" <= '<tuesday-of-week>T23:59:59'
ORDER BY "date:Meeting Date:start" ASC
```

Once you have the page URLs from the query, fetch each one with `notion-fetch` to read the full content.

The **Weekly Update** page (for What Matters, Product, Pipeline, and Customers sections) is different — it is a standalone page, not a meeting record. Find it with:
```
notion-search("Weekly Update")
```
Take the most recent result. It is the primary source for the week's narrative content across most sections.

## What to Cover

### What Matters This Week

Search Notion for this week's Weekly Update page — it is the primary source for what the company is actively focused on. The existing weekly update is the ground truth; use it to anchor What Matters.

Also search Slack for: `"blocker" OR "go-live" OR "critical" OR "urgent" OR "this week"` to surface any live urgency not yet in Notion.

**Extract:** The 2-3 most important things in flight right now — active implementations with imminent milestones, pipeline deals with near-term close dates, product deadlines. Do NOT surface board meeting dates, financing status, fundraising updates, or CEO-specific priorities. Frame everything as company priorities, not leadership priorities.

### One Thing You Should Know

This is the single most important signal from the week — proposed based on where the CEO had the highest engagement: Slack threads they responded to, meeting notes they're mentioned in, and the most active topics in recent working sessions.

Look up the CEO's name and Slack ID from `chief-context/org.yaml` (the leadership entry with `role: CEO`). Search Slack for messages from or mentioning the CEO (`from:<first-name>` or `<@<slack_id>>`) in the past week to identify where they were most actively engaged.

Search Notion for recent meeting notes (past 7 days) mentioning the CEO or flagged as high-priority.

**Extract:** The one issue, breakthrough, or risk that had the most leadership attention this week. This should connect directly to What Matters This Week.

### Product & Engineering

Search Slack: `"shipped" OR "released" OR "deployed" OR "launched" OR "merged" OR "v1."` — look for specific release numbers, feature names, and PR descriptions.

Search Notion for this week's Weekly Update page — it typically has a "Shipped this week" section with specifics.

**Extract:** Named releases with version numbers, specific features or UX changes, in-progress work with context on why it matters, and any reliability incidents (what happened, root cause, fix). Use real names — specific version strings and feature names beat generic phrases like "platform improvements."

### Revenue & Pipeline

Search Notion for this week's Weekly Update — the Sales & Pipeline section typically has current late-stage deals, named accounts, and amounts.

Search Slack for: `"walk to close" OR "closed" OR "signed" OR "new customer" OR "contract"` for live signals.

Do NOT rely solely on the strategy doc for pipeline numbers — it goes stale quickly. Use live Notion/Slack signals for specific deal names and amounts. Strategy doc is useful only for baseline metrics (prior-quarter actuals, full-year targets).

**Extract:** Named deals in late-stage with amounts and target close dates. Any past-due deals. Strategic opportunities worth flagging. Do not surface board, financing, or fundraising updates.

### Customers & Implementation

Search Notion for this week's Weekly Update — the Customers & Implementation section has per-customer narratives.

Search Slack: `"go-live" OR "implementation" OR "onboarding" OR "expansion" OR "at risk"` for any live signals.

**Extract:**
- Per-customer narrative updates — specific wins, blockers, milestones, and next steps for each active account. Generic lists are not useful.
- Watch items — accounts with active risks or time-sensitive dependencies.
- 30/60/90-day post go-live flags — call out any customers at these milestones explicitly. This is the window where adoption habits form and early churn risk concentrates.

### Support

**Primary source:** The Support Working Session meeting note from the current week. Query the Meetings database for `Subtype = "Support"` on Monday–Tuesday of the current week, then fetch the page. Do not use `notion-search("support working session")` — it surfaces prior weeks.

Search Slack for: `"developer support" OR "support queue" OR "ticket"` for any signals between sessions.

**Extract:** Which customers are generating the most support volume and why. Escalations and their status. Top bugs being prioritized. Patterns in developer/API support activity. What's on the support working session agenda.

### Shoutouts

**Primary source:** The WLM (Weekly Leadership Meeting) meeting note from the current week. Query the Meetings database for `Subtype = "WLM"` on Monday–Tuesday of the current week, then fetch the page. Do not use `notion-search` — it surfaces prior weeks.

If the WLM page does not have an explicit Shoutouts section, extract celebrations from the content: go-lives, at-risk accounts that moved to on-track, individuals called out by name for stepping up, notable completions. Also check the Support Working Session for anyone called out there.

**Extract:** Verbatim or close-paraphrase shoutouts. Keep this section warm and specific — use real names and say what they did.

## Output Format

Keep it skimmable. No icons, no stylization. Plain structure.

```
# Weekly Update — [Mon date – Fri date, YYYY]

## What Matters This Week
[2-3 bullets. Specific milestones, imminent go-lives, pipeline deadlines. No board/financing/CEO framing.]

## One Thing You Should Know
[The single issue with the highest leadership engagement this week. Should connect to What Matters.]

---

## Product & Engineering
**Shipped:** [Named releases, specific features — version numbers and feature names]
**In Progress:** [What's actively being built and why it matters]
**Notes:** [Incidents, reliability events, infrastructure watch items]

## Sales & Pipeline
[Named late-stage deals with amounts and close targets. Strategic opportunities. Quarterly progress vs. target.]

## Customers & Implementation
[Per-customer narratives — specific wins, blockers, next steps. Watch items. 30/60/90-day post go-live flags.]

## Support
[Top accounts by volume. Escalations. Bug prioritization. Developer support patterns.]

## Shoutouts
[From this week's WLM — real names and what they did.]
```

## Publishing

Do NOT publish until the user explicitly approves the output ("ship it", "publish it", "post it", or similar). After approval, do both steps:

**Step 1 — Create Notion page**

Parent page: read `workspace.weekly_update_parent_page_id` from `chief-context/company.yaml`.

```
notion-create-pages({
  parent: { type: "page_id", page_id: "<weekly_update_parent_page_id>" },
  pages: [{ properties: { title: "Weekly Update — [Mon date–Fri date, YYYY]" }, content: "..." }]
})
```

Use the full update content as-is (Notion markdown). Do not include the title in the content body.

After creating the page, construct the canonical workspace URL for use in the Slack post — the Notion MCP only returns raw UUID URLs, which trigger Slack's "untrusted link" warning. Build the URL manually using the workspace slug:

```
https://www.notion.so/<notion_workspace_slug>/Weekly-Update-[Mon-Fri-YYYY]-[page-id-no-dashes]
```

The page ID comes from the `notion-create-pages` response. Strip the dashes from the UUID.

**Step 2 — Post to Slack**

Channel: read `workspace.weekly_update_slack_channel` from `chief-context/company.yaml`.

Post a brief announcement that links to the Notion page — do NOT paste the full update into Slack. 2-3 sentences max: what week it covers, the link, and one sentence with the 2-3 biggest things from the week.

Example format:
```
Weekly Update is up for [date range]: [Notion page URL]

[One sentence hitting the 2-3 most important things — a go-live, closed deals, a key risk.]
```

Slack formatting rules:
- Plain text only — no bold, no bullets, no markdown
- Do NOT use `---` horizontal rules
- Do NOT use special unicode characters (em dashes, arrows)

## Rules

- Use specific names, numbers, and dates. "Strong pipeline" means nothing. "$492K in late-stage across 10 deals" is useful.
- The existing weekly Notion update is the primary source of truth for live data — the strategy doc is the baseline for targets and actuals only.
- Never mention board meetings, financing, fundraising, or investor updates.
- Never frame content as CEO priorities. Frame as company priorities.
- Per-customer updates must be narratives, not lists. If you don't have specifics for a customer, skip them.
- If a search returns nothing useful for a section, say so briefly and move on.
- Do not stylize the output — no icons, no emoji, no callout boxes. Plain headers and bullets only.
- Keep each section focused: employees should be able to read this in 3-5 minutes.
- Don't include information only one person would care about — every bullet should matter to at least one full team.
