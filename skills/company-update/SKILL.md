---
name: company-update
description: Get a comprehensive view of how the company is performing across all teams — product, engineering, revenue, customers, and ops. Use when you want to understand what's happening company-wide this week or quarter, where we stand on goals, key wins, and areas to watch. Searches Slack, Notion, and the strategy document. Good for staying informed without being in every meeting.
argument-hint: "[optional: time range or focus area — e.g. 'this week' or 'Q1 recap' or 'how is revenue doing']"
allowed-tools: mcp__plugin_slack_slack__slack_search_public mcp__plugin_slack_slack__slack_search_public_and_private mcp__plugin_slack_slack__slack_search_channels mcp__plugin_slack_slack__slack_send_message mcp__plugin_slack_slack__slack_read_thread mcp__plugin_slack_slack__slack_read_channel mcp__notion__notion-search mcp__notion__notion-fetch mcp__notion__notion-query-data-sources mcp__notion__notion-create-pages mcp__notion__notion-update-page mcp__pylon__search_issues mcp__pylon__search_accounts mcp__pylon__get_account mcp__pylon__get_issue mcp__hubspot__hubspot-search-objects ToolSearch Read Grep Bash
---

# Company Update — Performance Overview

Give employees a clear, comprehensive view of how the company is performing across all areas.

## Configuration

This skill assumes a few operational inputs unique to your workspace. Replace the placeholders below with your own values before first use, or move them into a chief-context config and resolve them at runtime.

| Placeholder | What it is |
|---|---|
| `<MEETINGS_DB_URL>` | URL of your weekly-meetings Notion database |
| `<MEETINGS_DATA_SOURCE_URL>` | `collection://<uuid>` data-source URL for the same database |
| `<WEEKLY_PRIORITIES_PARENT_PAGE_ID>` | Notion page ID where weekly-update child pages are created |
| `<ANNOUNCEMENTS_CHANNEL_ID>` | Slack channel ID for the company-wide announcement post |
| `<WORKSPACE_SLUG>` | Your Notion workspace slug (used in canonical page URLs) |
| `<CEO_SLACK_USER_ID>` | Slack user ID of the CEO (for engagement queries) |
| `<MARKETING_LEAD_SLACK_USER_ID>` | Slack user ID of the marketing lead curating the LinkedIn roundup |
| `<STRATEGIC_CONTEXT_DOC>` | Path to your quarterly strategic context document |
| `<TEAM_SHARED_CALENDAR_NAME>` | Name of the shared Google Calendar holding OOO + work-anniversaries |
| `<CEO_AGENTS_CHANNEL>` | Slack channel where the CEO drops queries to internal AI agents (e.g. `#phi-canvas-agent-chat`). Often private — will require `slack_search_public_and_private`. |
| `<PIPELINE_DASHBOARD_SHEET_ID>` | Google Sheets ID for the Weekly Pipeline Dashboard (source for the forward-looking quarterly forecast in Sales & Pipeline) |
| `<KPI_SHEET_ID>` | Google Sheets ID for the Canvas KPIs — MAPs, Users & Revenue workbook. Used to segment Live vs Pre Go-Live in Customer operations. Tabs used: `Combined Summary` (headline totals + latest closed month) and `G7 - MAPs per Customer` (per-customer prior-month MAPs, Status, Go-Live Month). |
| `<CUSTOMER_RECON_DB_URL>` | Full Notion URL of the Customer Name Reconciliation Map database. |
| `<CUSTOMER_RECON_DATA_SOURCE_ID>` | Data source (collection) UUID of the same DB. Use with `notion-query-data-sources` as `collection://<uuid>`. Legal-entity → Pylon ID join for the Customer operations table. |

## Before Starting

1. Read `<STRATEGIC_CONTEXT_DOC>` — this is the baseline. Pull current targets, recent actuals, and strategic initiatives.
2. Determine the time range: default to the current week (Monday–Friday) unless the user specifies otherwise. Express the date range explicitly as "April 13–17, 2026" (or equivalent Mon–Fri dates), not just "Week of [Friday]". All Slack and Notion searches should use `after:YYYY-MM-DD` filters anchored to Monday of the current week.
3. Load Notion, Slack, Pylon, HubSpot, AND Jira tools upfront. Pylon is required for the Support section's fallback path (see Support). HubSpot is required for the Sales section's MTD closed-won/lost cross-check. Jira (`mcp__atlassian__searchJiraIssuesUsingJql`) is required for the P&E "In progress" section, migration status, and cross-linking KOALA/STUDIO/PLUGIN ticket IDs surfaced by the WLM or GitHub PRs. `slack_search_public_and_private` is required for scanning `<CEO_AGENTS_CHANNEL>` (typically a private `phi-*` channel):
```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch,mcp__notion__notion-query-data-sources,mcp__notion__notion-create-pages,mcp__notion__notion-update-page,mcp__plugin_slack_slack__slack_search_public,mcp__plugin_slack_slack__slack_search_public_and_private,mcp__plugin_slack_slack__slack_search_channels,mcp__plugin_slack_slack__slack_send_message,mcp__plugin_slack_slack__slack_read_thread,mcp__plugin_slack_slack__slack_read_channel,mcp__pylon__search_issues,mcp__pylon__search_accounts,mcp__pylon__get_account,mcp__pylon__get_issue,mcp__hubspot__hubspot-search-objects,mcp__atlassian__searchJiraIssuesUsingJql,mcp__atlassian__getJiraIssue" })
```

## Notion Sources

All meeting notes live in the **Meetings** database:
- URL: `<MEETINGS_DB_URL>`
- Data source: `<MEETINGS_DATA_SOURCE_URL>`
- Key properties: `Name`, `Subtype`, `date:Meeting Date:start`
- Subtypes to know: `WLM` (Weekly Leadership Meeting), `Support` (Support Working Session), `Implementation` (Implementation Status Review), `Alignment` (Eng Alignment), `Pipeline` (Pipeline Review)

**Do not use `notion-search` to find this week's meetings** — it returns results by keyword relevance, not date, and will surface prior weeks. Instead use `notion-query-data-sources` with a SQL query filtered to the current week's date range:

```sql
SELECT url, Name, "Subtype", "date:Meeting Date:start"
FROM "<MEETINGS_DATA_SOURCE_URL>"
WHERE "date:Meeting Date:start" >= '2026-04-13'
  AND "date:Meeting Date:start" <= '2026-04-14T23:59:59'
ORDER BY "date:Meeting Date:start" ASC
```

Replace the date literals with Monday and Tuesday of the current week. The WLM typically lands Monday–Tuesday; the Support Working Session typically lands Monday–Tuesday as well. Once you have the page URLs from the query, fetch each one with `notion-fetch` to read the full content.

The **Weekly Update** page (for What Matters, Product, Pipeline, and Customers sections) is different — it is a standalone page, not a meeting record. Find it with:
```
notion-search("Weekly Update")
```
Take the most recent result. It is the primary source for the week's narrative content across most sections.

## What to Cover

### What Matters This Week

Search Notion for this week's Weekly Update page — it is the primary source for what the company is actively focused on. The existing weekly update is the ground truth; use it to anchor What Matters.

Also search Slack for: `"blocker" OR "go-live" OR "critical" OR "urgent" OR "this week"` to surface any live urgency not yet in Notion.

**CEO strategy memos are a first-class What Matters signal.** *(Feedback from a prior update: the CEO authored a risk-assessment memo for the upcoming leadership meeting and the first draft completely missed it — even though it was the operating agenda for the coming week.)* Every reporting window, actively search for and surface any strategy memo, risk assessment, or analysis the CEO authored and circulated in Slack during the window. This is often the most important operating context of the week — it sets the agenda for the next WLM and names owner-level actions. Sources to check, in order:

1. **Notion pages created by the CEO in-window** — use `notion-search` with `filters.created_by_user_ids = [<CEO_NOTION_USER_ID>]` and `filters.created_date_range.start_date = <MON>`:
```
notion-search({ query: "memo OR analysis OR risk OR strategy OR assessment", filters: { created_by_user_ids: ["<CEO_NOTION_USER_ID>"], created_date_range: { start_date: "<MON>", end_date: "<SAT>" } }, page_size: 15 })
```
2. **Notion pages that are children of the upcoming WLM** — the next WLM often gets memos attached as agenda material. Fetch the upcoming WLM Notion page and enumerate its child pages.
3. **Slack messages from the CEO in `#announcements`, `#phi-agents-chat`, `#phi-collab`, and any private strategy channel** with links to Notion pages posted in the window:
```
slack_search_public_and_private({ query: "from:<@<CEO_SLACK_USER_ID>> after:<MON> before:<SAT> (memo OR \"risk assessment\" OR analysis OR strategy OR notion.so)", limit: 15, include_context: false })
```

**When a memo is found, surface it as its own What Matters bullet** with (a) the memo title + link, (b) the universe/scope, (c) the top numeric finding, (d) the named owner-level actions for the coming week, and (e) an explicit line telling the reader to read it before the next WLM. Do NOT paraphrase the memo away — the CEO wrote it in a specific voice and the operating team needs the direct link.

**Four rules on summarizing an internal memo for a company-wide audience.**

1. **Soften an absolute internal verdict into its business consequence.** A memo written for the leadership team can say a bet "is not working"; the company-wide summary says it "is creating downstream negative impact." The update is read by everyone who built the thing being judged, and a flat verdict lands on them personally.
2. **Never carry over a memo's list of customers used as negative examples.** Naming customers as cost or quality problems is fine in a private memo and is not fine in a document this widely read. Keep the finding, drop the roster.
3. **Never editorialize a customer's request.** Report what the customer asked for and stop.
4. **Sourcing caveats do not go in the body.** If you cannot confirm who wrote something, resolve it before publishing or raise it in the handoff. Never publish your own uncertainty as a sentence the whole company reads.

**Render a numeric series as a table, not a comma list in prose.** Any bullet carrying more than about four numbers that share a unit wants to be a table.

