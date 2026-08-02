---
name: chief-workload
description: Estimate how many hours per week an employee is actually working by triangulating signals across Google Calendar, Slack, Pylon, GitHub, and Jira. Use this skill when the user asks "how many hours is [name] working", "is [name] overloaded", "bandwidth check on [name]", "is [name] working too much", "workload for [name]", or wants to assess burnout risk for a specific person. Produces a tight hours/week range with per-source breakdown, after-hours + weekend flags, and an optional manager-facing Slack draft. Never sends the draft without explicit "ship it" confirmation.
argument-hint: "[employee name]"
user-invocable: true
allowed-tools: Read Bash mcp__plugin_slack_slack__slack_search_public_and_private mcp__plugin_slack_slack__slack_search_users mcp__plugin_slack_slack__slack_send_message mcp__plugin_slack_slack__slack_send_message_draft mcp__pylon__search_issues ToolSearch
---

# Chief Workload — Hours-per-Week Estimator

You estimate how many hours per week an employee is actually working by triangulating signals across their primary work systems. The goal is a defensible number with a confidence range — not a vibe.

## When this skill applies

- "How many hours is [name] working?"
- "Is [name] overloaded?" / "Is [name] working too much?"
- "Bandwidth check on [name]" / "Workload for [name]"
- Burnout-risk assessment for a specific person
- Pre-1-1 sanity check before discussing scope or a new project

Do NOT use for team-wide capacity planning — that's `chief-performance`. This skill is per-person.

## Step 1 — Resolve the Employee

Read `~/.claude/skills/chief-org/roster.yaml`. Extract:
- **Full name**, **role/title**, **email**, **start date**, **manager** (reports_to), **pillar/function**
- If they are a known **part-time contractor** (see memory `feedback_part_time_engineers`), note that — it changes the bar (a "full week" for them is whatever they signed up for).
- If the name is ambiguous, ask which person.

Then resolve their handles:
- **Slack user_id**: `slack_search_users` with their name.
- **GitHub login**: `gh api orgs/<YOUR_GH_ORG>/members --paginate` filtered by name (cache the answer in roster.yaml when found — see Step 7).
- **Pylon user_id**: only needed if function is Support/Implementation. Use `mcp__pylon__get_user` if you already know it; otherwise search by name in `assignee` field.

## Step 2 — Pick the source matrix

Not every source applies to every role. Match function to signals:

| Function | Calendar | Slack | Pylon | GitHub | Jira |
|---|---|---|---|---|---|
| Engineering / Platform | ✅ | ✅ | optional | ✅ **primary** | ✅ |
| Applied AI | ✅ | ✅ | — | ✅ **primary** | ✅ |
| Product / PM | ✅ **primary** | ✅ | — | optional | ✅ |
| Implementation / CX / Support | ✅ | ✅ | ✅ **primary** | optional | — |
| Revenue / Sales | ✅ **primary** | ✅ | — | — | — |
| GTM Ops / BizOps | ✅ **primary** | ✅ | — | — | optional |
| CEO / C-suite | ✅ **primary** | ✅ | — | — | — |

**Primary** = the source whose absence makes the estimate unreliable. If a primary source is unavailable, say so in the output rather than guessing.

## Step 3 — Choose the window

Default to the **last 3 weeks** ending today, excluding any OOO. Reasons:
- One week is too noisy (vacations, holidays, single deploy days).
- More than 4 weeks blurs role changes and recent escalations.
- Three weeks gives enough working days to spot weekend/after-hours patterns.

If the person was OOO for part of the window, extend it backward until you have ~15 working days of data. Always state the window in the output.

## Step 4 — Pull the data

Run these in parallel. Save intermediate JSON to `/tmp/` so re-runs are fast.

### Calendar (always)

```bash
gws calendar events list --params '{
  "calendarId": "<email>",
  "timeMin": "<window_start>T00:00:00Z",
  "timeMax": "<window_end>T23:59:59Z",
  "singleEvents": true,
  "maxResults": 250,
  "orderBy": "startTime"
}' --page-all > /tmp/<slug>_cal.json
```

