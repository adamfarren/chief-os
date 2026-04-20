# Chief OS — Claude Code Skills

This repo contains the Chief of Staff skill package for Claude Code.

## Architecture

This repo contains **generic, reusable skills**. Company-specific skills and data live locally in `~/.claude/skills/` and are never committed here.

Three layers:
1. **Public skills** (this repo) — symlinked into `~/.claude/skills/` via `install.sh`
2. **Override skills** — exist in the repo but local versions are used instead (e.g., router, style, context)
3. **Private skills** — live only in `~/.claude/skills/`, not in this repo

## Skills

- `skills/chief/` — Router skill, entry point for all requests
- `skills/chief-context/` — Company context (strategy, org, voice)
- `skills/1-1/` — Employee 1-1 skill: org + calendar detect direction, PPP format for manager meetings, impact + talking points for direct reports
- `skills/chief-1-1/` — 1-1 prep for direct reports: function-aware activity pull, prioritized talking points
- `skills/chief-memo/` — Internal memo writer
- `skills/chief-investor/` — Investor meeting briefs
- `skills/chief-deal/` — Deal and term sheet analysis
- `skills/chief-board/` — Board meeting materials
- `skills/chief-performance/` — Team performance analysis
- `skills/chief-pipeline/` — CEO-level pipeline briefing with forecast
- `skills/chief-linkedin/` — LinkedIn content engine
- `skills/chief-escalation/` — Customer escalation synthesis
- `skills/chief-event/` — Event planning
- `skills/chief-fundraise/` — Fundraising process management
- `skills/chief-competitive/` — Competitive intelligence
- `skills/chief-style/` — Brand style guide, design tokens, Figma integration
- `skills/chief-initiative/` — Business case and pro forma model for a new line of business
- `skills/chief-org/` — Org intelligence from charts and headcount rosters
- `skills/chief-roadmap/` — Engineering roadmap progress: Jira throughput by project and engineer
- `skills/claude-usage/` — Weekly Claude usage ingestion: Slack canvas → Google Sheets tab + tiered adoption analysis
- `skills/company-update/` — Weekly company-wide update from live data sources
- `skills/funnel/` — Lead funnel analysis: lead volume by source, lead→qualified→deal conversion, velocity
- `skills/whiteboard/` — FigJam diagram generation: flowcharts, sequences, state machines, Gantt charts with brand colors

## Installation

```bash
./install.sh          # create symlinks from ~/.claude/skills/ → this repo
./install.sh --status # show what's linked, overridden, and private
```

The install script:
- Symlinks public skills into `~/.claude/skills/`
- Backs up any existing real directories before replacing
- Never overwrites `chief-context/`, `chief-style/`, or `chief-org/` (local overrides — customize per company)
- Seeds `chief-context/` with example data if it doesn't exist

Then run `/chief-context` to configure your company details.

## Rules

- No company-specific context, customer names, employee PII, or internal IDs should be added to this repo — keep those in your private fork or in the override skills
- Skills in `install.sh` OVERRIDE_SKILLS array are maintained locally with company-specific modifications
- When editing a symlinked skill, changes go directly into this repo's working tree