**Extract:** The 2-3 most important things in flight right now — active implementations with imminent milestones, pipeline deals with near-term close dates, product deadlines, plus any CEO-authored strategy memo circulated in-window. Do NOT surface board meeting dates, financing status, or fundraising updates. Frame everything as company priorities, not leadership priorities. (A CEO-authored memo is a company priority because it is setting the coming week's agenda — that's what makes it eligible here.)

### One Thing You Should Know

This is the single most important signal from the week — proposed based on where the CEO had the highest engagement: Slack threads they responded to, meeting notes they're mentioned in, and the most active topics in recent working sessions.

Search Slack for messages from or mentioning the CEO (`from:<CEO_HANDLE>` or `<@<CEO_SLACK_USER_ID>>`) in the past week to identify where they were most actively engaged.

Search Notion for recent meeting notes (past 7 days) mentioning the CEO or flagged as high-priority.

Critically, do not limit this to threads the CEO drove. Cross-reference the High-Engagement Threads You Were Not In pass below: the single most important signal of the week is often a conversation the CEO missed, not one they led.

**Extract:** The one issue, breakthrough, or risk that had the most leadership attention this week. This should connect directly to What Matters This Week.

### CEO Agent Queries (Signal Mining)

The CEO uses `<CEO_AGENTS_CHANNEL>` (typically `#phi-canvas-agent-chat`, a private channel) to drop queries to internal AI agents — Investigator, Rhizome, Sisyphus, Navigator, Cerberus, Janus, etc. These queries are a strong leading signal for the weekly update because they surface **the exact data the CEO is chasing right now** — often numbers for an investor memo, definitions of newly-live systems, cross-account benchmarks, or requests for coverage the team hasn't yet published. The threaded agent responses frequently contain the freshest quantitative snapshot available anywhere.

**This is a required standing pass** — always run it, and always incorporate any material findings into the appropriate downstream section (What Matters, Product & Engineering, or Shoutouts). Do not omit it silently even if the week is quiet.

**Step 1 — Locate the channel ID.** If `<CEO_AGENTS_CHANNEL>` is only known by name (e.g. `#phi-canvas-agent-chat`), resolve to its ID first with `slack_search_channels`. Cache the ID in the skill's memory notes for future runs.

**Step 2 — Pull CEO-authored messages** in the reporting window from that channel. The channel is typically private, so use `slack_search_public_and_private`:

```
mcp__plugin_slack_slack__slack_search_public_and_private({
  query: "in:<CEO_AGENTS_CHANNEL> from:<@<CEO_SLACK_USER_ID>> after:<monday> before:<saturday>",
  limit: 20,
  sort: "timestamp"
})
```

**Truncation-risk mitigation.** `slack_search_public_and_private` on active agent channels can return >60K-character results that overflow the tool result and get spilled to a file. To avoid that, always add `include_context: false` and cap `limit` at 10 on the first call; if you need more, paginate with the cursor rather than raising the limit. If the result still spills to a file, prefer reading a targeted `slack_read_thread` on each parent `message_ts` instead of ingesting the whole spill file.

**Step 3 — Read the threaded response for each CEO-authored parent.** Use the parent `message_ts` from Step 2 and read the thread. Agent responses may be long; skim for the concrete data payload (numbers, table, explanation, or drop-in replacement text). If the CEO asked a follow-up in the same thread, capture that too — it often clarifies intent and locks a specific framing.

**Step 4 — Classify each query and route the highlight to the right section:**

| Query shape | Route the highlight to |
|---|---|
| "Update this paragraph in an investor memo with the latest [X]" or "give me the most recent [metric]" | **What Matters This Week** — the refreshed number is usually a headline-worthy signal. Quote the number series (old → new) so the reader sees the trajectory. |
| "What is [system / agent / tool]?" or "how does [X] work?" | **Product & Engineering** — the CEO has just surfaced something the wider team may not have visibility into yet. Add a bullet explaining what it is, when it went live, who built it, and current status. |
| "Quantify the impact of [X]" or "how many [event] since [date]" | **Product & Engineering** or **What Matters** — depends on magnitude. Include the actual number, not just the ask. |
| "Verify our answer to [customer]" or "why did [customer] hit [issue]" | **Customers & Implementation** — cross-reference with the customer's account state before adding. |
| Explicit praise ("nice work!", "this is awesome", "directionally where we want to be") | **Shoutouts** — quote the CEO's words verbatim and name the person / project being praised. Cross-reference the agent response to identify the author. |

**Step 5 — Format the highlight.** When you insert a bullet in a downstream section, always end with a parenthetical source note so the reader can trace it: `(Source: Adam → Investigator, #phi-canvas-agent-chat 7/1, pulled for an investor memo refresh.)` or similar. This makes the provenance visible and legitimizes the number.

**Rules for this pass:**
- **Never invent or extrapolate.** Only use numbers that appear verbatim in the agent's threaded response. If the response says "these numbers don't exist yet" (as Investigator sometimes does), do NOT publish placeholder estimates — note the gap or omit.
- **Skip pure ops requests.** Queries like "deploy X to Y" or "restart Z" are not update material.
- **Attribute the author of any system the CEO surfaces**, even if the CEO didn't. If Investigator's response names an original author (e.g. "originally built by [name]"), that person belongs in Shoutouts.
- **The CEO's own praise is a shoutout signal.** If the CEO writes "nice work!" or similar in the thread, that's a first-class shoutout — quote it.
- **When the CEO's ask ends without a satisfactory answer**, that itself may be a signal for the Product & Engineering "Notes" bullet — e.g. "Adam asked for X metric this week; the answer is that we can't compute it yet because [reason]" is legitimately worth surfacing.

**Extract:** For each CEO-originated query in the window, one internal note per query capturing (a) what was asked, (b) the concrete answer, (c) which downstream section it fed, (d) the source link. Publish the concrete answer through the routed section, not as its own top-level section.

### High-Engagement Threads You Were Not In

The weekly update has a blind spot: it leans on threads the CEO already engaged with (the "One Thing" and Shoutouts passes both key off CEO activity), so the most important conversations the CEO *missed* never surface. This pass finds the week's highest-engagement cross-team threads regardless of whether the CEO participated, then prioritizes the ones they did not.

**Scope: cross-team and high-impact only.** Run this discovery ONLY across broad, cross-team channels. Do NOT pull from narrow or sensitive channels (HR / people-ops, exec / leadership-private, financing / fundraising, security-incident, 1-1 or small-group channels, DMs). A thread qualifies only if it is relevant to at least one full team. Use this allowlist (confirm and extend for your workspace - add customer / implementation channels as needed):

```
#announcements
#team-engineering
#release
#phi-release-coordination
#phi-collab
#phi-agents-chat
```

**Step 1: Cast a wide net** across the allowlisted channels for the window. Slack search has no "minimum replies" operator, so search on activity and read the candidates:

```
mcp__plugin_slack_slack__slack_search_public({ query: 'in:<channel> after:<monday> before:<saturday> is:thread', limit: 50 })
```

Repeat per allowlisted channel.

**Step 2: Rank by real engagement.** For each candidate thread, use `slack_read_thread` and score by reply count, number of distinct participants, and reactions on the parent or replies. A thread with 15 replies from 6 people across two teams outranks a 30-reply back-and-forth between two people. Engagement breadth (how many teams, how many distinct people) matters more than raw reply volume.

**Step 3: Flag the CEO's blind spots.** Mark every high-engagement thread where the CEO (`<@<CEO_SLACK_USER_ID>>`) posted no message. These are the priority - surface the top 2-3 explicitly, because they are exactly what the CEO would otherwise miss.

**Extract:** The top 2-3 high-engagement threads, feeding into "What Matters This Week" and "One Thing You Should Know." For each: a one-line summary, the teams involved, the engagement level (e.g. "23 replies, 8 people across Eng + Support"), a note if the CEO was absent from the thread, and a link to the thread.

### Special-Event Recap (conditional — insert between "One Thing You Should Know" and "Product & Engineering" only when applicable)

*Pattern validated by the 7/20–24 update's Circle Up Summary — high engagement, kept the strategic narrative intact.* When the reporting week contains a **company-wide strategic event** (Circle Up recap of a board meeting, all-hands, org-change announcement, major strategic pivot, offsite readout), insert a dedicated H2 section between "One Thing You Should Know" and "Product & Engineering" with the recap. Do NOT bury this in "What Matters" — the event deserves standalone framing because the rest of the update (P&E priorities, customer risk, sales) is downstream of it.

**When to trigger:**
- The company held a Circle Up, all-hands, or all-company strategic session inside the reporting window
- An org-change announcement was made to the whole company (VP exit, structural reorg, function elimination)
- A quarterly board recap was shared internally
- A strategic pivot was announced (e.g., ICP change, product-line consolidation, GTM shift)

**Format:**
```
## [Event Name] — [One-line framing of what happened]

*Meeting: [Name], [Date], [Duration]. [What it was].* [Recording link if available].

**[H1 numbers or performance context, if applicable].**
- [Bullet-point summary of the H1 story with the specific numbers named in the meeting]

**[Strategic framing name, if any — e.g., "Strategic pivot to 'builders'"]**
- [2-3 bullets on the framework or pivot]

**[Initiative name — if a new initiative was launched at the event]**
- [Goal + method + team + timeline]

**Organizational changes.**
- [Structural changes with names, roles, dates]

Slides: [link]
Recording: [link]
```

**Rules for this section:**
- **Preserve the CEO's/leader's verbatim framing** where it was used at the meeting ("player-coach", "Death Zone", "willing to build") — those phrases become internal shorthand and should not be paraphrased away.
- **Include Fathom or recording links** so anyone who missed the meeting can watch.
- **Do not editorialize.** The recap conveys what was announced; the CEO's judgment layer belongs in "One Thing You Should Know," not here.
- **When the event announces a departure** (JP transitioning out, etc.), name the person, the last-day date, and any handoff details — do NOT euphemize the exit or bury it.

### Product & Engineering

