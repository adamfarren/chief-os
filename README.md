# Chief OS

An AI Chief of Staff for startup CEOs, built as a package of Claude Code skills.

## What This Is

A system of 25 interconnected Claude Code skills that handle the operational work a Chief of Staff does: investor prep, board materials, memos, deal analysis, LinkedIn content, team performance reviews, competitive intelligence, fundraising coordination, customer escalation synthesis, customer 360 analysis, meeting digests, event planning, brand style guide, org intelligence, 1-1 direct report prep, and company context management.

## Architecture

Chief OS uses a three-layer architecture that separates generic skills (shareable) from company-specific content (private):

```
┌─────────────────────────────────────────────────────────┐
│  ~/.claude/skills/                                      │
│                                                         │
│  PUBLIC (symlinked → ~/repos/chief-os/)                 │
│  ├── chief-memo/        ── Generic skill logic.         │
│  ├── chief-investor/       Edits flow directly to the   │
│  ├── chief-board/          repo working tree.           │
│  ├── chief-deal/           git commit && git push.      │
│  ├── ...13 skills                                       │
│                                                         │
│  OVERRIDE (in repo, but local version used)             │
│  ├── chief/             ── Same skill exists in the     │
│  ├── chief-context/        repo with generic defaults,  │
│  ├── chief-style/          but local copy is used       │
│  ├── chief-org/            because it has company-      │
│                            specific data baked in.       │
│                                                         │
│  PRIVATE (local only, never in repo)                    │
│  ├── your-custom-skill/ ── Company-specific skills      │
│  ├── ...                   that only exist on your      │
│                            machine.                     │
└─────────────────────────────────────────────────────────┘
```

### How the layers work

| Layer | Where it lives | What it contains | Synced to repo? |
|-------|---------------|-----------------|-----------------|
| **Public** | Symlink → `~/repos/chief-os/skills/` | Generic skill logic any CEO can use | Yes — edits go directly to the repo |
| **Override** | `~/.claude/skills/` (real directory) | Skills that exist in the repo but need company-specific modifications | No — local copy takes precedence |
| **Private** | `~/.claude/skills/` (real directory) | Skills unique to your company that have no generic equivalent | No — never touches the repo |

### Skills

```
/chief              ← Router: parses intent, dispatches to sub-skills
/chief-context      ← Foundation: company strategy, org chart, voice guide
/1-1                ← Employee 1-1: auto-detects manager vs direct report, PPP upward / impact+talking points downward
/chief-1-1          ← 1-1 prep for direct reports: impact, blockers, talking points
/chief-memo         ← General-purpose memo writer in CEO's voice
/chief-investor     ← Investor meeting briefs with firm/attendee research
/chief-deal         ← Term sheet analysis, contract review, negotiation prep
/chief-board        ← Board meeting materials from live data sources
/chief-performance  ← Team performance and tool adoption analysis
/chief-linkedin     ← LinkedIn posts in codified editorial voice
/chief-escalation   ← Customer support intelligence and at-risk alerts
/chief-event        ← Event planning from creative brief to post-event
/chief-fundraise    ← End-to-end fundraising process management
/chief-competitive  ← Competitive intelligence and battle cards
/chief-digest       ← Daily meeting digest from transcripts → Slack
/chief-style        ← Brand style guide, design tokens, Figma integration
/chief-initiative   ← Business case and pro forma model for a new line of business
/chief-org          ← Org intelligence from charts and headcount rosters
/chief-pipeline     ← CEO-level pipeline briefing with forecast
/customer-360       ← Full 360-degree customer view across all services
/chief-roadmap      ← Engineering roadmap progress: Jira throughput mapped to OKRs, by project and engineer
/claude-usage       ← Weekly Claude usage ingestion: Slack canvas → Google Sheets + tiered adoption analysis
/company-update     ← Weekly company-wide update from Slack, HubSpot, Grain, Notion
/funnel             ← Lead funnel analysis: lead volume by source, lead→qualified→deal conversion rates and velocity
/whiteboard         ← FigJam diagrams with brand colors: flowcharts, sequences, state machines, Gantt
```

## Org Area → Source of Truth

Each org area has a DRI (Directly Responsible Individual) and a canonical tool that is the single source of truth. Skills always pull from the designated tool first when they need data for that area.

