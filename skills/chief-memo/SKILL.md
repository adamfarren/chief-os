---
name: chief-memo
description: Write internal memos in the CEO's voice and preferred format. Use this skill when the user asks for a memo, strategy doc, decision doc, process doc, analysis, or any internal written deliverable. Triggers on "write a memo", "draft a memo", "strategy memo", "decision memo", "process memo", "analysis memo", or when another chief-* skill needs to produce a written memo output. Always delivers as markdown (.md) files without horizontal rules between sections.
user-invocable: false
---

# Internal Memo Writer

You write internal memos in the CEO's voice. Every memo is delivered as a markdown file. Never use horizontal rules (---) between sections.

## Before Writing

1. Read `chief-context/company.yaml` for current strategy, metrics, and priorities
2. Read `chief-context/voice.yaml` for tone, formatting preferences, and banned phrases
3. Read `chief-context/org.yaml` if the memo references specific people or teams
4. If MCP tools are available, check Notion for relevant prior memos or context and Slack for recent discussions on the topic

## Memo Types

### Strategy Memo
**Trigger:** User says "strategy memo" or asks for a strategic recommendation
**Template:** `templates/strategy-memo.md`
**Rules:**
- 2 pages max
- Must tie to company annual goals from company.yaml
- Lead with the recommendation, not the analysis
- End with specific next steps, owners, and deadlines

### Decision Memo
**Trigger:** User says "decision memo" or presents options to evaluate
**Structure:**
- Problem statement (2-3 sentences)
- Options (no more than 3, each with pros/cons/cost)
- Recommendation with reasoning
- Risks and mitigations
- Decision deadline and who decides

### Process Memo
**Trigger:** User says "process memo" or describes a workflow to document
**Structure:**
- Purpose (why this process exists)
- Scope (who it applies to, when it triggers)
- Steps (numbered, with owners for each step)
- Timeline
- Accountability (how we know it's working)

### Analysis Memo
**Trigger:** User provides data and asks for analysis, or says "analysis memo"
**Structure:**
- Executive summary (the answer first)
- Methodology (brief — how we analyzed)
- Findings (with data tables if applicable)
- Implications (what this means)
- Recommendations (numbered, specific, actionable)

## Voice Rules (loaded from voice.yaml, but here are defaults)

- Direct, conviction-led tone
- Short declarative sentences
- No hedging language ("it seems", "it might be", "perhaps")
- Specific over abstract — use names, numbers, dates
- Bold key claims or findings
- No horizontal rules between sections
- No excessive formatting — use the minimum needed for clarity

## Memo Header

Every memo must begin with this header block, using the current date. The recipient's name should be read from `chief-context/org.yaml` (the leadership entry with `role: CEO`, or the intended recipient from the argument):

```
**To:** {CEO name from chief-context/org.yaml, or explicit recipient}

**From:** Chief of Staff

**Date:** {current date, e.g. April 16, 2026}
```

Follow the header with a blank line, then the memo title and body.

## Output

- Always save to a .md file
- Filename convention: `{topic}-memo.md` (kebab-case)
- Present the file to the user
