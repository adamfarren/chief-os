---
name: company-update
description: Get a comprehensive view of how the company is performing across all teams — product, engineering, revenue, customers, and ops. Use when you want to understand what's happening company-wide this week or quarter, where we stand on goals, key wins, and areas to watch. Searches Slack, Notion, and the strategy document. Good for staying informed without being in every meeting.
argument-hint: "[optional: time range or focus area — e.g. 'this week' or 'Q1 recap' or 'how is revenue doing']"
allowed-tools: mcp__plugin_slack_slack__slack_search_public mcp__plugin_slack_slack__slack_send_message mcp__plugin_slack_slack__slack_read_thread mcp__notion__notion-search mcp__notion__notion-fetch mcp__notion__notion-query-data-sources mcp__notion__notion-create-pages mcp__notion__notion-update-page mcp__pylon__search_issues mcp__pylon__search_accounts mcp__pylon__get_account mcp__pylon__get_issue ToolSearch Read Grep Bash
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
| `<CROSS_TEAM_CHANNELS>` | Allowlist of broad, cross-team Slack channels to scan for high-engagement threads. Exclude narrow / sensitive channels (HR, exec-private, financing, security-incident, small-group, DMs). |
| `<STRATEGIC_CONTEXT_DOC>` | Path to your quarterly strategic context document |
| `<TEAM_SHARED_CALENDAR_NAME>` | Name of the shared Google Calendar holding OOO + work-anniversaries |

## Before Starting

