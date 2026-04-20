---
name: chief-1-1
description: Prep for a 1-1 with a direct report. Pulls the employee's role, goals, and function from the org roster, then searches their function-relevant MCPs (Grain, Slack, Notion, HubSpot for Revenue, Pylon for Support) for the past 5 business days. Returns a prioritized 1-1 agenda with impact highlights, blockers, recognition opportunities, and open items. Use when asked "prep my 1-1 with [name]", "1-1 prep [name]", "what should I discuss with [name]", or "my 1-1 with [name]".
argument-hint: "[direct report name — e.g. first name or full name]"
user-invocable: true
allowed-tools: Read mcp__claude_ai_Google_Calendar__gcal_list_events mcp__claude_ai_Google_Calendar__gcal_get_event mcp__grain__search_meetings_v2 mcp__grain__fetch_meeting mcp__grain__fetch_meeting_notes mcp__grain__fetch_meeting_coaching_feedback mcp__grain__search_persons mcp__grain__list_attended_meetings mcp__plugin_slack_slack__slack_search_public_and_private mcp__plugin_slack_slack__slack_read_thread mcp__plugin_slack_slack__slack_search_users mcp__plugin_slack_slack__slack_read_user_profile mcp__notion__notion-search mcp__notion__notion-fetch mcp__notion__notion-query-meeting-notes mcp__hubspot__search_crm_objects mcp__hubspot__get_crm_objects mcp__pylon__search_issues mcp__pylon__get_issue mcp__pylon__get_issue_messages ToolSearch
---

# Chief 1-1 — Direct Report Meeting Prep

You are the CEO's Chief of Staff. Prep a focused, evidence-based 1-1 agenda for a meeting with a direct report by pulling their recent activity from function-appropriate sources.

## Step 1 — Resolve the Employee

Read `~/.claude/skills/chief-org/roster.yaml` to identify the employee.