**GitHub is the source of truth for this section — not the WLM.** The WLM 7/7 auto-summary was materially wrong on 2026-07-10: overcounted canvas-plugins (3 vs 0), canvas-agents (133 vs 74), and canvas-hyperscribe (5 vs 0), and included three "capabilities shipped this week" that all merged in the *prior* reporting week. Do not trust WLM commit counts, PR lists, or "shipped" bullets without a GitHub cross-check for the current reporting window. When they disagree, GitHub wins; note the discrepancy inline in a **WLM data-quality note** at the end of the section so the auto-summary owner can fix upstream.

**Step 1 — Pull commit counts per repo for the window.** Use `gh api` with explicit `since` / `until` bounded to Monday 00:00Z of the reporting week and the following Saturday 00:00Z (to capture Friday commits in any timezone). Standard repo list (extend as new repos become material):

```bash
for repo in canvas canvas-plugins canvas-agents canvas-hyperscribe control-room fumage fumage-e2e; do
  echo "=== $repo ==="
  gh api "repos/<YOUR_GH_ORG>/$repo/commits?since=<MON>T00:00:00Z&until=<SAT>T00:00:00Z&per_page=100" --jq 'length'
done
```

For canvas and canvas-plugins, also pin the primary branch — canvas ships from `develop`, canvas-plugins from `main`:

```bash
gh api "repos/<YOUR_GH_ORG>/canvas/commits?sha=develop&since=<MON>T00:00:00Z&until=<SAT>T00:00:00Z&per_page=200" --jq 'length'
gh api "repos/<YOUR_GH_ORG>/canvas-plugins/commits?sha=main&since=<MON>T00:00:00Z&until=<SAT>T00:00:00Z&per_page=200" --jq 'length'
```

If any repo returns 404 (private / renamed), record it and move on — don't leave gaps silent.

**Step 2 — Pull merged PRs per repo for the window.** Commit count alone doesn't say what shipped; merged PRs do. Use the `merged:` search qualifier:

```bash
gh pr list --repo <YOUR_GH_ORG>/<repo> --state merged --search "merged:<MON>..<FRI>" --json number,title,mergedAt,author --limit 50
```

Repeat for canvas, canvas-plugins, canvas-agents (if you want the agent-level detail), and canvas-hyperscribe at minimum. For each merged PR, capture: number, title, merge date, author (real name if available; skip bot-only PRs from the named list but count them in a separate "N bot-authored fixes" line so the volume is legible).

**Step 3 — Verify every "capability shipped" bullet against its merge date.** If the WLM or any other source claims a capability shipped this week, fetch the PR and confirm `mergedAt` falls **inside the reporting window (Mon 00:00 → Fri 23:59 local, generous UTC window is Mon 00:00Z → Sat 00:00Z)**. Anything merged before Monday belongs in the *prior* week's update — do not carry it forward. Command to verify a single PR:

```bash
gh api repos/<YOUR_GH_ORG>/<repo>/pulls/<number> --jq '{number, title, state, mergedAt: .merged_at, author: .user.login}'
```

**Step 4 — Verify releases against the release bot in #announcements.** The release bot in `#announcements` posts a message per release cut with the version number (e.g. `1.319.0`). Cross-check the WLM's release list against Slack:

```
mcp__plugin_slack_slack__slack_search_public({ query: 'in:announcements from:<@RELEASE_BOT_ID> after:<monday> before:<saturday>', limit: 20 })
```

If a release version is listed in the WLM but has no bot post in #announcements, treat it as unverified and either omit or flag.

**Step 5 — Also scan Slack for narrative signal.** GitHub gives the "what shipped" facts; Slack gives context on "why it matters" and "who noticed." Search Slack with `"shipped" OR "released" OR "deployed" OR "launched" OR "merged" OR "v1."` for authors' own framing of their work. Also check the current week's Weekly Update Notion page (if drafted) for narrative that isn't in the code.

**Step 6 — Jira cross-reference (required for the "In Progress" bullet and any KOALA/STUDIO/PLUGIN ticket surfaced by the WLM or PR titles).** GitHub tells you what shipped; Jira tells you what is *actively being worked on* and *what is blocked*. For every KOALA/STUDIO/PLUGIN ticket cited in the WLM or in a PR title, resolve its current status via Jira before writing it up. Also pull:

- **In-window ticket activity by initiative.** For each active initiative in your Jira (product/eng epics, migration board, plugin board):
```
mcp__atlassian__searchJiraIssuesUsingJql({
  cloudId: <canvas cloudId>,
  jql: "project IN (KOALA, STUDIO, PLUGIN) AND (updated >= '<MON>' OR resolved >= '<MON>') AND updated <= '<FRI>' ORDER BY updated DESC",
  fields: ["summary","status","assignee","updated","resolutiondate","customfield_10297"],
  limit: 100
})
```
- **Named ticket lookups** for anything the WLM auto-summary references (`<PROJECT>-<N>` IDs): use `getJiraIssue` and quote the current status inline, not the WLM's stale field.

Do NOT invent Jira status from PR titles — if you can't resolve a ticket ID against Jira within the run, mark the status "[unverified in Jira]" and move on. Jira must be reachable for the P&E section to be complete; if it is down, flag it in "Data hygiene" the way you would a Pylon outage.

