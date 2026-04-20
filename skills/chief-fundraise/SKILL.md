---
name: chief-fundraise
description: Manage the full fundraising process as a coordinated campaign. Use this skill when the user is actively fundraising or preparing to fundraise. Triggers on "fundraise status", "investor pipeline", "fundraise update", "where are we on the raise", "meeting prep for [investor]", "follow-up for [investor]", "diligence tracker", or when coordinating across multiple investor conversations simultaneously. This skill composes chief-investor, chief-deal, and chief-memo to manage the end-to-end process.
user-invocable: false
---

# Fundraising War Room

You manage the full fundraising process — from pipeline tracking to meeting prep to follow-ups to term sheet evaluation.

## Before Starting

1. Read `chief-context/company.yaml` — especially the fundraising section
2. Check HubSpot for the current state of investor deals/contacts
3. Determine what the user needs: pipeline status, meeting prep, follow-up, or analysis

## Capabilities

### Pipeline Status
Produce a weekly fundraise status memo:
- Pipeline summary by stage: Initial Outreach → First Meeting → Follow-up → Diligence → Term Sheet → Close
- Meetings this week (with brief context for each)
- Follow-ups due (overdue flagged)
- Diligence requests outstanding (by firm, with deadlines)
- Decisions needed this week
- Blockers or stalled conversations

### Meeting Prep
Trigger `/chief-investor` to generate a full brief for any upcoming meeting:
- Auto-detect investor meetings on the calendar for the next 7 days
- Generate briefs for each one
- Present a summary: "You have 4 investor meetings this week. Here's what you need to know."

### Follow-Up Drafting
After a meeting:
- User provides quick notes on what was discussed
- Generate a personalized follow-up email (via Gmail draft)
- Reference specific discussion points from the brief
- Include any materials promised during the meeting
- Set appropriate tone: warm but professional, momentum-building

### Diligence Tracker
Maintain a running list of:
- Outstanding diligence requests by firm
- Status of each (not started, in progress, sent, acknowledged)
- Deadlines (explicit or implied)
- Who on the team owns each deliverable
- Flag items that are blocking progress
- **Deadline risk detection:** Flag any item that is "not started" with a deadline within 5 business days. These are the items most likely to slip and create a bad impression. Surface them in the "Decisions Needed" section with a specific owner and action.

### Term Sheet Comparison
When multiple term sheets arrive:
- Trigger `/chief-deal` for full analysis
- Produce a side-by-side comparison
- Include financial modeling for each scenario
- Provide a clear recommendation

### Investor Update
Draft monthly/quarterly updates to existing investors:
- Key metrics update
- Highlights and wins
- Challenges (be honest — investors respect transparency)
- Specific asks (introductions, expertise, signal)

## Output

Use `/chief-memo` for all written outputs. Pipeline status is a markdown memo. Follow-ups are Gmail drafts. Briefs are markdown files.

## Rules

- Never let a follow-up go more than 48 hours after a meeting without flagging it
- Always surface the single most important action the CEO needs to take this week
- When in doubt about priority, ask: "Which conversation is closest to a term sheet?"
- Treat the fundraise as a sales process — track it with the same rigor as customer deals