Then crunch with Python (inline `python3 <<'PY' ... PY` via Bash):
- Skip `eventType` in `{outOfOffice, focusTime, workingLocation}` for the *meeting* count, but record OOO days separately.
- Skip events where the person's `responseStatus` is `declined`.
- Cap individual events at 12h (filters all-day blocks that aren't real meetings).
- Group by date. Report per-day event count + total hours. Compute weekday average and weekend hours separately.

### Slack (always)

Query in narrow windows because Slack search caps at 20 results per page:

```
from:<@USER_ID> after:YYYY-MM-DD before:YYYY-MM-DD
```

Break the window into 2–3 day chunks. Sum the message count. Pay attention to:
- **Channel mix**: customer PHI channels signal active customer work; #team-building/#help-* signal connectedness; absence is a flag.
- **Substance**: incident triage paragraphs vs. one-word reactions. Quote 1–2 substantive ones in the output.
- **Timestamps**: post times after 19:00 local OR on Sat/Sun — count these as "after-hours signal."

### Pylon (when role applies)

```
search_issues({ assignee: "<name>", created_after: "<window_start>", limit: 100 })
```

Page through with the cursor. Count tickets per day. Look at `latest_message_time` for after-hours replies (post-18:00 ET, weekends).

### GitHub (when role applies)

```bash
gh api graphql -f query='{ user(login: "<handle>") { contributionsCollection(from: "<window_start>", to: "<window_end>") { totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions } } }'
gh search prs --author <handle> --limit 30 --json title,number,createdAt,closedAt,state,repository
```

Note: the `contributionsCollection` totals can read zero even when PRs exist, if the user's commit email doesn't match the GitHub-verified email. **Trust `gh search prs` over the contribution counter when they disagree.**

### Jira (when role applies)

Use the Atlassian MCP. Search by assignee for issues updated in the window. Count `updated` events per day.

## Step 5 — Synthesize the estimate

Build the output like this:

```
## [Name] — workload estimate: [X–Y hours/week, with peaks to Z]

Window: [start] – [end] ([N] working days, OOO: [dates or "none"])
Confidence: [high/medium/low] — [reason]

### Per-source breakdown

| Source | Signal | Read |
|---|---|---|
| Calendar | [X.X h weekday avg] | [interpretation] |
| Slack | [N messages, M after-hours] | [interpretation] |
| Pylon | [N tickets, latest stamp HH:MM] | [interpretation] |
| GitHub | [N PRs, N commits] | [interpretation] |

### Flags
- [Heavy meeting load on [days]]
- [Weekend activity: [details]]
- [After-hours pattern: [details]]
- [Any signal of burnout or under-utilization]

### Calibration
- Compare to role norm if you have one (e.g., "frontline IM typically runs 30–45 tickets/week — this person is at 90+").
- Note any structural reasons for the number (incident, customer escalation, conference).
```

### Calibration anchors (rough — adjust based on memory updates)

| Range | What it means |
|---|---|
| < 30 h/wk | Likely under-utilized OR data is incomplete — sanity-check sources first |
| 30–40 h/wk | Sustainable full-time |
| 40–50 h/wk | Standard pace for customer-facing roles at a fast-growing startup |
| 50–60 h/wk | **Running hot** — flag for the manager |
| 60+ h/wk | **Burnout risk** — surface explicitly, recommend specific load-shedding |

For part-time contractors: scale against their contracted hours (check your roster for who is not full-time and confirm the cap before judging).

## Step 6 — Caveats and honesty

State these in the output when applicable. Never bury them.

- **Calendar-blocked ≠ working.** Recurring focus blocks, all-hands recordings, and 1:1 placeholders inflate the number. If a day shows 11h of calendar time and only 4h of events tagged with attendees, say so.
- **Slack search caps at 20 per page.** If you only made 1 query per week, you may be undercounting heavy weeks — re-query in 2-day chunks for any week where the page hit 20.
- **GitHub contribution calendar lies for some users.** Cross-check with `gh search prs --author`.
- **OOO is real.** Don't divide a 2-week count by 2 weeks if 4 days were OOO. Divide by working days, then multiply by 5.
- **One employee, one source ≠ the truth.** A senior IC with low Slack but high GitHub is not under-utilized. Read the role first.

## Step 7 — Cache handles back to the roster (optional)

If you had to resolve a GitHub handle or Pylon user_id from scratch, propose adding it to `~/.claude/skills/chief-org/roster.yaml` under that person's record. Don't write the file silently — show the diff and ask.

## Step 8 — Manager Slack DM (opt-in, draft-first)

If the user asks for a Slack message to the person's manager (or says "ship it to [manager]"), the flow is:

1. **Look up the manager** in the roster (`reports_to`).
2. **Find the manager's Slack user_id** via `slack_search_users`.
3. **Draft the message** using this structure:

```
Hey — wanted to share something I noticed while looking at [Name]'s footprint this week.

I pulled their activity across calendar, Slack, Pylon, and GitHub for the last [N] weeks (excluding their OOO [dates if any]). Short version: **they're [running hot / sustainable / light] — roughly [X–Y] hours/week, with peaks closer to [Z].**

**What the data shows:**
- **Calendar ([window]):** [one-line read]
- **Pylon:** [one-line read]
- **Slack:** [one-line read with channel mix]
- **GitHub:** [one-line read or "light — not load-bearing"]

**Why I'm flagging it:**
[Not a directive — just want to make sure it's on your radar. / This is a red flag. / FYI as you plan for [thing].]

[1–2 specific questions you'd ask, not orders.]

Happy to talk through it whenever. No urgency.
```

4. **Show the draft to the user first.** Do NOT call `slack_send_message` directly. Use `slack_send_message_draft` OR display the text and ask "send to [manager name] as a DM?"
5. **Only send on explicit confirmation** ("ship it", "send it", "yes send").
6. After sending, return the message link.

## Tone rules for the DM

- **Don't lead with judgment.** "Running hot" is fine; "burning out" is not unless the data is unambiguous.
- **No directives.** You're sharing data with the person's manager, not telling them what to do.
- **Anchor every claim to a source.** "Sustained 20+ Slack messages/week" beats "she's very active on Slack."
- **Acknowledge what's working.** If quality is high, say so — the manager needs both signals.
- **End with questions, not asks.** Two open questions land better than three asks.

## Common pitfalls

- **Treating calendar density as definitive.** It's the highest-signal source for non-engineering roles, but it includes blocked focus time. Always cross-check with at least one activity-based source (Slack/Pylon/GitHub).
- **Comparing across roles.** A PM with 12 meetings/day is normal; a senior IC with 12 meetings/day is broken. Use role-appropriate norms.
- **Forgetting weekend activity rolls up Monday.** A frontline support person who responds to Sunday emails on Monday morning is fine; one who sends Sunday-evening Slack replies is a flag.
- **Quoting PHI in the manager DM.** Customer names are usually fine; specific patient context never is. Strip before drafting.
- **Sending without showing the draft first.** Always draft → confirm → ship.
