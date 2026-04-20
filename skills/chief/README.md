# Chief of Staff — Claude Code Skill Package

An AI Chief of Staff for startup CEOs, built as a package of Claude Code skills.

## What This Is

A system of 13 interconnected Claude Code skills that handle the operational work a Chief of Staff does: investor prep, board materials, memos, deal analysis, LinkedIn content, team performance reviews, competitive intelligence, fundraising coordination, customer escalation synthesis, event planning, and company context management.

## Skills

| Skill | What it Does | Resources |
|-------|--------------|-----------|
| `/chief` | Router — parses intent and dispatches to the right sub-skill | — |
| `context` | Stores and updates company.yaml, org.yaml, and voice.yaml | company.yaml, org.yaml, voice.yaml |
| `memo` | Writes internal memos and strategy docs in the CEO's voice | company.yaml, voice.yaml, Notion, Slack |
| `investor` | Generates investor meeting briefs with firm and attendee research | HubSpot, Clay, Google Calendar |
| `deal` | Analyzes term sheets, contracts, and proposals with negotiation strategy | company.yaml, Gmail |
| `board` | Assembles full board meeting packages from live data | HubSpot, Pylon, Notion, GitHub, Jira, Google Calendar |
| `performance` | Analyzes team performance and tool adoption data | Slack, GitHub, Jira |
| `pipeline` | CEO-level pipeline briefing with monthly and quarterly forecast | HubSpot, Slack, Notion |
| `linkedin` | Drafts LinkedIn posts and articles in the CEO's editorial voice | voice.yaml, company.yaml, Slack |
| `escalation` | Synthesizes support data into at-risk account and trend intelligence | Pylon, Slack, Notion, HubSpot, Jira |
| `event` | Plans events from creative brief through post-event content | Google Calendar, Notion, Figma |
| `fundraise` | Manages end-to-end fundraising as a coordinated campaign | HubSpot, Gmail, chief-investor, chief-deal |
| `competitive` | Monitors competitors and produces battle cards and win/loss analysis | Notion, Slack, Ahrefs |
| `initiative` | Builds the business case and pro forma model for a new line of business | company.yaml, org.yaml |
| `org` | Parses org charts and rosters into structured people and team intelligence | org.yaml, Notion |
| `/company-update` | Company-wide performance view across product, revenue, and customers | Slack, Notion |

## Quick Start

1. **Install:** Copy the `chief*` directories into your `.claude/skills/` folder
2. **Configure:** Run `/chief-context` and fill in your company details
3. **Use:** Run `/chief` with any request, or use a specific skill directly

### First Run

```
/chief
```

If your company context is empty, Chief will walk you through setup interactively.

### Example Commands

```
/chief prep me for my meeting with Sequoia tomorrow
/chief-memo strategy memo on expanding into the mid-market
/chief-linkedin write a post about our new enrollment dashboard
/chief-board assemble materials for next week's board meeting
/chief-deal analyze this term sheet [paste or attach]
/chief-escalation what's happening in support this week
/chief-competitive battle card for [competitor name]
/chief-fundraise where are we on the raise
```

## MCP Server Configuration

These skills are enhanced by MCP server connections. Each skill gracefully degrades when an MCP is unavailable — it tells you what's missing and proceeds with available tools.

| MCP Server | What It Enables | Used By |
|-----------|----------------|---------|
| **Slack** | Channel monitoring, thread search, message drafting | escalation, performance, linkedin, memo, context |
| **Notion** | Wiki, databases, meeting notes, knowledge base | board, event, escalation, memo, context, competitive |
| **HubSpot** | CRM, deal pipeline, contact enrichment | investor, fundraise, escalation, competitive, board |
| **Pylon** | Support tickets, customer issues, resolution tracking | escalation, board |
| **Google Calendar** | Event search, scheduling, meeting logistics | investor, fundraise, event, board |
| **Gmail** | Thread search, draft creation, correspondence | investor, fundraise, deal |
| **GitHub** | Repos, PRs, issues, changelogs | performance, board, competitive |
| **Jira** | Issues, sprints, epics, initiative tracking | performance, board |
| **Figma** | Design files, asset review, comment threads | event |
| **Ahrefs** | Domain analytics, content performance, SEO | linkedin, competitive |
| **Clay** | Contact enrichment, people/company data | investor, fundraise |

## Customization

### Company Context (`chief-context/`)

- **company.yaml** — Your strategy, metrics, positioning, fundraising status
- **org.yaml** — Your org chart, team structure, key relationships
- **voice.yaml** — Your editorial voice, banned phrases, formatting preferences

Update these files directly or run `/chief-context` for interactive updates.

### Templates

Each skill includes templates in its `templates/` directory. Modify these to match your preferred document structure.

### Voice Guide

The voice guide (`voice.yaml`) controls how all written output sounds. Configure:
- Tone and sentence style
- Formatting preferences (numbered lists vs. bullets, bold usage)
- Banned phrases and patterns
- Content archetypes for LinkedIn posts
- Memo formatting rules

## How Skills Compose

Skills call each other when needed:

- `/chief-board` pulls from `/chief-escalation` (support data), `/chief-performance` (eng velocity)
- `/chief-fundraise` composes `/chief-investor` (briefs), `/chief-deal` (term sheets), `/chief-memo` (updates)
- `/chief-linkedin` reads from `/chief-context` (narratives, voice)
- All writing skills use `/chief-memo` conventions for consistent formatting

## Contributing

1. Fork the repo
2. Create a skill directory under `skills/` following the existing pattern
3. Include a `SKILL.md` with valid YAML frontmatter (`name` and `description`)
4. Add templates in a `templates/` subdirectory if needed
5. Update the router table in `chief/SKILL.md`
6. Submit a PR with a description of what the skill does and example usage

## License

MIT
