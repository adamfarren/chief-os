---
name: 1-1
description: Prep for a 1-1 meeting. Looks up the other person in the company org roster and checks your calendar to determine if this is a meeting with your manager (→ PPP format: Priorities, Problems, Plans against your goals) or a direct report (→ impact review, talking points, blockers, open items). Pass the person's name or meeting time.
argument-hint: "[person name or meeting time — e.g. 'with Alex', 'my 1-1 with Jordan', '2pm today']"
user-invocable: true
allowed-tools: mcp__notion__notion-search mcp__notion__notion-fetch mcp__notion__notion-query-meeting-notes mcp__grain__search_meetings_v2 mcp__grain__fetch_meeting mcp__grain__fetch_meeting_notes mcp__grain__search_persons mcp__grain__list_attended_meetings mcp__plugin_slack_slack__slack_search_public_and_private mcp__plugin_slack_slack__slack_read_thread ToolSearch Agent
---

# 1-1 — Meeting Prep

Prep a 1-1 with a manager or direct report. The direction of the meeting changes what you need — this skill detects the relationship and formats the output accordingly.

---

## Step 1 — Resolve the Person + Load Org Context

Load Notion tools and fetch the org roster:

```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch" })
notion-search("Org Roster")
```

Fetch the roster page. From it, find the named person and extract:
- Full name and role
- Who they report to
- Who reports to them (if anyone)
- Their team or pillar

If the name is ambiguous (e.g., two people named "Andrew"), ask: "Did you mean [name 1] or [name 2]?"

---

## Step 2 — Verify Meeting on Calendar + Determine Direction

Use the Agent tool to call the `/gcal` skill:

```
Agent: "Use /gcal to find a 1-1 meeting with [person name] in the next 7 days,
or within the past 3 days if not found ahead. Return: event title, start time,
duration, attendee names and email addresses, and any event description or agenda."
```

**If a matching event is found:**
- Extract: date, time, attendees with emails, agenda description
- Use the **attendee email list** to cross-reference both participants against the org roster
- From the org roster, determine: is the named person above or below the current user in the reporting chain?

**Determine direction:**
- **Manager mode** — the named person is listed as the manager/lead of the user's team, or the user appears in the named person's reports list
- **Direct report mode** — the named person appears in the named person's reports list under the current user
- **If direction cannot be determined** from the org roster (e.g., cross-functional peer, ambiguous): ask the user: "Is [name] your manager or a direct report?"

**If no calendar event is found:**
- Note "No calendar event found — confirm meeting time with [name]"
- Ask the user to confirm direction: "Is [name] your manager or a direct report?"

**If /gcal is unavailable:**
- Note "Calendar unavailable" in the output header
- Ask the user: "Is [name] your manager or a direct report?"

---

## Step 3A — Manager Mode: PPP Prep

*Use this when the named person is the current user's manager.*

The PPP framework (Priorities · Problems · Plans) structures reporting-up conversations. Your job is to pull evidence of what you've been doing and help the user frame it against their goals before walking into the room.

### Load your goals

Search Notion for the user's goals and OKRs:
```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch,mcp__notion__notion-query-meeting-notes" })
```

Search for:
- `"[user name] goals"` or `"[user name] OKRs"`
- `"[team] priorities Q2"` or `"[role] goals"`
- `"performance review [user name]"`
- `"1-1 [manager name] [user name]"` — past 1-1 notes for open items

Also read the company context page (your company's handbook's "Company Context" page, or equivalent) for the current quarter's objectives and your team's contribution.

If no personal goals are found: derive from their role, team OKRs, and company context. Note the gap and suggest they write down their Q2 commitments before the meeting.

### Pull your recent activity (past 5 business days)

Compute the 5-business-day window from today (skip weekends). Run in parallel:

**Slack — what you've been doing and committing to**
```
ToolSearch({ query: "select:mcp__plugin_slack_slack__slack_search_public_and_private,mcp__plugin_slack_slack__slack_read_thread" })
```
Search for:
- Messages `from:[user name]` in the past 5 business days — in channels relevant to their team
- Threads where the user made commitments, shipped something, or flagged a problem
- Any kudos or recognition mentions