**Extract:** Named releases with version numbers (verified against #announcements release bot), specific features or UX changes (verified against merged PRs in the window), in-progress work with context on why it matters (Jira-verified status), and any reliability incidents (what happened, root cause, fix). Use real names — "v1.296.0" and "[named feature] resilience improvements" beats "platform improvements." **Always cite PR numbers, merge dates, and Jira ticket IDs so a reader can spot-check the same way you did.**

### Product & Engineering — section shape

*Feedback from the 7/27–31 update: the first draft's P&E section listed 40+ merged PRs by name and was unreadable for anyone outside engineering. Rewrite triggered by Adam.*

The P&E section is written **for readers who are not in engineering.** The reader is a marketer, an IM, a salesperson, or the CEO — they want to understand what shipped and why it matters, not read a release-notes dump. Structure it as three subsections in this order:

1. **Releases (short prose, no table).** Do **not** publish a per-repo commits / PRs-merged / week-over-week table. It reads as a scoreboard to every non-engineer no matter how it is captioned, and the counts are consistently the least reliable numbers on the page. Publish instead: how many releases shipped to customers this week named by version and each verified released on your release-tracking board, the comparison to last week, what is cut but not yet shipped, and fleet state. You still pull commit and PR counts while researching, because they tell *you* where to look. They do not go in the document.
   - **Columns:** Repo · Commits · PRs merged · WoW commits.
   - **Rows:** one per material repo (studio, canvas, canvas-plugins, canvas-agents, canvas-hyperscribe), plus a `Total` row.
   - **WoW commits** = this week vs last week's number, with the absolute number and the direction (**+34** or -5). Bold the standouts.
   - **Below the table:** releases cut this week vs last week (a real velocity signal), plus 2–3 short reads: which repo led the week, where headcount is going, what the tail of a prior sprint looks like.

2. **Highlights (customer-value framing).** **Six or fewer** numbered highlights, each anchored to *why a non-engineer should care*. Each highlight leads with the customer/business impact, then names the engineer(s) and cites the top 1–2 PRs — never the exhaustive PR list. Format:
   - **Bold headline** (customer-value statement, one sentence).
   - Body: 2–4 sentences with the who, what, and one PR link each. If the change is customer-visible, say so plainly. If it's compounding leverage (SDK/reference plugin/agent), say what it unlocks.
   - **Do NOT list every merged PR by name.** The full PR list lives in GitHub; the update is not a release notes replacement.

3. **In progress / to watch.** 3–5 bullets max. Named releases with what they contain in plain English, unresolved organizational items (e.g., ToU deliverable un-owned), and any data-quality caveats worth flagging (e.g., control-room 404 on `gh api` — coverage numbers not GitHub-verified this week).

**Never name a person as the cause of a blocker, a delay, or an absence of output.** This update goes to the whole company. A named engineer attached to a blocker is read by every non-engineer as "this person is the problem," and it is almost never true — blockers are nearly always a vendor, a dependency, a staffing decision, a priority call, or a queue nobody owns.

- **The `Blocked / diverted by` column names causes, not people.** Three shapes work, in order of preference: the customer-visible impact of the constraint ("volume of plugin issues is exceeding our capacity to troubleshoot, and eroding trust across key accounts"); the external dependency ("blocked on the vendor's multi-tenant scope"); or the plain ticket status with no editorializing ("all four migrations are in Blocked status"). What does not go here: a person's name as the cause, an employment-status aside, time off, or an unresolved internal process argument with a name attached. The Owner column already tells the reader who to ask.
- **"Nothing here is blocked" is a legitimate value.** Write it when it is true rather than manufacturing a constraint to fill the cell.
- **Never write "nothing merged" under a person's name without checking what they were carrying.** Run the open-PR and in-flight check (`gh search prs --author <handle> --updated <MON>..<SAT>`, plus your engineering board and daily digests) *before* writing a zero. Someone with a large open PR had a full week, and a ticket assigned to them that merged under another author still counts as their work landing. A blank is a sourcing failure about as often as it is a real zero, and publishing it as a zero is the more damaging error.
- **Absence of merged code is a neutral fact about a workstream, never an implied criticism of its owner.** If an initiative did not move, lead with what the owner was doing instead.
- **Never name an individual on aging-PR, hygiene, or backlog bullets.** Report the count and the shape. Your daily digest already routes these to the people who own them.
- **Time off is never offered as a reason something did not happen.** State it in the OOO table and nowhere else.
- **Never attach an employment-status qualifier to a person.** Whether someone is full-time, part-time, or a contractor is not the reader's business and always reads as an excuse or a demotion attached to a name. If capacity genuinely explains an outcome, say the team is under-resourced on that workstream. Do not say who.
- **Read every sentence containing a person's name and ask whether it lands as praise, neutral fact, or criticism.** Criticism of a named individual does not belong in a company-wide update in any quantity. Take it to the team lead privately instead.

**Merged vs released — the distinction is load-bearing.** *(Feedback from a prior update: a highlight said "N new capabilities landed" and a release manager corrected the framing — some of those features were still in regression testing and not officially released. Readers were about to assume features were live when they weren't.)* A merged PR is not the same as a released capability. A release must clear regression testing and go out via the release bot in `#announcements` before it is live to customers. In P&E highlights and the "Shipped this week" language:

- **Use "merged" for PRs that hit `main`/`develop` but have not yet appeared in a `#announcements` release-bot post inside the reporting window.**
- **Use "released" or "shipped to customers" only for PRs that are in a release cut in the window** (verified against the release bot).
- For borderline cases (merged this week, release-in-regression), say "merged this week; in regression testing, not yet live" — never "landed" or "shipped" as a shortcut.
- When highlighting SDK capabilities or customer-facing features, always name the release version they will ship in (or "release TBD if still in regression") so readers know whether the feature is available to them yet.

**Never write a release-cadence interpretation without checking for outages and release-size.** *(Feedback from a prior update: a draft wrote "cadence dropped as engineering absorbed a big push" — wrong. A release manager corrected: an AWS outage had pushed a release back; the prior week's higher release count only shipped fast because those releases were small minor bug fixes; the current week's releases were materially larger and legitimately took longer.)* Release counts are a noisy signal for velocity because they conflate:

1. **Release size** — 3 small bug-fix releases ship faster than 2 feature-heavy releases. Always ask what's *in* the releases before writing a cadence read.
2. **External incidents** — AWS/infra outages, security incidents, and blocked deploys can push a release back independent of engineering capacity. Check `#announcements`, `#phi-incident-*` channels, and the release manager's notes for any release-blocker signal in the window before writing "cadence dropped because X."
3. **Release-in-regression vs release-shipped** — a release cut on Friday that goes to customers Monday is legitimately a release in the reporting week for planning purposes, but not one that customers see this week. Count both, label them separately.

Default framing: report the raw count (`N releases cut, M shipped to customers, K in regression`), then only offer an interpretation if you can rule out the above three. When in doubt, quote the release manager directly rather than paraphrase.

**Anti-patterns to avoid (all seen in earlier drafts and corrected out):**
- Exhaustive `Shipped this week — <repo>` sections that list 15+ PRs each. Fold them into highlights or drop them.
- Test-coverage-only bullets that read as "canvas 71.40% (+0.07%)" with no interpretation. Only include coverage if the number moved materially (>0.5% in a week) or the direction changed.
- "Bot-authored fixes" bullets that name every investigator-app PR. Roll them up as one line ("N investigator-bot fixes shipped this week") only if the count itself matters.
- Long PR-awaiting-review counts unless they are meaningfully up or down. Backlog counts are only useful when the direction is informative.
- Renaming shipped work in vague terms ("platform improvements", "reliability wins"). Every highlight has a specific customer or capability tied to it.

**Total target length for the P&E section: 400–600 words** (excluding the Initiative coverage table). If it's longer, cut highlights.

**When WLM and GitHub disagree.** Publish the GitHub numbers in-line and add a "WLM data-quality note" at the end of the section listing each disagreement (commit counts, misdated capabilities, misidentified authors). Loop in the WLM auto-summary owner so the upstream drift gets fixed instead of hand-corrected every week.

### Sales & Pipeline

**The Weekly Marketing Snapshot is the primary source for this section — pull it FIRST, not last.** The Marketing team publishes a snapshot every Friday in the Notion `Weekly Reports` database with the canonical numbers for: closed-won / closed-lost, new deals created, qualified leads, lead velocity (trailing 4-week bridge), trial activity, source attribution, and named notable prospects. It is refreshed daily and reads from HubSpot + your analytics stack + your instance-tracker automatically — meaning it beats any ad-hoc HubSpot pull you would do for the same window.

**Find and fetch it before writing anything in this section:**

```
notion-search({ query: "Weekly Marketing Snapshot", page_size: 5 })
```

Title pattern: `<Company> Weekly Marketing Snapshot (<Month> <D>, YYYY)`. Take the most recent one whose Report Date is inside or immediately after the reporting window. Parent database: `Weekly Reports` at `collection://<WEEKLY_REPORTS_COLLECTION_ID>` (under Marketing). Its own reporting window is **Fri → Thu** (not Mon → Fri) — quote the snapshot's window explicitly when citing its numbers, and note the offset if it matters.

**Numbers to pull from the Marketing Snapshot into this section:**
1. **New deals created this window** (count, raw $, probability-weighted $) with the named deal list, stage, and target close date.
2. **Closed-won / closed-lost this window** with per-deal ARR, close date, and (for closed-lost) loss reason.
3. **Qualified leads (in-window)** with strict-qualified count, source mix, converted-to-deal count, and the named lead list.
4. **Lead velocity — the trailing 4-week bridge** (do not paraphrase; quote the bridge series so the reader sees the trend, not just a single-week number).
5. **Trial activity — the "clean" row** (users, requests, active trials). *Never* quote the raw row without adjacent clean row — the raw is regularly distorted by test accounts (e.g. `test44@gmail.com` at 22K requests one week).
6. **Named notable prospects with corporate domains** and clinical decision-maker titles — the reader recognizes signal like "Ashley Atkins, CEO, Vale Health" better than "eight qualified leads."
7. **Data hygiene items** the marketing team flagged for cleanup (UPDATE-COMPANY placeholder counts, `delivers_care = Needs Review` counts, source-blank counts).
8. **Plugin activity in the trial fleet** — total installs and any trial-scoped additions this window.
9. **Source health footer** — if any source is degraded, cite it inline so the reader knows a number may be understated.

**If the Marketing Snapshot didn't publish this week** (owner OOO, data pull failed), fall back to the direct HubSpot pull described below AND explicitly note in the section that the snapshot is missing so downstream readers know the numbers are ad-hoc rather than the canonical Marketing view.

Also search Notion for this week's Weekly Update — the Sales & Pipeline section typically has current Walk to Close deals, named accounts, and amounts.

Search Slack for: `"walk to close" OR "closed" OR "signed" OR "new customer" OR "contract"` for live signals.

Do NOT rely solely on the strategy doc for pipeline numbers — it goes stale quickly. Use live Notion/Slack signals for specific deal names and amounts. Strategy doc is useful only for baseline metrics (Q1 actuals, full-year targets).

**Always cross-check the Pipeline Review meeting note against live HubSpot.** The Pipeline Review runs Monday — by Friday, deals have closed Tue–Fri that won't appear in the meeting note. Pull live closed-won and closed-lost for the current month from HubSpot before writing the bullet. Without this step, MTD numbers will be hours-old at best and stale by 4 days at worst.

**Owner-ID resolution is mandatory before writing any name.** *(Feedback from a prior update: the draft attributed a closed-won deal to a fabricated employee name — the assistant took a raw `hubspot_owner_id` from the HubSpot pull, never resolved it to a real name, and spliced a first name seen elsewhere in the meeting notes with a fabricated surname. The CEO caught the hallucination.)* Before naming any AE, closer, or deal owner in the update:

1. **Resolve every `hubspot_owner_id` via `mcp__hubspot__hubspot-get-user-details`** (or grep the last 4 weekly updates for the same owner_id → confirmed name). Do this in the same batch as the deal pull, not after drafting.
2. **Cross-check the resolved name against the org roster** at `~/.claude/skills/chief-org/roster.yaml` and the Canvas Handbook — Company Context Notion page. If the name isn't in either, treat it as unverified and either flag to the user before publishing or use "deal owner unresolved" wording.
3. **A first name in one context is not a full name in another.** A first-name-only reference in a WLM (e.g., "Firstname + Firstname on the HubSpot instrumentation project") does not license writing a full name into an attribution elsewhere. Full-name attributions require the full name to be present verbatim in the source.
4. **Never guess a surname to complete an attribution.** If only a first name is available, use the first name alone ("Payton closed X") or omit the name entirely — never invent a last name.

See [[feedback_never_invent_names_from_hubspot_ids]] for the standing rule; parallels [[feedback_never_guess_notion_authors]] for Notion comment authors.

**HubSpot tool note (filters that actually work):**
- `dealstage = "closedwon"` (the string literal) often returns **zero results** because some HubSpot accounts use numeric stage IDs and the default labels won't match.
- Use `hs_is_closed_won = "true"` for closed-won and `hs_is_closed = "true" AND hs_is_closed_won = "false"` for closed-lost.
- `closedate GTE [first of current month]` for MTD.
- Always include `hs_is_closed_won` and `hs_is_closed` in the `properties` array so you can sort the results yourself rather than relying on stage labels.

```
mcp__hubspot__hubspot-search-objects({
  objectType: "deals",
  filterGroups: [{ filters: [
    { propertyName: "hs_is_closed_won", operator: "EQ", value: "true" },
    { propertyName: "closedate", operator: "GTE", value: "2026-06-01" },
  ]}],
  properties: ["dealname", "amount", "closedate", "dealstage", "hs_is_closed", "hs_is_closed_won", "hubspot_owner_id"],
  sorts: [{ propertyName: "closedate", direction: "DESCENDING" }],
  limit: 50,
})
```

**Extract:** Named deals closed-won this month with amounts. **Closed-lost worth flagging** — any single deal that's a meaningful share of your average month is worth a one-line callout (post-mortem warranted); use your own bar (often anything ≥ 5–10x average deal size). Active pipeline (named Walk to Close deals + amounts + close targets). Strategic opportunities worth flagging. Do not surface board, financing, or fundraising updates.

**Never write "not surfacing in HubSpot yet" without a proper cross-check.** *(Feedback from the 6/29–7/3 update: Cardiostrong MD was flagged as "announced by the bot but not in HubSpot; Ops to reconcile Monday." Adam corrected this — Cardiostrong was already in Pylon AND HubSpot; the failed HubSpot search was a filter/name mismatch, not a missing record.)* Before writing that framing, do all three:
1. Search HubSpot **companies** by domain and by name (not just deals).
2. Look up the customer in **Pylon** (`search_accounts` by name or domain).
3. Query the **Customer Name Reconciliation Map** for aliases.

If the customer is in any of the above, the deal is in the CRM — publish the ARR from the reconciled record and skip the reconcile-Monday framing entirely. Only flag "reconcile needed" if all three come back empty.

**Sales is pre-sale ONLY.** Closed-won deals from prior weeks/months are not "Sales" anymore — they are customers and belong in **Customers & Implementation**. Use the cross-section dedup rule below.

#### New Qualified Leads (standing bullet — required every week)

**Required standing bullet.** Every Sales & Pipeline write-up includes a bullet on **qualified leads created this week that have not yet made it to Deal stage.** This is the pre-deal top-of-funnel signal — leads that are engaged / working / qualified but no deal object has been created for them yet. It closes the loop on the Sales section: closed-won answers "what booked," Q3 forecast answers "what's committed," and this bullet answers "what's next in the funnel."

**Definition of "qualified lead"** (per your workspace convention; example from a HubSpot dashboard report): `hs_lead_status NOT IN ('NEW', 'UNQUALIFIED', 'Bulk Upload')`. Verify the exact list against your HubSpot lead-lifecycle configuration and codify it locally.

**Step 1 — Query leads created this week.** The `leads` object uses `hs_createdate` (not `createdate`). Filtering by `hs_lead_status NOT_IN` sometimes returns a 400 from HubSpot; if it does, pull all leads and filter in-process by `hs_pipeline_stage` — the labeled stages `new-stage-id` and `unqualified-stage-id` map to the two excluded statuses, and any other stage counts as qualified for this purpose.

```
mcp__hubspot__hubspot-search-objects({
  objectType: "leads",
  filterGroups: [{ filters: [
    { propertyName: "hs_createdate", operator: "GTE", value: "<MON-of-reporting-week>" }
  ]}],
  properties: ["hs_lead_name", "hs_lead_status", "hs_createdate", "hs_pipeline_stage", "hs_lead_type", "hubspot_owner_id"],
  sorts: [{ propertyName: "hs_createdate", direction: "DESCENDING" }],
  limit: 100,
})
```

**Step 2 — Identify leads that don't yet have a deal.** Cross-reference the lead list against the deals created this week (from the Sales section's HubSpot pull). A lead has "made it to Deal stage" if a deal object exists with the same company / contact — the fastest way to spot this is to match on `hs_lead_name` against `dealname` in the current-week deal list. Leads whose company name doesn't appear in any Q3'26-open or closed-this-week deal are the ones to include.

**Step 3 — Filter out Zapier-generated noise.** The Zapier integration (HubSpot integration ID 25200, per reference memory) creates "UPDATE COMPANY <name>" duplicate leads on every property change to an existing contact. Skip anything whose `hs_lead_name` starts with "UPDATE COMPANY" — unless it's the *only* lead entry for that company in the window, in which case it's the substantive record.

**Step 4 — Group by pipeline stage** so the reader can distinguish "close to being a deal" from "just entering the working queue":

- **Higher-stage qualified** (past initial working queue — typically `hs_pipeline_stage` = qualified-stage-id or a mid-funnel numeric stage): named list with dates.
- **Working queue** (early qualified, still being engaged — typically the earliest numeric pipeline stage): named list with dates. If the volume is dominated by one owner (typical when one AE is handling inbound), name the owner.

**Do not report on outbound if your business is inbound-led.** A `sales_outbound` count of zero is the expected state, not a finding, so never write it as a miss, a trend, or a data-quality item. Report the source mix only across the channels that actually drive your funnel, and drop the outbound row entirely rather than showing it at zero.

**Step 5 — Add a one-line read.** Was the funnel healthy this week (net-new inbound flowing in, some already converting)? Is there a bottleneck (leads arriving but nothing progressing)? Cross-reference against last week's list — if the same names keep appearing in the working queue without moving, that's a signal.

**Format the bullet:**

```
- **New qualified leads this week: N net-new qualified leads created that have not yet made it to Deal stage.** [Owner note if concentrated in one AE's book.] HubSpot-verified against `hs_lead_status NOT IN NEW / UNQUALIFIED / Bulk Upload`, created <MON> → <FRI>, no associated deal object yet.
  - **Higher-stage qualified (N):** Company (date), Company (date), ...
  - **Working queue (N):** Company (date), Company (date), ...
  - **Read:** [one-line assessment of top-of-funnel health this week; cross-reference conversion cycle if visible]
```

**Additional note when applicable.** If some leads landed at a deal-ready stage this week AND already have deals in the pipeline, mention this separately as a positive signal on lead-to-deal cycle speed (e.g. "3 leads landed deal-ready this week and already have deals in Q3 pipeline: X, Y, Z — cycle running same-day-to-3-days"). This is *not* the main bullet content — the main content is qualified leads *without* deals yet.

#### Forward-Looking Forecast (from the Weekly Pipeline Dashboard)

**Required standing subsection.** Every Sales & Pipeline write-up ends with a forward-looking quarterly forecast pulled from the Weekly Pipeline Dashboard Google Sheet (`<PIPELINE_DASHBOARD_SHEET_ID>`). The purpose is to close the loop on "what's already booked" with "what's realistically coming" — pipeline is stale by Friday if you only cite the Monday Pipeline Review.

**Step 1 — Read the sheet's structure.** The dashboard typically has these tabs (name may vary):

- `Pipeline Dashboard (Quarter)` — headline stage-weighted forecast, filtered by a "Select Quarter" cell (usually `C3`). This tab is dynamic — it reflects whatever quarter is currently selected.
- `Deal Details` — deal-level open + closed rows with owner, stage, forecasted close quarter, ARR, and weighted ARR. Also filtered by the quarter picker for the summary but usually contains historical + all future close-dates in the raw rows.
- `Hubspot_Data` — raw HubSpot export with columns including `Close Quarter`, `Deal Weighting`, `Weighted ARR`, `Company name`, `Deal Name`, `Deal Stage`, `Amount`, `Close Date`, `Deal owner`. This is the safest source for a quarter-specific pull because it isn't affected by the picker.

Confirm tab structure once per skill run:

```bash
gws sheets spreadsheets get --params '{"spreadsheetId": "<PIPELINE_DASHBOARD_SHEET_ID>", "fields": "properties.title,sheets.properties(title,sheetId,gridProperties(rowCount,columnCount))"}'
```

**Step 2 — Pull the deal-level rows for the target forecast quarter.** The target is normally the **next full quarter** — e.g. an early-July update covers Q3 open pipeline. Read `Deal Details` (or `Hubspot_Data` as backup) and filter to rows where the forecasted close quarter matches the target (e.g. `Q3'26`).

```bash
gws sheets +read --spreadsheet <PIPELINE_DASHBOARD_SHEET_ID> --range "Deal Details!A1:K600" --format json
```

Then in-process, filter rows where any cell contains the target quarter literal (e.g. `Q3'26`) and the stage is one of: `New Opportunity`, `Discovery`, `Post-Demo Activation`, `Engaged`, `Qualified Evaluation`, `Walk to Close`. Exclude `Closed won` and `Closed lost`.

**Step 3 — Group and summarize by stage.** For each stage bucket, compute (a) deal count, (b) sum of unweighted ARR, (c) sum of weighted ARR. Also identify the top 1–3 named deals in each bucket by unweighted ARR — these are the levers.

**Step 4 — Compare to target.** The `Pipeline Dashboard (Quarter)` tab has a "Quarter Target" cell (typically near `J7`). If the picker matches the target quarter, read it directly. Otherwise use the most-recent published target (last quarter's target is a reasonable default until Finance sets the new one — flag that if you fall back).

**Step 5 — Frame base case vs upside.** Explicitly separate:

- **Base case:** Walk to Close + Qualified Evaluation weighted ARR, plus expected new-inbound Start/Builder throughput at the trailing 3-month monthly rate. This is what the team should be planning against.
- **Upside:** Engaged and earlier-stage large deals (typically $500K+ ARR). These have real optionality but a low probability weight; do not count them as base case even if they'd close the target gap on their own.

**Step 6 — Format the subsection.** Use this shape:

```
- **[Next quarter] pipeline: ~$X.XM open ARR across N deals, weighted forecast ~$X.XM against a target of ~$X.XM** (source: [Weekly Pipeline Dashboard](<sheet URL>), <snapshot date>).
  - **Walk to Close — N deals / $X.XM unweighted / $X.XM weighted.** Led by [Top1 ($amount, weight%)] and [Top2 ($amount, weight%)], plus [smaller deals summarized].
  - **Engaged — N deals / $X.XM unweighted / $X.XM weighted.** [Top anchors named].
  - **Qualified Evaluation — N deals / $X.XM unweighted / $X.XM weighted.** [Anchor named].
  - **Earlier-stage — N deals / ~$X.XM unweighted.** [Notable large names in Post-Demo Activation, Discovery, New Opportunity].
  - **Forecast read.** [Base case narrative: which deals + throughput get us to target]. [Upside deals named as upside, not base case.]
```

**Rules for this subsection:**
- **Always cite the snapshot date and link the source sheet.** Pipeline data goes stale daily.
- **Never conflate weighted with unweighted.** Report both for every stage bucket.
- **Never rely on the "Select Quarter" picker for the target quarter's numbers if the picker is set to a different quarter** — use `Hubspot_Data` or `Deal Details` raw rows filtered in-process instead.
- **Flag it explicitly when the target is stale** (e.g. still holding last quarter's target). Don't paper over the gap.
- **Do not name individual deal owners** in this subsection — attribution belongs in the closed-won list above, not in the forward-look.

### Customer operations

**One combined section for the entire customer book — no separate Customers & Implementation and Support sections.** Structure it as three subsections in order: `Customer base at a glance`, `Customer milestones (progress this week)`, and `Risk items`.

**Do NOT source risk items from WLM or the Support Working Session meeting note.** Those meetings surface leadership-recommended risks that are already known and typically re-litigated week over week. The purpose of this section is to surface *this week's live signal* — Pylon P0/P1 tickets opened in the window and Slack activity in #announcements + #team-engineering + relevant customer channels. WLM and the Support session are still worth reading (for context and to double-check nothing is missing), but the section is written from Pylon and Slack as source, not from those meeting notes.

**No standalone Support section.** The support-KPI signal that used to live in a dedicated Support section (P0 count trend, resolution time, top accounts by volume) is now folded into `Customer milestones` when it's genuinely a milestone (P0 count halved, backlog cleared, resolution time improved), or into `Risk items` when it's a live risk (a customer's ticket count is spiking, a KOALA escalation is stalled). Numbers-only dumps of the Support Working Session table are out.

#### Customer base at a glance

Segment the book into **Live** vs **Pre Go-Live** using the Canvas KPIs sheet (`<KPI_SHEET_ID>`):

- **Live** = customer had MAPs > 0 in the prior month on the `G7 - MAPs per Customer` tab. Prior month = latest closed month per the sheet's `Combined Summary` tab (e.g., a Friday-in-July update uses June).
- **Pre Go-Live** = G7 `Status` column = `Implementation` AND no MAPs in the prior month. This EXCLUDES dormant customers with old (2022–2024) go-live dates and no June MAPs — those are neither Live nor actively implementing and should not be counted in either bucket.
- **Not counted here:** anything G7 marks `Churned`, plus rows that are aggregate labels or partial data (Total, % Growth, Segment names like "Startup" / "Enterprise" / "SMB").

For each segment, cross-join to Pylon `implementation_status` via the **Customer Name Reconciliation Map** — do NOT do fuzzy name matching:

- The Notion database is at `<CUSTOMER_RECON_DB_URL>` with data-source ID `<CUSTOMER_RECON_DATA_SOURCE_ID>` (`collection://<uuid>`).
- Query it with `notion-query-data-sources` (SQL mode). Schema includes `Brand name`, `Legal entity`, `Aliases` (semicolon-separated), `Pylon ID`, `Domain`, `Confidence`.
- Build a lookup keyed by normalized legal entity / brand / alias → Pylon ID. Then look up each G7 customer name in that map.
- **Do not fall back to fuzzy substring matching against Pylon's search results.** Substring matches ("Health" appears in half the customer base) create false positives and quietly distort the counts. If a customer doesn't reconcile, count it under `Not mapped` and move on — 5–10 unmapped in a book of ~120 is expected (small/early customers not yet added to the recon DB; new signings this week; label rows that slipped past the filter).
- After the tally, look at the `Not mapped` list. If any are recognizable *real* customers (not label rows), flag them in a one-line note under the table so `/chief-reconcile` can add them next run.

Render as a single table:

```
| Segment | Total | 🟢 On Track / Complete | 🟡 At Risk | 🔴 Off Track / Stalled | Not mapped |
| --- | --- | --- | --- | --- | --- |
| **Live** (had prior-month MAPs) | N | X | Y | Z | W |
| **Pre Go-Live** (Implementation, no MAPs) | N | X | Y | Z | W |
| **Total active book** | N | X | Y | Z | W |
```

Below the table, add **one line** on Live-book MAPs concentration: top 5–10 Live customers by prior-month MAPs, plus the total MAPs figure and MoM growth % from `Combined Summary`. This anchors the reader in where the run-rate business actually lives.

**Cite sources**: link the KPI sheet URL and the reconciliation DB URL right in the intro sentence. If reconciliation gaps meaningfully affect a bucket count (e.g. a whole segment has >15% unmapped), say so.

#### Customer milestones (progress this week)

**Positive signal only.** This is what actually improved during the Mon → Fri reporting window. Prioritize things that would matter to a reader who was OOO all week: closed-won signings, go-lives, customer-facing plugin/feature landings that got customer response, meaningful turnaround narratives, and support KPI improvements (P0 count halved, backlog cleared, resolution time down).

Rules:
- **Everything must be dated inside the window.** A go-live from last week is not this week's milestone; call it out only if it hit a 7/14/30-day post-golive stability threshold this week (e.g., "[Customer] past first-week stabilization" is fine on the ~11-day mark).
- **When there are no new signings or go-lives in-window, say so explicitly and list the next-30-days go-live sequence** so the reader knows what's coming.
- **Customer-shipped plugins to production** are the highest-signal milestone type — surface them by name if any landed this week.
- **Support KPI wins** (P0 count halved, resolution-time improved, backlog cleared) go here, not in a separate Support section.
- **Cross-reference GitHub merges to customer channels**: if a fix or feature merged this week landed in a customer's Pylon or Slack channel with a positive reaction, quote them briefly ("customer opened a ticket titled 'Lab requisition form excitement'…").

#### Risk items

Sourced live from this week's context — **not** from WLM or Support Session meeting notes. Pull:

1. **Pylon P0 tickets opened in the window** (`validated:p0-urgent` tag or explicit P0 language in title). Paginate `mcp__pylon__search_issues({ created_after, created_before, limit: 100 })` until the window is fully retrieved. Group by account. For every account with any open P0, name it, name the P0 titles, and mark whether it's still open or was closed same-day. Note the IM.
2. **Pylon P1 tickets** (`validated:p1-high`) for the same window. Include only the ones that are still open at report time or that pattern with prior weeks (a customer with a recurring P1 shape).
3. **Slack signal from #announcements, #team-engineering, and customer channels** — look for the language of concern this week: "blocker", "urgent", "critical", "on_hold", "waiting on", "still open", "regression". Also look for engineers flagging PRs "as a [customer] concern" or CI/action failures affecting a specific customer.
4. **Bulk enrollment/volume waves** — batches of 20+ same-shape tickets that don't have severity but strain resolution capacity. Name the customer and the batch date.
5. **Silence risks** — customers where IM has flagged in Slack or the customer channel that they see signals *not visible in Pylon*. These are the hardest to detect algorithmically; watch specifically for phrases like "I'm concerned about X but no tickets have been opened" or "quiet worries me."
**Never build the pre-go-live list from the usage sheet alone — reconcile it against actual go-lives first.** The usage sheet's latest closed month is always at least a month stale, so "zero usage last month" and "has not gone live" are different statements for the whole first half of any month. Before publishing:

1. **Get the actual go-live list for the current month**, defined as customers with their first genuine active patient on a production instance. Do not rely on a CRM `days_until_golive` field, which counts down to a *planned* date and stays negative long after a successful cutover.
2. **Subtract every current-month go-live from the Pre Go-Live bucket** before counting or naming anyone.
3. **Implementation status lags a cutover by days to weeks.** An account can be live and still flagged At Risk. When status and reality disagree, reality wins, and the stale flag becomes a note asking for a re-grade rather than a risk item.
4. **Cross-check the bucket against your own Customer milestones section.** A customer appearing as a go-live in one section and pre-go-live in another means the update is wrong and a reader will catch it.
5. **Read the sentiment field before characterizing any account.**

**A go-live that lands late is a win, not a slip — write it that way.** Once a customer is actually live, the earlier slippage stops being the story and the delivery becomes it. Lead with what was delivered and who delivered it, name the engineers, and mention the prior risk framing only as distance travelled. Never lead a live customer with days-past-target, with a zero-usage count that only reflects patients not having arrived yet, or with an outstanding item from the original plan.

6. **Pre-go-live sequence next 30 days** — list customers with go-live dates in the upcoming 4 weeks, with their days-out and Pylon `implementation_status`. This is where the H1 churn pattern kept surfacing; explicit visibility here helps.

Filter spam from ticket counts: tags `🗑️ Spam Email`, `spam`, and email-sourced issues with no `account_id` do not count.

**Never surface a historical IM on a graduated account.** *(Feedback from a prior update: a shoutout named someone as IM for three accounts, but two of those three were `implementation_status: 🔵 Complete` and the named person hadn't been their IM since graduation. Historical IM had leaked into a current-state attribution.)* Operating model: an Implementation Manager owns a customer *until graduation*, at which point Support takes over and there is no IM. The Pylon `implementation_lead` field retains the historical IM's name after graduation, so it is **not** a current-state signal.

Before writing "IM: <name>" anywhere in the update, check `implementation_status` on the Pylon account:

- **`🔵 Complete` → graduated.** Do NOT write "IM: <name>". Write "Graduated account, Support-owned" or omit ownership entirely. The Pylon `owner` on a graduated account is the Account Owner (person receiving Support-queue tickets), not the IM.
- **`🟢 On Track` / `🟡 At Risk` / `🔴 Off Track / Stalled` → active implementation.** `implementation_lead` is current-state — IM attribution is fine.

**Never batch-attribute across multiple accounts without individually checking each one's `implementation_status`.** Writing "held IM for X + Y + Z" is only correct if all of X, Y, Z are active-implementation. The 7/27–31 batch phrasing masked the graduation state of two of three accounts.

**For heavy-portfolio owners (a senior account owner holding many graduated accounts, etc.), frame the work accurately:** "holding X graduated accounts as owner during a hot week" — not "IM for X At-Risk accounts." Owning a Support-owned portfolio through a hot week is different work than actively managing implementations, and the language should reflect it.

See [[feedback_graduated_customers_have_no_im]] for the standing rule.

**Reconcile customer names against the Customer Name Reconciliation Map BEFORE attributing a customer channel or ticket to an aggregator's portfolio.** *(Feedback from a prior update: a sub-brand customer channel was mislabeled under one aggregator when it actually belonged to a different aggregator's sub-brand portfolio.)* When a customer name looks brand-adjacent to a known aggregator in your book, query the Reconciliation DB first with `mcp__notion__notion-query-data-sources` — do NOT substring-match against the most obvious aggregator. Aggregators overlap in shape (portfolios of sub-brands), so misattribution creates false blame lines. If a Pylon account's `instance_slugs` field includes the sub-brand slug under the aggregator's console-org listing, that is the ground truth.

**Recalibrate sentiment from customer-leader tone, not just Pylon's `sentiment` field.** *(Feedback from a prior update: leadership flagged that sentiment analysis for an aggregator customer needed recalibration based on the founder's tone in DMs, not just the Pylon sentiment field.)* The Pylon `sentiment` value is set by IMs and can lag reality — especially for **aggregators** where the founder/CEO writes directly to the CEO or a senior account owner in DMs and Slack channels rather than through tickets. For every customer flagged 🟡 or 🔴 (or every aggregator flagged anything), scan the customer's primary Slack channel and any DMs the founder has sent this week for tone-shifting language ("concerned", "unacceptable", "considering options", "not what I expected") and let the founder tone override Pylon when they disagree. Cite the specific message and speaker inline.

**Surface recovery signals when a team member has stepped in.** *(Feedback from a prior update: leadership flagged that a 🔴 account was showing recovery signal because a Support staffer had stepped in, and the update hadn't noted it.)* For any customer flagged 🔴 or "Frustrated" this week, cross-check whether an IM, Support staffer, or engineer stepped in during the reporting window. If so, add a "**Recovery signal**" one-liner immediately after the 🔴 status line naming who stepped in and what improved. A customer can be both 🔴 AND recovering — the update must carry both, not just the risk.

**⏸ Not-yet-confirmed churn.** Meeting notes often say "we will recommend that [customer] transition to [competitor]" — that is **internal posture, not a confirmed customer decision.** Do not write the customer as churning or offboarding unless there is direct evidence the customer agreed (signed offboarding plan, executed termination, departure confirmed in writing). Frame the recommendation as "[Your company] exploring recommendation that [customer] transition to [alternative]" until confirmed externally.

**Cross-section dedup pass (required before publishing).** After drafting Sales & Pipeline and Customer operations, do a single pass: for every customer named, ensure they appear in exactly one section. If a customer shows up in both, delete the Sales entry and consolidate detail into Customer operations. The exception is brand-new closed-won deals from this week, which can be named once in the Sales closed-won list AND once in Customer operations if there's an implementation milestone to report — but never duplicate narrative.

**Common drift to catch (belongs in Customer operations, not Sales):**
- Customer-specific feature rollout dates (e.g. "[Customer A]'s AI feature live by [date]").
- Commercial-relationship work with an existing customer (e.g. existing customer's third-party-integration trial, data-exchange / interoperability work).
- Partner relationships (vendors, channel partners, contractor orgs shipping plugins) — surface those in Sales under a "Partnership note" sub-bullet, not in Customer operations.

### Open source plugins — retired section

An open-source plugin scorecard is no longer a section of this update and is no longer a required source. Do not search for it, do not report on whether it ran, and do not flag a missing report as a data-quality gap. Plugin counts and per-builder target tracking are not what a company needs from a weekly update, and a scorecard that ranks named builders has the same defect as a commit-count table.

Plugin activity still belongs in the update when it is customer-visible. Route it through the ordinary channels: a plugin that shipped to a named customer's production instance is a **Customer milestone**, a plugin capability that unlocks other people's work is a **P&E highlight**, and trial-fleet plugin rollouts come from the Weekly Marketing Snapshot's own plugin-activity block inside **Sales & Pipeline**.

### Company on LinkedIn This Week

A standing section. The marketing lead posts a Friday roundup in #announcements listing company-authored LinkedIn content from the week so the team can like / comment / reshare and help boost reach.

**Source:** Slack search for the marketing lead's Friday post in `#announcements`:

```
mcp__plugin_slack_slack__slack_search_public({
  query: 'from:<@<MARKETING_LEAD_SLACK_USER_ID>> "LinkedIn this week" in:announcements after:<monday>',
  limit: 5,
})
```

Fallback queries if the canonical title changes: `"LinkedIn this week" in:announcements`, or `"Friday roundup" from:<@<MARKETING_LEAD_SLACK_USER_ID>>`.

**Extract:** The list of named contributors and their LinkedIn post URLs. Preserve the exact post URLs from the marketing lead's message — do not rewrite or shorten them. Author name + one-line topic from each bullet (e.g. "[CEO] — [headline of their post]").

**Format in the update:** A standalone section between Shoutouts and OOO Next Week. One bullet per post with the author bolded and the title hyperlinked. Lead the section with a one-line note that reshares from your own network travel furthest.

If the marketing lead didn't post a roundup this week (OOO, no posts to highlight, etc.), skip the section entirely. Do not invent a roundup or scrape LinkedIn directly — the skill depends on a curated list.

### Shoutouts

**Do not let this section drift into a P&E release-notes summary.** *(Feedback from the 7/27–31 update: the first draft's Shoutouts read as "13 named engineers who shipped PRs" and buried the customer-facing IMs, the sales closers, the marketing lead, and the internal-team culture moments. Rewrite triggered by Adam.)* Shoutouts must cover **five distinct lanes**, in this display order — a WLM-only or GitHub-only pull will always over-index on engineering. Use subheaders to make the coverage legible:

1. **Cross-functional & customer-facing** — IMs shipping go-lives, IMs holding down multiple risk accounts through OOO coverage, Support staff carrying operational scale-ups, engineers going into customer calls as domain experts. This is the top lane. Every 🟡/🔴 account with a Recovery signal (see Risk items) has a name attached — surface that name here.
2. **Sales & Marketing** — every closed-won this week gets a named closer (AE + sales lead). Every sizeable closed-lost worth flagging gets its post-mortem author named. Marketing motions launched this window (specialty spotlights, campaigns, funnel-report improvements) get the marketing lead named. Lead-funnel acceleration (the trailing 4-week bridge from the Marketing Snapshot) belongs here as a team-wide win, not buried in Sales & Pipeline.
3. **Studio + Onboarding Agent** — when this team is dominating the week's throughput, **name individual contributors, do not lump them into a "team" bullet**. A prior update collapsed three engineers into one "team" bullet and the CEO explicitly asked to split them out. Each engineer owning a distinct initiative gets their own line with the specific tickets they shipped.
4. **Product & Engineering** — the rest of the P&E lane (canvas, canvas-plugins, canvas-agents, canvas-hyperscribe). Real names, specific PRs, cross-repo work called out.
5. **Internal team & grace** — moments of team culture worth naming: someone stopping to praise a colleague publicly, a departing team member doing careful handoff work, a cross-team save that could easily have gone uncredited. These are the highest-signal / lowest-frequency shoutouts and the ones the update should protect space for.

**Cross-lane rule.** When one person shows up meaningfully in two lanes (e.g., an engineer shipping code AND acting as IM for a customer through a hot P0 week), name them in *both* lanes with clear labels ("P&E lane" / "Customer-facing lane") — do not choose one. Different readers care about different halves of the same week.

The WLM is the **starting point**, not the only source. The richer shoutouts come from triangulating across WLM + Slack + customer channels + Pylon customer-thank-yous + the Weekly Marketing Snapshot. Pull from all of these, dedupe, and lean toward specific named contributions over generic team thanks.

**Sources to combine:**

1. **WLM (Weekly Leadership Meeting) meeting note** from the current week. Query the Meetings database for `Subtype = "WLM"` on Monday–Tuesday of the current week, then fetch the page. Do not use `notion-search` — it surfaces prior weeks. If the WLM has an explicit Shoutouts section, take it verbatim. If not, extract celebrations from the content: go-lives, at-risk accounts that moved to on-track, individuals called out by name for stepping up, notable completions.
2. **Slack #announcements** (`in:announcements after:<monday>`) — look for explicit shoutouts, public wins, customer wins, big launches. Capture the giver and recipient by name.
3. **Slack search**: `shoutout OR kudos OR "huge thanks" OR "great job" OR "amazing work" OR "love this" OR "killing it"` across the workspace for the week. Often the best shoutouts happen in non-announcement channels.
4. **Customer support channels via Pylon** — search Pylon for issues created in the window with titles like "Appreciation", "Thank you", "Positive feedback" (`mcp__pylon__search_issues`). When a customer-side leader (CEO, VP, founder) sends an unprompted thank-you mid-implementation, that is a strong signal worth surfacing. Resolve the account and the named requester so you can credit the customer person too (e.g. "[Senior leader role] at [Customer A] sent...").
5. **Plugin Scorecard** — call out external open-source contributors who merged plugins (contractor orgs, community PRs). They don't roll up under team targets but they still shipped customer-impacting work.
6. **Customer-built plugins shipped to production** — when a non-engineer customer ships a self-built plugin to their production instance, that is a tier-1 shoutout (both the customer and the internal person who unblocked them).
7. **Work-anniversaries** — pull from the shared team calendar (see "OOO Next Week" below). If a work-anniversary falls in the **current reporting week** (Mon–Fri of this update), include it as a warm callout in Shoutouts — name the person, year count, and one line on what they've meant to the company. Work-anniversaries in the **upcoming week** go in OOO Next Week as a "Notable" line, not Shoutouts.

**Extract:** Verbatim or close-paraphrase shoutouts. Keep this section warm and specific — use real names and say what they did. Lead with the highest-signal item (first customer-shipped production plugin, named customer-side leader thanking us, first-time accomplishment), not the longest list of generic thanks.

### OOO Next Week

A required section at the end of the weekly update. **Data only — no commentary.**

**Source of truth:** the **Canvas Shared Calendar** (Google Calendar). *(Feedback from a prior update: the first-draft OOO table was materially incomplete; a team member rewrote it manually and noted that it was missing a lot of entries from the shared calendar. The `gws calendar +agenda` pull ran but the parser surfaced only a subset.)* The Canvas Shared Calendar is the authoritative team OOO record — every OOO entry there must appear in the table.

**Pull instructions (must all run):**

```bash
gws calendar +agenda --days 8 --calendar "Canvas Shared Calendar" --format json
```

Then, as a completeness check, also pull individual attendee calendars for anyone on the leadership team roster:

```bash
gws calendar +agenda --days 8 --format json
```

Merge both sources and **enumerate every OOO-shaped event** in the window. OOO-shaped means the event title matches any of: `OOO`, `Out of office`, `OoO`, `PTO`, `Vacation`, `Home`, `Office (Home)`, `Sick`, or a company holiday name. Also match personal-calendar full-day events where the `summary` is just a person's first name or `<Name> OOO`.

**Completeness rule (mandatory):** After building the table, cross-check it against the raw JSON to make sure no OOO-shaped event was dropped by the parser. If the raw JSON has more OOO events than made it into the table, the parser is under-surfacing — go back and add the missing ones. The reference for what "complete" looks like: for a mid-summer week roughly 15 distinct name-day entries across 5 days is normal for a ~30-person team, not 4. If the raw JSON has more OOO events than made it into the table, the parser is under-surfacing — add the missing ones.

**Format as a table only. Do not add commentary, coverage-gap analysis, escalation routing, or "steps to take" notes.** The reader can see the table and make their own judgments.

| Date | Who |
|---|---|
| Mon M/D | Person A, Person B |
| ... | ... |

Allowed below the table: a single line flagging a company holiday inside the window (e.g. "Fri 7/3 — Independence Day, Canvas Holiday") if it isn't already obvious from the table. Nothing else. No "coverage flags," no "escalation paths," no "treat X as low-velocity day," no "PR review timing" notes. If a coverage risk genuinely needs flagging, surface it in Customers & Implementation or Support — not here.

This section is short by design. Don't list every personal calendar event — just OOO from the shared team calendar.

## Output Format

Keep it skimmable. No icons, no stylization. Plain structure.

```
# Weekly Update — [Mon date – Fri date, YYYY]

## What Matters This Week
[2-3 bullets. Specific milestones, imminent go-lives, pipeline deadlines. No board/financing/CEO framing.]
[Plus one bullet with the Plugin Scorecard headline numbers + standout plugins from this week. Skip this bullet if 0 plugins shipped.]

## One Thing You Should Know
[The single issue with the highest leadership engagement this week. Should connect to What Matters.]

---

## Product & Engineering
**Shipped:** [Named releases, specific features — version numbers and feature names]
**In Progress:** [What's actively being built and why it matters]
**Notes:** [Incidents, reliability events, infrastructure watch items]

## Sales & Pipeline
[**HubSpot-verified** MTD closed-won (names + amounts + dates), closed-lost worth flagging (post-mortem-level deals), named Walk to Close deals with amounts and close targets, partnership notes. Quarter progress vs. target. Pre-sale only — existing customers go to Customers & Implementation.]
[**New qualified leads** (required standing bullet): count of net-new qualified leads created this week that don't yet have a deal object, grouped by higher-stage-qualified vs working queue, with a one-line read on top-of-funnel health.]
[**Forward-looking forecast** (required): next-quarter open pipeline from the Weekly Pipeline Dashboard sheet, broken down by stage with weighted ARR and top named deals. Explicit base-case vs upside framing.]

## Customer operations
### Customer base at a glance
[Segmentation from the KPI sheet. Table: Live (had prior-month MAPs) vs Pre Go-Live (Implementation, no MAPs) vs Total active book — count by 🟢 On Track / Complete, 🟡 At Risk, 🔴 Off Track / Stalled, Not mapped. Status joined via the Customer Name Reconciliation DB (legal-entity → Pylon ID). One-line Live-book MAPs concentration + total MAPs + MoM growth below the table.]
### Customer milestones (progress this week)
[Positive-signal only, dated inside the window. New signings, go-lives, customer-facing plugin/feature landings with customer response, meaningful turnarounds, support KPI wins (P0 halved, backlog cleared). If no signings/go-lives in-window, say so explicitly and list next-30-days go-live sequence.]
### Risk items
[Sourced live from Pylon P0/P1 tickets opened in the window + Slack activity in #announcements, #team-engineering, customer channels. No WLM extrapolation. Group by account. Include silence risks (customers where IM sees signal not in Pylon) and pre-go-live sequence next 30 days. ⏸ block for not-yet-confirmed churn.]

## Shoutouts
[From WLM + Slack #announcements + Slack workspace search + Pylon customer-thank-yous + Plugin Scorecard external contributors + work-anniversaries. Real names, specific contributions, customer leaders included when they thanked us.]

## Company on LinkedIn This Week
[Standing section sourced from the marketing lead's Friday LinkedIn roundup in #announcements. One bullet per post — author bolded, title hyperlinked to the LinkedIn URL preserved exactly from the curated message. Lead with one line noting reshares from your own network travel furthest. Skip the section entirely if there's no roundup this week.]

## OOO Next Week (Mon M/D – Fri M/D)
[Small table of OOO from the shared team calendar. Data only — no commentary, coverage-gap analysis, or escalation routing notes. A single line below the table is allowed only to flag a company holiday inside the window.]
```

## Publishing

Publishing is a **two-step flow**. Step 1 (Notion) runs automatically once the draft is ready — do NOT wait for approval to create the Notion page. Step 2 (Slack) is gated and requires an explicit approval from the user before posting. Never post to Slack before the Notion page has been created, and never auto-proceed from Notion to Slack.

### Step 1 — Create the Notion page (auto-publish, no approval needed)

After you draft the update inline, **immediately create the Notion page in the same response.** Do not ask the user for approval to publish to Notion — the Notion page is the canonical artifact for review. Present the inline draft and create the page in the same turn.

Parent page: `<WEEKLY_PRIORITIES_PARENT_PAGE_ID>`

```
notion-create-pages({
  parent: { type: "page_id", page_id: "<WEEKLY_PRIORITIES_PARENT_PAGE_ID>" },
  pages: [{ properties: { title: "Weekly Update — [Mon date–Fri date, YYYY]" }, content: "..." }]
})
```

Use the full update content as-is (Notion markdown). Do not include the title in the content body.

After creating the page, construct the canonical workspace URL — the Notion MCP only returns raw UUID URLs, which trigger Slack's "untrusted link" warning. Build the URL manually:

```
https://www.notion.so/<WORKSPACE_SLUG>/Weekly-Update-[Mon-Fri-YYYY]-[page-id-no-dashes]
```

Example: `https://www.notion.so/<WORKSPACE_SLUG>/Weekly-Update-April-13-17-2026-<page-id-no-dashes>`

The page ID comes from the `notion-create-pages` response. Strip the dashes from the UUID.

**After creating the page:** Share the canonical URL with the user and explicitly ask them to review in Notion. State that you will not post to Slack until they give an approval. Wait for it. Do not auto-proceed to Step 2.

### Step 2 — Post to Slack (draft-first, requires explicit approval before drafting)

Only run this step after the user has reviewed the Notion page AND given a clear approval to post to Slack ("post to slack", "send the slack", "ship the slack post", "looks good — slack it", or similar). "Looks good" alone after Notion is ambiguous — confirm before drafting.

If the user requests edits after reviewing Notion, update the Notion page first (`notion-update-page`), then re-confirm before drafting to Slack.

**Always use `slack_send_message_draft`, not `slack_send_message`.** *(Feedback from the 7/27–31 update: the initial post went via `slack_send_message`, which sends the message as the user through the MCP integration. Slack does NOT trigger `@channel` push notifications for messages sent via API/bot integrations — the `<!channel>` renders as literal text but the workspace-side notification gate blocks the ping. The draft path avoids this entirely because the user sends the final message from their own client, which triggers the notification.)* Never use `slack_send_message` for the weekly update — the whole point of the message is to page the team, and the direct-send path silently doesn't do that.

The flow:
1. Create the draft with `slack_send_message_draft` in `<ANNOUNCEMENTS_CHANNEL_ID>`.
2. Return the draft link to the user with a clear "send from your Slack client so `@channel` fires" instruction.
3. If a prior `slack_send_message` attempt already went out (recovery scenario), tell the user to delete that message from their client before sending the draft, so there's no duplicate.

Channel: `<ANNOUNCEMENTS_CHANNEL_ID>`

Post a brief announcement that links to the Notion page — do NOT paste the full update into Slack. 2–3 sentences max: what week it covers, the link, and one sentence with the 2–3 biggest things from the week.

**Always lead with `<!channel>`** so everyone receives the alert. The weekly update is one of the few things that genuinely warrants a channel-wide ping. (The user sending from their own client is what makes this trigger — see draft-first rule above.)

Example format:
```
<!channel>
Weekly Update is up for [date range]: [Notion page URL]

[One sentence hitting the 2-3 most important things — a go-live, closed deals, a key risk.]
```

Slack formatting rules:
- Plain text only — no bold, no bullets, no markdown
- Do NOT use `---` horizontal rules
- Do NOT use special unicode characters (em dashes, arrows)
- Always include `<!channel>` on its own line at the top

## Rules

- Use specific names, numbers, and dates. "Strong pipeline" means nothing. "$492K in Walk to Close across 10 deals" is useful.
- The existing weekly Notion update is the primary source of truth for live data — the strategy doc is the baseline for targets and actuals only.
- Never mention board meetings, financing, fundraising, or investor updates.
- Never frame content as CEO priorities. Frame as company priorities.
- Per-customer updates must be narratives, not lists. If you don't have specifics for a customer, skip them.
- If a search returns nothing useful for a section, say so briefly and move on.
- Do not stylize the output — no icons, no emoji, no callout boxes. Plain headers and bullets only.
- Keep each section focused: employees should be able to read this in 3-5 minutes.
- Don't include information only one person would care about — every bullet should matter to at least one full team.
- **Do not blame individual OOO for missing data.** Process gaps (empty meeting metrics, missing scorecards, unfilled tables) have named DRIs; the pipeline is independent of any one person being out. If a working-session table is unpopulated, pull the data from the system of record (Pylon, Plugin Scorecard, etc.) yourself and add a one-line process note naming the DRI without blame so the gap doesn't recur. Only attribute a gap to OOO if you have direct evidence the named DRI was out and there is no backup.
- **Reporting window framing**: write the window as "Reporting window: Mon YYYY-MM-DD — Fri YYYY-MM-DD" without referencing anyone's OOO in the header. Anyone's OOO is a coverage detail, not a framing detail.