| Org Area | DRI | Source of Truth | MCP | Used By |
|----------|-----|----------------|-----|---------|
| **Sales & Revenue** | VP Sales | HubSpot | `mcp__hubspot__*` | pipeline, board, investor, fundraise, deal, escalation, customer-360 |
| **Engineering** | CTO | Jira | `mcp__jira__*` | roadmap, board, escalation, customer-360 |
| **Customer Success** | Head of CS | Pylon | `mcp__pylon__*` | escalation, board, customer-360 |
| **People & Org** | CEO | Notion — Org Roster | `mcp__notion__*` | chief-org |
| **Knowledge Base** | Everyone | Notion — Handbook | `mcp__notion__*` | board, competitive, escalation, memo, digest, context |
| **Customer Calls** | CS / Sales | Grain | `mcp__grain__*` | digest, company-update |
| **Internal Comms** | Everyone | Slack | `mcp__plugin_slack_slack__*` | pipeline, digest, escalation, performance, linkedin, company-update |
| **Design & Brand** | Design | Figma | `mcp__figma__*` | style |
| **Finance & IR** | CEO | HubSpot + Gmail + Google Sheets (financial model) | `mcp__hubspot__*` + `gws sheets` | investor, fundraise, deal, context |

> **Note on Jira:** Jira is a first-class MCP in the health check (`jira_get_myself`). If you don't have a dedicated Jira MCP configured, skills fall back to querying Jira via Notion's connected databases integration — but a direct Jira MCP gives better coverage.

## Quick Start

### 1. Clone and install

```bash
git clone git@github.com:adamfarren/chief-os.git ~/repos/chief-os
cd ~/repos/chief-os
./install.sh
```

The install script creates symlinks from `~/.claude/skills/` to the repo for all public skills. It backs up any existing skill directories before replacing them.

### 2. Set up your company context

Chief OS needs three pieces of context to work. These live in `~/.claude/skills/chief-context/` — a local directory that is **never synced to the repo**.

The install script seeds this directory with empty templates. Fill them in by running `/chief-context` in Claude Code, or edit the YAML files directly.

> **Tip:** If you want to explore the system before filling in real data, copy the fictional Meridian Ledger examples from `examples/` into `~/.claude/skills/chief-context/`. See [`examples/README.md`](examples/README.md) for the exact commands.

**company.yaml** — Your company's identity and metrics:
- Company name, stage, one-liner
- Key metrics: ARR, growth rate, customer count, burn rate, runway
- Strategy: annual goals, active initiatives with status
- Product: architecture, key products, differentiators
- Positioning: competitive lanes, key narratives
- Fundraising: current round, target, status

**org.yaml** — Your team and relationships:
- Leadership: name, role, reports-to, what they own
- Teams: name, lead, members, current focus
- Key relationships: investors, advisors, board members

**voice.yaml** — How your written output should sound:
- Tone and sentence style
- Formatting preferences (numbered lists vs. bullets, bold usage)
- Banned phrases
- Content patterns for recurring output types
- Memo and investor brief structure rules

### 3. Customize override skills (optional)

Four skills exist in the repo with generic defaults but are designed to be customized locally:

| Override skill | Why it needs local customization |
|---------------|--------------------------------|
| `chief/` | Router table — add your company-specific skills and routing rules |
| `chief-context/` | Company data — your real strategy, metrics, org, and voice |
| `chief-style/` | Design system — your Figma file key, brand colors, design tokens |
| `chief-org/` | Org data — your real roster, reporting lines, and headcount |

These are **not symlinked**. The install script copies the repo's generic version only if the local directory doesn't already exist. Once you've customized them, your local version is preserved across updates.

### 4. Use

Run `/chief` with any request, or invoke a specific skill directly:

```
/chief prep me for my meeting with Sequoia tomorrow
/chief-1-1 prep my 1-1 with [direct report name]
/chief-memo strategy memo on expanding into the mid-market
/chief-linkedin write a post about our new enrollment dashboard
/chief-board assemble materials for next week's board meeting
/chief-deal analyze this term sheet
/chief-escalation what's happening in support this week
/chief-digest what happened in customer meetings today
/chief-competitive battle card for [competitor name]
/chief-fundraise where are we on the raise
/chief-performance analyze this adoption data
/chief-event creative brief for our user conference
/chief-style what are our brand colors
/chief-org show me the org
/chief-org who reports to the CTO
/customer-360 pull everything on [customer name]
```