Extract: things completed or shipped, commitments made, blockers raised, anything unresolved.

**Notion — docs and meeting notes you touched**
```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch,mcp__notion__notion-query-meeting-notes" })
```
Search for docs created or updated by the user, meeting notes from their recent meetings.

Extract: decisions made, progress updates, open items.

**Grain — meetings you attended**
```
ToolSearch({ query: "select:mcp__grain__search_meetings_v2,mcp__grain__fetch_meeting,mcp__grain__fetch_meeting_notes,mcp__grain__search_persons,mcp__grain__list_attended_meetings" })
```
Search for meetings the user attended in the past 5 business days. Also search for the most recent prior 1-1 with this manager (look back up to 90 days) to surface open action items.

Extract: what was discussed, decisions made, what you committed to.

### Output — PPP Format

```
## 1-1 Prep: With [Manager Name]
[Day, Month D at H:MMam/pm] | [Their role]
[If no calendar event: "Meeting time unconfirmed — no event found"]

**Your Goals — Q[N] [Year]**
[Bulleted list of your stated goals or team OKRs. Flag any that are on track vs. at risk based on this week's evidence. If no goals doc found, say so and recommend bringing written priorities to the meeting.]

---

**Priorities** — What you've been working on
[3–5 bullets: specific things you shipped, progressed, or closed in the past 5 days. Each cites a source. Lead with what best demonstrates progress toward your goals.]
- [Item — source]
- [Item — source]
- [Item — source]

**Problems** — What you need from your manager
[Bulleted list of blockers, decisions you need, risks worth flagging, or things that are stuck. Be specific: what is the problem, what decision or action is needed, and what happens if it stays stuck.]
- [Problem — what you need]
- [Problem — what you need]
[If no problems surfaced: "No blockers to surface — confirm this is still accurate before walking in."]

**Plans** — What's next
[2–4 bullets: what you're focused on next week or this month. Include one explicit ask — something you need your manager to do, decide, or unblock.]
- [Plan]
- [Plan]
- Ask: [one specific thing you need from your manager]

---

**Open from Last 1-1** ([date if found])
[Action items or commitments from your most recent Grain 1-1 with this manager. Note which appear resolved vs. still open based on this week's evidence. If no prior 1-1 found in Grain, say so.]

---

**Sources**
Grain: [N] meetings ([date of most recent 1-1 if found]) | Slack: [N] threads | Notion: [N] docs
```

---

## Step 3B — Direct Report Mode: Impact + Talking Points

*Use this when the named person reports to the current user.*

Pull the direct report's recent activity from function-appropriate sources.

### Determine their function

From the org roster: note their role, team, and pillar. This determines which Slack channels to search and whether to pull HubSpot (Revenue) or Pylon (Support) data.

| Function / Pillar | Slack channels to search | Extra sources |
|---|---|---|
| Platform (Engineering) | `#eng-*`, `#platform-*`, `#infra-*`, `#dev-*` | Notion (Jira via connected source) |
| Product | `#product-*`, `#roadmap-*`, `#eng-*` | Notion |
| Revenue (Sales) | `#sales-*`, `#revenue-*`, `#deals-*`, `#wins-*` | HubSpot |
| Ops (Support) | `#support-*`, `#cx-*`, `#escalations-*` | Pylon |
| Ops (GTM / BizOps) | `#gtm-*`, `#ops-*`, `#revenue-*` | Notion |

### Load their goals

Search Notion for:
- `"[name] goals"` or `"[name] OKRs"`
- `"[team] priorities Q2"` or `"1-1 [name]"`
- Any prior 1-1 notes with this person

### Pull the past 5 business days of activity

Compute the 5-business-day window from today (skip weekends). Run all searches **in parallel**:

**Grain (all functions)**
```
ToolSearch({ query: "select:mcp__grain__search_meetings_v2,mcp__grain__fetch_meeting,mcp__grain__fetch_meeting_notes,mcp__grain__search_persons,mcp__grain__list_attended_meetings" })
```
Search for meetings the direct report attended in the past 5 business days. Also fetch the most recent prior 1-1 with them (look back 90 days) for open action items.

**Slack (all functions)**
```
ToolSearch({ query: "select:mcp__plugin_slack_slack__slack_search_public_and_private,mcp__plugin_slack_slack__slack_read_thread" })
```
Search for messages from this person and mentions of them, in channels matching their function. Read the top 5 most active threads. Extract: things shipped, blockers, commitments, recognition signals.

**Notion (all functions)**
```
ToolSearch({ query: "select:mcp__notion__notion-search,mcp__notion__notion-fetch,mcp__notion__notion-query-meeting-notes" })
```
Search for docs updated or meeting notes involving this person. Extract: progress updates, decisions, open items.

**HubSpot (Revenue function only)**
```
ToolSearch({ query: "select:mcp__hubspot__search_crm_objects,mcp__hubspot__get_crm_objects" })
```
Pull deal activity for the past 5 business days: stage advances, closes, notes logged.

**Pylon (Support function only)**
```
ToolSearch({ query: "select:mcp__pylon__search_issues,mcp__pylon__get_issue" })
```
Pull ticket activity: opens, resolves, escalations, high-priority items.

### Output — Direct Report Format

```
## 1-1 Prep: [Full Name] — [Role]
[Day, Month D at H:MMam/pm] | [Team/Pillar] | Tenure: [X years Y months]
[If no calendar event: "Meeting time unconfirmed"]

**Their Agenda** *(only if the calendar event has an agenda in the description)*
[Bullet verbatim from event description. Omit section if none.]

**Context**
[2 sentences: what they own this quarter, what success looks like for their role.]

**Goals Alignment** (Q[N] [Year])
[Bulleted list of their stated goals or team OKRs — note which appear on track vs. unclear. If no goals found, say so and suggest asking them to bring written priorities.]

---

**Impact This Week**
[3–5 specific, sourced items — what they shipped, closed, resolved, or moved forward. Each cites the source. Skip anything vague or unverifiable.]
- [Item — source]
- [Item — source]
- [Item — source]

---

**Talking Points** (prioritized by what needs your attention)
1. [Most important — a decision needed, a win to recognize, or a risk to discuss. Grounded in evidence.]
2. [Second priority — follow up on an open item or public commitment.]
3. [Third priority — development, recognition, or forward-looking question.]
[Add a 4th only if evidence warrants it.]

---

**Blockers & Watch Items**
[Bulleted list of anything stuck, at risk, or needing your intervention. If none surfaced: "No blockers detected — confirm at the start of the meeting."]

---

**Open from Last 1-1** ([date if found])
[Action items or commitments from your most recent Grain 1-1 with this person. Flag which appear resolved vs. still open. If no prior 1-1 found in Grain, say so.]

---

**Sources**
Grain: [N] meetings ([date of most recent 1-1 if found]) | Slack: [N] threads | Notion: [N] docs[HubSpot: [N] deal updates — Revenue only][Pylon: [N] tickets — Support only]
```

---

## Rules (both modes)

- Every item in **Priorities** / **Impact This Week** / **Talking Points** must cite a specific source — never invent context.
- If a source returns nothing, say so — don't fill gaps with guesses.
- **Manager mode:** The PPP sections should be honest and specific. This is not a status report — it's a conversation starter. "Problems" is the most important section: if there's nothing there, the 1-1 loses most of its value.
- **Direct report mode:** Talking points rank by what requires the manager's decision or attention — not by recency.
- Recognition belongs in Talking Points only if the evidence supports it — don't manufacture praise.
- Keep output to one screen — this is pre-meeting context, not a research report.
- If the person is a recent hire (< 6 months), note ramp expectations in the Context line and prioritize the "What do you need from me?" question.
- If no activity is found for the past 5 days (OOO, travel), say so clearly and suggest confirming before the meeting.
- Don't include DM content or verbatim personal opinions from Slack.