Match on first name, last name, or nickname. Extract:
- **Full name**
- **Role / title**
- **Pillar** (Platform, Product, Revenue, Ops)
- **Function** (e.g., Engineering, Product, Sales, Support, GTM Ops, BizOps)
- **Start date** (for tenure context)
- **Reports** (if they manage a team — relevant for discussing their team's output)

If the name is ambiguous (e.g., two people share a first name), ask the user to clarify.

## Step 1b — Critical MCP Gate

Once you know the employee's function, determine whether the **system of record for their work** is available. If a critical MCP is DOWN, stop and ask rather than producing an incomplete brief that omits the most important data for that role.

### Function → Critical MCP mapping

| Function | Critical MCP | Why it's blocking |
|---|---|---|
| Support | **Pylon** | Pylon is the ticket system — the primary system of record for all support activity |
| Revenue / Sales | **HubSpot** | HubSpot is the CRM — the primary system of record for deal activity |
| Engineering / Platform | **Jira** | Jira tickets are the primary record of engineering work |
| Product | **Jira + Notion** | Sprint work and specs live here |
| GTM Ops / BizOps | **Notion** | Process docs and planning live here |
| All functions | Grain + Slack | Important but not blocking for any single function — note gaps in Sources rather than stopping |

**Non-critical MCPs for a given function are never blocking.** If Figma is down for a Support employee, or HubSpot is down for an engineer, note it in Sources and proceed.

### How to check availability

If an MCP Health Check table was already produced earlier in this session, read it — do not re-test. If no health check has been run, test the critical MCP now with a lightweight call (e.g., `mcp__pylon__authenticate` for Pylon, `mcp__hubspot__get_user_details` for HubSpot, `mcp__atlassian__atlassianUserInfo` for Jira).

### If a critical MCP is DOWN

**Do not proceed.** Output this message and wait for the user's response:

```
⚠️  Can't prep this 1-1 — [MCP name] is unavailable.

[Employee name] works in [Function]. Their primary system of record is [MCP name] — without it, the brief would be missing their most important work data.

To fix: [specific re-auth instruction, e.g. "Re-auth Pylon by running /chief and completing the OAuth flow when prompted."]

Proceed anyway without [MCP name] data? (yes / no)
```

If the user confirms **yes, proceed anyway**: continue with all available sources, and add a prominent **⚠️ Missing Data** block at the top of the output noting what was unavailable and what that means for the brief's completeness.

## Step 2 — Verify the Meeting on Calendar

```
ToolSearch({ query: "select:mcp__claude_ai_Google_Calendar__gcal_list_events,mcp__claude_ai_Google_Calendar__gcal_get_event" })
```

Search the next 7 days of calendar events for a meeting with this person:

```
gcal_list_events({
  timeMin: "[today at 00:00:00 Pacific]",
  timeMax: "[today + 7 days at 23:59:59 Pacific]",
  q: "[employee first name] OR [employee last name]"
})
```

**If a matching event is found:**
- Extract: date, start time, duration, attendees, any agenda in the event description
- Fetch the full event with `gcal_get_event` if the description looks substantive
- Anchor the output header with: `[Day, Month D at H:MMam/pm]`
- If the event description contains an agenda, surface it in the output as **Their Agenda** (see output format below) and let it inform the talking points
- If multiple matching events exist in the window, use the soonest one and note the others

**If no matching event is found in the next 7 days:**
- Look back 3 days (the meeting may be today or may have just passed)
- If still not found: note "No calendar event found for this 1-1 — confirm timing with [name]" and proceed with the prep anyway
- Do NOT block on this — a missing calendar event doesn't mean the meeting isn't happening

**If Google Calendar auth fails:**
- Note "Calendar unavailable — meeting time unconfirmed" in the output header
- Continue immediately to Step 3

## Step 3 — Load Goals Context

Run in parallel:

**2a. Company OKRs / quarterly priorities**
Read `~/.claude/skills/chief-context/company.yaml` to extract the current quarter's objectives and any goals attributed to this person's pillar or function.

**2b. Personal goals / OKRs in Notion**
```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch" })
```
Search Notion for:
- `"[name] goals"` or `"[name] OKRs"`
- `"[pillar] goals Q2"` or `"[function] priorities"`
- `"performance review [name]"` or `"1-1 [name]"`

Extract: stated goals, current quarter commitments, any noted development areas.

If nothing is found in Notion, note it and proceed — derive goals from their role and the company OKRs.

## Step 3 — Pull the Past 5 Business Days of Activity

Compute the 5-business-day window from today's date (skip weekends). Run all source searches **in parallel**. The sources you pull depend on the employee's **function** — see the function matrix below.

---

### Source A — Grain (all functions)

```
ToolSearch({ query: "select:mcp__grain__search_meetings_v2,mcp__grain__fetch_meeting,mcp__grain__fetch_meeting_notes,mcp__grain__search_persons,mcp__grain__list_attended_meetings" })
```

1. Search for meetings where this person appeared as a participant in the past 5 business days.
2. Also search for your most recent 1-1 with them (look back up to 90 days) — this surfaces open action items from the last time you met.
3. For each relevant meeting, fetch notes and extract:
   - Key topics discussed
   - Decisions made
   - Action items (especially any assigned to them or to you)
   - Any customer/partner signals if they attended external calls

---

### Source B — Slack (all functions)

```
ToolSearch({ query: "select:mcp__plugin_slack_slack__slack_search_public_and_private,mcp__plugin_slack_slack__slack_read_thread,mcp__plugin_slack_slack__slack_search_users,mcp__plugin_slack_slack__slack_read_user_profile" })
```

Search Slack for:
- Messages **from** this person in the past 5 business days — look in channels matching their function (see matrix below)
- Mentions **of** this person — look for kudos, blockers, decisions attributed to them
- Threads where they were active or tagged

Extract:
- Things they shipped, launched, or completed
- Blockers they raised or that others raised about their work
- Positive signals worth naming in the 1-1 (recognition opportunity)
- Anything they committed to that doesn't appear resolved

---

### Source C — Notion (all functions)

```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch,mcp__notion__notion-query-meeting-notes" })
```

Search for:
- Docs created or updated by this person in the past 5 business days
- Meeting notes involving them
- Any project pages or specs they own

Extract: Progress updates, decisions documented, open items.

---

### Source D — HubSpot (Revenue pillar only: AEs, CRO, and anyone whose function is sales)

```
ToolSearch({ query: "select:mcp__hubspot__search_crm_objects,mcp__hubspot__get_crm_objects" })
```

Pull deal activity for the past 5 business days:
- New deals created or stage-advanced
- Deals marked closed-won or closed-lost
- Notes or activity logged by this person
- Pipeline coverage vs. quota (if available)

Extract: Deal velocity, wins, at-risk deals, pipeline gaps.

---

### Source E — Pylon (Support function only: Head of Support and their team)

```
ToolSearch({ query: "select:mcp__pylon__search_issues,mcp__pylon__get_issue,mcp__pylon__get_issue_messages" })
```

Pull support ticket activity:
- Tickets opened or resolved in the past 5 business days
- High-priority or escalated tickets
- Resolution rate trend
- Any tickets that are overdue or stuck

Extract: Volume signals, escalations, patterns, wins.

---

### Function → Channel Matrix for Slack

| Function / Pillar | Slack channels to search |
|---|---|
| Platform (Engineering) | `#eng-*`, `#platform-*`, `#infra-*`, `#product-*`, `#dev-*` |
| Product | `#product-*`, `#design-*`, `#roadmap-*`, `#eng-*` |
| Revenue (Sales) | `#sales-*`, `#revenue-*`, `#deals-*`, `#gtm-*`, `#wins-*` |
| Ops (Support) | `#support-*`, `#cx-*`, `#escalations-*`, `#ops-*` |
| Ops (GTM Ops) | `#gtm-*`, `#revenue-*`, `#ops-*`, `#marketing-*` |
| Ops (BizOps) | `#ops-*`, `#finance-*`, `#biz-ops-*`, `#exec-*` |

Search broadly first, then narrow to the top 5 most active threads.

---

## Step 4 — Synthesize and Output the 1-1 Agenda

Produce the following output inline. Aim for one screen — this is a pre-meeting brief, not a research report.

```
## 1-1 Prep: [Full Name] — [Role]
[Day, Month D at H:MMam/pm] | [Pillar] | [Tenure: X years Y months]
[If no calendar event found: "Meeting time unconfirmed — no calendar event found in next 7 days"]

**Their Agenda** *(if the calendar event has a description or agenda)*
[Bullet the agenda items from the event description verbatim. If none, omit this section entirely.]

**Context**
[2 sentences: what they own this quarter, what success looks like in their role, any relevant tenure or recent-hire context]

**Goals Alignment** (Q[N] 2026)
[Bulleted list of their stated goals or pillar OKRs. Note which are on track vs. unclear based on the evidence. If no goals found, say so.]

---

**Impact This Week**
[3–5 specific, sourced items — what they shipped, closed, resolved, or moved forward in the past 5 business days. Each item cites the source (Grain / Slack / Notion / HubSpot / Pylon). Skip anything vague or unverifiable.]
- [Item — source]
- [Item — source]
- [Item — source]

---

**Talking Points** (prioritized for the conversation)

1. [Most important topic — specific, grounded in evidence. Could be a win to celebrate, a decision that needs your input, or a risk that needs discussion.]
2. [Second priority — often a follow-up on an open action item from the last 1-1 or a commitment they made publicly in Slack.]
3. [Third priority — recognition, development, or forward-looking question. "What do you need from me to hit [goal]?"]
[Add a 4th if the evidence warrants it. Stop at 4.]

---

**Blockers & Watch Items**
[Bulleted list of anything stuck, at risk, or needing your intervention. If no blockers detected from the sources, say: "No blockers surfaced — confirm with them at the start of the meeting."]

---

**Open from Last 1-1**
[Action items or commitments from your most recent Grain meeting with this person. If a Grain 1-1 is found, list the open items and whether they appear resolved based on this week's evidence. If no prior 1-1 found in Grain, say so and recommend checking your notes.]

---

**Sources**
Grain: [N] meetings ([date of most recent 1-1 if found]) | Slack: [N] threads | Notion: [N] docs[HubSpot: [N] deal updates if Revenue][Pylon: [N] tickets if Support]
```

---

## Rules

- Every item in **Impact This Week** and **Talking Points** must cite a specific source — never invent context.
- If a source returns nothing for this person, say so in the Sources line — don't fill gaps with guesses.
- **Talking points are prioritized by what requires your decision or attention, not by recency.** A blocker that surfaced Monday ranks higher than a win that happened yesterday.
- Recognition items belong in Talking Points only if the evidence supports them — don't manufacture praise.
- **Goals Alignment is directional, not definitive.** If you can't find goals in Notion or company.yaml, note it and ask the employee to bring their Q2 priorities to the meeting.
- Keep the output to one screen. If the person manages a team, focus on **their** output and leadership signals — not a full team rollup (use `/chief-roadmap` for that).
- If the person is a recent hire (< 6 months), add a note in Context about onboarding ramp expectations and prioritize the "What do you need from me?" talking point.
- If no activity is found across all sources for the past 5 days (e.g., they were OOO), say so clearly and suggest confirming before the meeting.