1. Read `<STRATEGIC_CONTEXT_DOC>` — this is the baseline. Pull current targets, recent actuals, and strategic initiatives.
2. Determine the time range: default to the current week (Monday–Friday) unless the user specifies otherwise. Express the date range explicitly as "April 13–17, 2026" (or equivalent Mon–Fri dates), not just "Week of [Friday]". All Slack and Notion searches should use `after:YYYY-MM-DD` filters anchored to Monday of the current week.
3. Load Notion, Slack, and Pylon tools upfront. Pylon is required for the Support section's fallback path (see Support):
```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch,mcp__notion__notion-query-data-sources,mcp__notion__notion-create-pages,mcp__notion__notion-update-page,mcp__plugin_slack_slack__slack_search_public,mcp__plugin_slack_slack__slack_send_message,mcp__plugin_slack_slack__slack_read_thread,mcp__pylon__search_issues,mcp__pylon__search_accounts,mcp__pylon__get_account,mcp__pylon__get_issue" })
```
4. **Find last week's Plugin Scorecard early.** Plugin output for this section comes from the most recent scorecard, not from ad-hoc searches. The scorecard is a child page of the WLM and covers the prior Tuesday-to-Tuesday window — for a Friday weekly update, that means *last week's completed* scorecard, never a partial week-in-progress. See the [Open Source Plugins](#open-source-plugins-scorecard) section below.

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

**Extract:** The 2-3 most important things in flight right now — active implementations with imminent milestones, pipeline deals with near-term close dates, product deadlines. Do NOT surface board meeting dates, financing status, fundraising updates, or CEO-specific priorities. Frame everything as company priorities, not leadership priorities.

### One Thing You Should Know

This is the single most important signal from the week — proposed based on where the CEO had the highest engagement: Slack threads they responded to, meeting notes they're mentioned in, and the most active topics in recent working sessions.

Search Slack for messages from or mentioning the CEO (`from:<CEO_HANDLE>` or `<@<CEO_SLACK_USER_ID>>`) in the past week to identify where they were most actively engaged.

Search Notion for recent meeting notes (past 7 days) mentioning the CEO or flagged as high-priority.

Critically, do not limit this to threads the CEO drove. Cross-reference the High-Engagement Threads You Were Not In pass below: the single most important signal of the week is often a conversation the CEO missed, not one they led.

**Extract:** The one issue, breakthrough, or risk that had the most leadership attention this week. This should connect directly to What Matters This Week.

### High-Engagement Threads You Were Not In

The weekly update has a blind spot: it leans on threads the CEO already engaged with (the "One Thing" and Shoutouts passes both key off CEO activity), so the most important conversations the CEO *missed* never surface. This pass finds the week's highest-engagement cross-team threads regardless of whether the CEO participated, then prioritizes the ones they did not.

**Scope: cross-team and high-impact only.** Run this discovery ONLY across the broad, cross-team channels listed in `<CROSS_TEAM_CHANNELS>` (see Configuration). Do NOT pull from narrow or sensitive channels (HR / people-ops, exec / leadership-private, financing / fundraising, security-incident, 1-1 or small-group channels, DMs). A thread qualifies only if it is relevant to at least one full team.

**Step 1: Cast a wide net** across the allowlisted channels for the window. Slack search has no "minimum replies" operator, so search on activity and read the candidates:

```
mcp__plugin_slack_slack__slack_search_public({ query: 'in:<channel> after:<monday> before:<saturday> is:thread', limit: 50 })
```

Repeat for each channel in `<CROSS_TEAM_CHANNELS>`.

**Step 2: Rank by real engagement.** For each candidate thread, use `slack_read_thread` and score by reply count, number of distinct participants, and reactions on the parent or replies. A thread with 15 replies from 6 people across two teams outranks a 30-reply back-and-forth between two people. Engagement breadth (how many teams, how many distinct people) matters more than raw reply volume.

**Step 3: Flag the CEO's blind spots.** Mark every high-engagement thread where the CEO (`<@<CEO_SLACK_USER_ID>>`) posted no message. These are the priority - surface the top 2-3 explicitly, because they are exactly what the CEO would otherwise miss.

**Extract:** The top 2-3 high-engagement threads, feeding into "What Matters This Week" and "One Thing You Should Know." For each: a one-line summary, the teams involved, the engagement level (e.g. "23 replies, 8 people across two teams"), a note if the CEO was absent from the thread, and a link to the thread.

### Product & Engineering

Search Slack: `"shipped" OR "released" OR "deployed" OR "launched" OR "merged" OR "v1."` — look for specific release numbers, feature names, and PR descriptions.

Search Notion for this week's Weekly Update page — it typically has a "Shipped this week" section with specifics.

**Extract:** Named releases with version numbers, specific features or UX changes, in-progress work with context on why it matters, and any reliability incidents (what happened, root cause, fix). Use real names — "v1.296.0" and "[named feature] resilience improvements" beats "platform improvements."

### Sales & Pipeline

Search Notion for this week's Weekly Update — the Sales & Pipeline section typically has current Walk to Close deals, named accounts, and amounts.

Search Slack for: `"walk to close" OR "closed" OR "signed" OR "new customer" OR "contract"` for live signals.

Do NOT rely solely on the strategy doc for pipeline numbers — it goes stale quickly. Use live Notion/Slack signals for specific deal names and amounts. Strategy doc is useful only for baseline metrics (Q1 actuals, full-year targets).

**Always cross-check the Pipeline Review meeting note against live HubSpot.** The Pipeline Review runs Monday — by Friday, deals have closed Tue–Fri that won't appear in the meeting note. Pull live closed-won and closed-lost for the current month from HubSpot before writing the bullet. Without this step, MTD numbers will be hours-old at best and stale by 4 days at worst.

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

**Sales is pre-sale ONLY.** Closed-won deals from prior weeks/months are not "Sales" anymore — they are customers and belong in **Customers & Implementation**. Use the cross-section dedup rule below.

### Customers & Implementation

Search Notion for this week's Weekly Update — the Customers & Implementation section has per-customer narratives.

Search Slack: `"go-live" OR "implementation" OR "onboarding" OR "expansion" OR "at risk"` for any live signals.

**Extract:**
- Per-customer narrative updates — specific wins, blockers, milestones, and next steps for each active account. Generic lists are not useful.
- **Status indicator prefixed on every customer name.** Lead each customer bullet with a colored emoji that signals their implementation health: 🟢 on track, 🟡 at risk, 🔴 off track / churn / detractor, ⏸ stalled. Pull the indicator from the WLM implementation-health rollup (on track / at risk / off track / not started / stalled) and cross-check against the Pylon `sentiment` field — when they conflict, the trailing-week sentiment wins. Format: `- 🟡 **Customer (Level) — headline.** body…`. Process / operational bullets that don't name a customer (e.g. PPP automation, Go Live Calendar updates) get no indicator. The reader should be able to scan the section and see the at-a-glance distribution of green / yellow / red.
- Watch items — accounts with active risks or time-sensitive dependencies.
- 30/60/90-day post go-live flags — call out any customers at these milestones explicitly. This is the window where adoption habits form and early churn risk concentrates.

**This is where ALL existing-customer narratives live.** If a customer is closed-won (in Pylon as `account_status: customer` or has a past go-live date), they belong here — not in Sales & Pipeline. Common drift to catch:
- **Customer-specific feature rollout dates** (e.g. "[Customer A]'s AI feature live by [date]") belong here, not in the Sales section's cross-functional rollout-messaging bullet.
- **Commercial-relationship work with an existing customer** (e.g. an existing customer's third-party-integration trial, an existing customer's data-exchange / interoperability work) belongs here, not in Sales. Sales is for pre-sale pipeline only.
- **Partner relationships** (vendors, channel partners, contractor orgs that ship plugins) are neither pipeline nor customer narratives — surface them in Sales under a "Partnership note" sub-bullet, not in Customers.

**Confirmed vs recommended churn / offboarding.** Meeting notes often say "we will recommend that [customer] transition to [competitor]" — that is **internal posture, not a confirmed customer decision.** Do not write the customer as churning or offboarding unless there is direct evidence the customer agreed (signed offboarding plan, executed termination, departure confirmed in writing). Frame the recommendation as "[Your company] exploring recommendation that [customer] transition to [alternative]" until confirmed externally.

**Cross-section dedup pass (required before publishing).** After drafting Sales & Pipeline and Customers & Implementation, do a single pass: for every customer named, ensure they appear in exactly one section. If a customer shows up in both, delete the Sales entry and consolidate detail into Customers. The exception is brand-new closed-won deals from this week, which can be named once in the Sales closed-won list AND once in Customers if there's an implementation milestone to report — but never duplicate narrative.

### Support

**Primary source:** The Support Working Session meeting note from the current week. Query the Meetings database for `Subtype = "Support"` on Monday–Tuesday of the current week, then fetch the page. Do not use `notion-search("support working session")` — it surfaces prior weeks.

Search Slack for: `"developer support" OR "support queue" OR "ticket"` for any signals between sessions.

**Extract:** Which customers are generating the most support volume and why (use the Pylon ticket table in the meeting notes — it has per-customer counts and level). Escalations and their status. Top bugs being prioritized. Patterns in developer/API support activity. What's on the support working session agenda. As customers graduate from implementation, this section becomes increasingly critical.

**Fallback when the Support Working Session metrics are empty:** Check the rendered tables carefully. If the Pylon Support Tickets table, SUP Tickets table, and Top Tickets table are all empty (just template placeholders), **do not** silently omit the section or blame an individual's OOO — there is a named DRI for those metrics and the pipeline is independent of anyone being out. Instead, pull the data directly from Pylon yourself:

1. `mcp__pylon__search_issues({ created_after: "<window_start>T00:00:00Z", created_before: "<window_end>T00:00:00Z", limit: 100 })` — paginate via the returned cursor until you have the full window. The window matches the Support session's Tue→Tue or the weekly update's Mon→Fri; pick whichever the user asked for or, by default, mirror last week's update.
2. Group the issues by `account_id`. The top accounts by volume drive the table.
3. Resolve each top `account_id` with `mcp__pylon__get_account({ account: "<id>" })`. From the account object pull: `name`, `custom_fields.<status_field>` (Level), `custom_fields.sentiment`, `custom_fields.tickets_last_7_days`, `custom_fields.tickets_last_30_days`, `custom_fields.implementation_lead` (or `owner.name`).
4. Build a top-customers table with Customer / Level / Tickets (7d) / Tickets (30d) / Sentiment / IM. Include the IM column so accountability is visible. **Prefix the Customer cell with the same 🟢 / 🟡 / 🔴 / ⏸ status indicator used in the Customers & Implementation section** so a reader can cross-reference health at a glance (e.g. `🔴 Big Leap Health`). Theme bullets under the table get the same indicator prefix on the customer name.
5. Add a "Themes" subsection: WoW direction on the top account, any spike worth context (e.g. batch enrollment forms ≠ regressions), L1 accounts in Frustrated sentiment, and any High Risk / Detractor accounts regardless of volume.
6. Add a one-line **process note** at the bottom of the Support section flagging that the working-session metrics were unpopulated and naming the DRI without blame — e.g. "DRI for those metrics is [Support DRI]; flagging here so the gap doesn't recur." Do NOT attribute the gap to anyone's OOO unless you have direct evidence that the named DRI was out.

Filter spam from the ticket counts: tags `🗑️ Spam Email`, `spam`, and email-sourced issues with no `account_id` should not count toward customer volume.

### Open Source Plugins (Scorecard)

Open source plugin output is a strategic priority and goes under "What Matters This Week" as its own bullet. The source is the most recent **Plugin Scorecard** — a Notion page that lives as a child of the WLM. Do **not** query an ad-hoc internal agent for this section; the scorecard already has the authoritative deduped data with target tracking.

**Critical timing rule:** Always pull from **last week's completed scorecard** (the Tue → Tue window that ends *before* this week's Monday), never a partial in-progress week. For a Friday update covering Mon–Fri, that means the scorecard whose end date is the prior Tuesday (e.g. for an update written Fri 2026-05-15, pull the 2026-05-05 → 2026-05-12 scorecard).