## Managing Skills

### Check status

```bash
./install.sh --status
```

Shows what's symlinked, what's overridden locally, and what's private.

### Update public skills

```bash
cd ~/repos/chief-os
git pull
```

Symlinked skills update automatically — no re-install needed.

### Add a new private skill

Create a directory in `~/.claude/skills/` with a `SKILL.md` file. It stays local and is never synced.

### Promote a private skill to public

If you build a generic skill that any CEO could use:

1. Copy it to `~/repos/chief-os/skills/`
2. Remove any company-specific content
3. Add it to the `PUBLIC_SKILLS` array in `install.sh`
4. Run `./install.sh` to replace the local copy with a symlink
5. Commit and push

### Proprietary content guard

A git pre-commit hook scans all staged changes for company-specific terms before allowing a commit. To configure it:

1. Create `.proprietary-terms` in the repo root (one regex pattern per line)
2. The file is gitignored — it only exists on your machine
3. Any commit containing a matching term is blocked with a clear error

Example `.proprietary-terms`:

```
# Company name
Acme Corp

# Customer names
Big Client Inc
Another Customer

# Internal tools
internal-admin-tool

# Figma keys
abc123def456
```

## Skill Reference

| Command | What It Does |
|---------|-------------|
| `/chief` | Router — parses your request and dispatches to the right skill |
| `-context` | View/update company strategy, metrics, org chart, voice guide; pulls live ARR/MRR/usage from Google Sheets (Growth Forecast, MRR by Customer, Usage Metrics) when updating financials |
| `-1-1` | Prep a 1-1 with a direct report — gates on the employee's system-of-record MCP (Pylon for Support, HubSpot for Sales, Jira for Engineering) before pulling activity, then produces a prioritized agenda with impact highlights, blockers, open items from the last 1-1, and calendar-verified meeting time |
| `-memo` | Write strategy, decision, process, or analysis memos in CEO's voice |
| `-investor` | Generate investor meeting briefs with firm research, attendee profiles, rapport flags |
| `-deal` | Analyze term sheets, contracts, proposals; compare options; build negotiation playbooks |
| `-board` | Assemble board materials pulling live data from HubSpot, Jira (via Notion), Pylon, Notion |
| `-performance` | Analyze team performance and tool adoption data with tiered breakdowns |
| `-linkedin` | Draft LinkedIn posts using codified editorial voice and content archetypes |
| `-escalation` | Synthesize customer support data into CEO-level intelligence |
| `-event` | Plan events from creative brief through post-event content |
| `-fundraise` | Manage the full fundraise: pipeline, meeting prep, follow-ups, term sheet comparison |
| `-competitive` | Competitive intelligence, battle cards, win/loss analysis |
| `-digest` | Daily digest of external customer/prospect meetings, posted to Slack |
| `-style` | Brand style guide, design tokens, colors, component patterns; pulls fresh tokens from Figma |
| `-initiative` | Business case and pro forma model for a new line of business |
| `-org` | Org intelligence: parse org charts and headcount rosters into people context; tracks contracted agencies as extended teams (separate from headcount); proposes Notion sync after any roster update |
| `-pipeline` | CEO-level pipeline briefing with forecast, stage movement, and stuck-deal flags |
| `/customer-360` | Build a full 360-degree customer view across CRM, Slack, Jira, Notion, email, calendar, and web |
| `/chief-roadmap` | Track engineering progress against the roadmap — Jira throughput by project and by engineer, with quarterly/monthly/2-week framing |
| `/claude-usage` | Pull weekly Claude usage canvas from Slack, write to Google Sheets, run tiered adoption analysis with coaching recommendations |
| `/company-update` | Weekly company-wide update: pulls Slack, HubSpot, Grain, and strategy context into a Notion page |
| `/funnel` | Lead funnel analysis: lead volume by source, lead→qualified→deal conversion rates and velocity |
| `/whiteboard` | Create diagrams in FigJam — flowcharts, sequence diagrams, state machines, and Gantt charts; reads brand colors from your style guide |

## MCP Server Configuration

Skills are enhanced by MCP server connections. Each skill gracefully degrades when an MCP is unavailable — it tells you what's missing and proceeds with available tools.