**Step 1 — Find the latest Plugin Scorecard.** Search Notion:

```
notion-search("Plugin Scorecard")
```

Results are sorted by recency; take the most recent one whose end date is ≤ this past Monday. The title pattern is `Plugin Scorecard - YYYY-MM-DD → YYYY-MM-DD`.

**Step 2 — Fetch the page** with `notion-fetch` using the returned ID.

**Step 3 — Extract three things from the page:**

1. **Headline numbers** — total plugins from the customer-facing builder cohort, total engineering plugins, target vs. actual, and how many people hit target on each team.
2. **Plugin inventory table** — name, author, description, repo target, and the "who benefits" column. The inventory is the right level of detail for the weekly update; do not list every PR.
3. **External contributors** — call out non-employee builders separately (community PRs, contractor orgs). Their plugins count toward open-source totals but not toward team targets.

**Step 4 — Format the bullet for "What Matters This Week":**

Lead with the headline numbers, then list a few standout plugins with author attribution. Do not paste the entire inventory into "What Matters" — that's too much for a top-of-update bullet. The full inventory belongs in the Product & Engineering section if it's worth keeping; otherwise omit.

Example format:

```
- **Plugin Scorecard (last week, MM/DD → MM/DD).** N unique plugins from M of [team size] customer-facing builders hit (target 1/week); K engineering plugins from J of [team size] engineers hit (target 0.5/week each = [target]/week team). Standouts this week:
  - `plugin_name_1` — Author — one-line "what it does + who it's for"
  - `plugin_name_2` — Author — one-line
  - ...
  Plus N external contributions from [name] (not on team). Misses worth flagging by name if there's a pattern; otherwise leave individual misses out of the company-wide update.
```

If the scorecard shows 0 new plugins from either cohort, surface that explicitly — it's a leading indicator, not a thing to bury.

**Attribution rule:** Use real first names from the scorecard's PERSON column, not GitHub handles. The team should recognize themselves.

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

The WLM is the **starting point**, not the only source. The richer shoutouts come from triangulating across WLM + Slack + customer channels + the Plugin Scorecard + Pylon. Pull from all of these, dedupe, and lean toward specific named contributions over generic team thanks.

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

A required section at the end of the weekly update. Helps the team plan around coverage gaps and call out personal milestones.

**Source:** The shared team calendar via the `gws` CLI (Bash). Pull the next 7 days starting from today:

```bash
gws calendar +agenda --days 7 --calendar "<TEAM_SHARED_CALENDAR_NAME>" --format json
```

The shared team calendar holds OOO entries and work-anniversaries; individual employee calendars also surface OOO blocks. Parse the JSON, filter to events labeled "OOO", "Out of office", "OoO", "PTO", "vacation", or "work-anniversary" — and to dates within the upcoming Mon–Fri window.

**Format as a small table:**

| Date | Who |
|---|---|
| Mon M/D | Person A, Person B |
| ... | ... |

Then add:

- **Notable:** Work-anniversaries, milestone dates, or planned customer onsites (e.g. "[Customer A] onsite Wed–Thu M/D–D") inside the window.
- **Coverage flags to watch:** When two or more pillar leads (Eng / Support / Customer Ops / Revenue) are out the same day, call it out so the team knows where capacity is thin. Same for L1-customer-facing roles — if two L1 support owners are both out the same day, flag it.