| MCP Server | Org Area | What It Enables | Used By |
|-----------|---------|----------------|---------|
| **HubSpot** | Sales & Revenue | CRM, deal pipeline, contact enrichment | pipeline, investor, fundraise, escalation, board, partnerships, customer-360 |
| **Notion** | Knowledge Base + People/Org | Wiki, databases, meeting notes, org roster | roadmap, board, event, escalation, digest, memo, context, competitive, customer-360 |
| **Jira** | Engineering | Sprint boards, epics, issues, throughput by project and engineer | roadmap, board, escalation, customer-360 |
| **Pylon** | Customer Success | Support tickets, customer issues, CES tracking | escalation, board, customer-360 |
| **Slack** | Internal Comms | Channel monitoring, thread search, message drafting | pipeline, digest, escalation, performance, linkedin, company-update |
| **Grain** | Customer Calls | External meeting summaries, transcripts, AI notes | digest, company-update |
| **Figma** | Design & Brand | Design files, asset review, design tokens, style guide sync, diagram generation | style, event, whiteboard |
| **Gmail** | Finance & IR / Comms | Thread search, draft creation, correspondence | investor, fundraise, deal, customer-360 |
| **Google Calendar** | Scheduling | Event search, scheduling, meeting logistics | investor, fundraise, event, board, customer-360 |
| **Google Drive** | Docs & Files | File search, document access, shared drive browsing | investor, fundraise, deal, board, customer-360 |
| **GitHub** | Engineering | Repos, PRs, issues, changelogs | board, competitive |
| **Sentry** | Engineering | Error tracking, issue monitoring, stability signals | customer-360 |
| **Ahrefs** | Marketing | Domain analytics, content performance, SEO | linkedin, competitive |
| **Clay** | Sales & IR | Contact enrichment, people/company data | investor, fundraise |

> **Jira access:** Connect the Jira MCP for direct access (`jira_get_myself` is used in the session health check). Without a dedicated Jira MCP, skills fall back to Notion's connected databases integration — add Jira to your MCP config for full engineering data coverage.

> **Google Workspace (Gmail, GCal, GDrive):** These are not MCP servers — they run through the [`gws` CLI](https://github.com/nicholasgasior/gws) via Bash. Install `gws` and run `gws auth login` to authenticate. The session health check tests all three with lightweight `gws` calls.

## How Skills Compose

Skills call each other when needed:

- `/customer-360` searches CRM, Slack, Jira, Notion, email, calendar, Sentry, Pylon, and the web — then synthesizes into one report
- `/chief-board` pulls from `/chief-escalation` (support data), `/chief-digest` (customer voice), and `/chief-performance` (eng velocity)
- `/chief-digest` reads transcripts from Notion (sourced from a meeting recorder like Fathom), synthesizes, and posts to Slack
- `/chief-fundraise` composes `/chief-investor` (briefs), `/chief-deal` (term sheets), `/chief-memo` (updates)
- `/chief-linkedin` reads from `/chief-context` (narratives, voice)
- `/chief-style` provides brand tokens to any skill producing visual output (dashboards, presentations, UI)
- `/whiteboard` reads from `/chief-style` (or `/style`) to apply brand colors to FigJam diagrams automatically
- `/company-update` pulls from Slack (5 channel categories), HubSpot (pipeline snapshot), Grain (external meetings), and strategy context to produce the weekly update in Notion
- All writing skills use `/chief-memo` conventions for consistent formatting

## Customization

### Company Context

Edit the YAML files in `~/.claude/skills/chief-context/` directly or run `/chief-context` for interactive updates. These files are the single source of truth that all skills read from.

### Templates

Each skill includes templates in its `templates/` directory. Modify these to match your preferred document structure.

### Voice Guide

The voice guide (`~/.claude/skills/chief-context/voice.yaml`) controls how all written output sounds. Configure tone, formatting, banned phrases, content archetypes, and memo rules.

## Contributing

1. Fork the repo
2. Create a skill directory under `skills/` following the existing pattern
3. Include a `SKILL.md` with valid YAML frontmatter (`name` and `description`)
4. Add templates in a `templates/` subdirectory if needed
5. Update the router table in `skills/chief/SKILL.md`
6. Submit a PR

## License

MIT