This section is short by design. Don't list every personal calendar event — just OOO and milestones from the shared team calendar.

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

## Customers & Implementation
[Per-customer narratives — specific wins, blockers, next steps. **Each customer bullet prefixed with 🟢 / 🟡 / 🔴 / ⏸ status indicator.** Watch items. 30/60/90-day post go-live flags.]

## Support
[Top accounts by volume table (Customer / Level / Tickets 7d / Tickets 30d / Sentiment / IM) — **Customer cell prefixed with 🟢 / 🟡 / 🔴 / ⏸ matching the Customers & Implementation section.** Themes (also prefixed). Escalations. Bug prioritization. Developer support patterns. Process note if working-session metrics were empty.]

## Shoutouts
[From WLM + Slack #announcements + Slack workspace search + Pylon customer-thank-yous + Plugin Scorecard external contributors + work-anniversaries. Real names, specific contributions, customer leaders included when they thanked us.]

## Company on LinkedIn This Week
[Standing section sourced from the marketing lead's Friday LinkedIn roundup in #announcements. One bullet per post — author bolded, title hyperlinked to the LinkedIn URL preserved exactly from the curated message. Lead with one line noting reshares from your own network travel furthest. Skip the section entirely if there's no roundup this week.]

## OOO Next Week (Mon M/D – Fri M/D)
[Small table of OOO from the shared team calendar. Notable work-anniversaries / customer onsites. Coverage flags where two or more pillar leads or two L1 support owners are out the same day.]
```

## Publishing

Publishing is a **two-step gated flow**. Notion comes first and is its own step — the user reviews the rendered page in Notion before Slack ever goes out. Never combine the two steps under a single approval, and never post to Slack before the Notion page has been created.

### Step 1 — Create the Notion page (review draft)

After you present the drafted update inline, the user will typically ask to "upload to Notion for review", "post to Notion", "put it in Notion", or similar phrasing that mentions Notion specifically. Treat that as approval for Step 1 only. If the user only says "ship it" or "publish it" without specifying, default to Step 1 first and explicitly tell them the Slack post will require a second OK.

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

**After creating the page:** Share the canonical URL with the user and explicitly ask them to review in Notion. State that you will not post to Slack until they give a second approval. Wait for it. Do not auto-proceed.

### Step 2 — Post to Slack (requires separate approval)

Only run this step after the user has reviewed the Notion page AND given a clear second approval to post to Slack ("post to slack", "send the slack", "ship the slack post", "looks good — slack it", or similar). "Looks good" alone after Notion is ambiguous — confirm before posting.

If the user requests edits after reviewing Notion, update the Notion page first (`notion-update-page`), then re-confirm before posting to Slack.

Channel: `<ANNOUNCEMENTS_CHANNEL_ID>`

Post a brief announcement that links to the Notion page — do NOT paste the full update into Slack. 2-3 sentences max: what week it covers, the link, and one sentence with the 2-3 biggest things from the week.

**Always lead with `<!channel>`** so everyone receives the alert. The weekly update is one of the few things that genuinely warrants a channel-wide ping.

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
