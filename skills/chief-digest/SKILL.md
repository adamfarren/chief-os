---
name: chief-digest
user-invocable: false
description: Produce a daily executive digest of external customer and prospect meetings. Use this skill when the user asks for a meeting digest, daily meeting summary, customer meeting recap, prospect meeting notes, or says "what happened in meetings today". Pulls meeting transcripts from Notion (sourced from Fathom or another meeting recorder), synthesizes cross-conversation patterns, and posts the digest to a dedicated Slack channel. Triggers on "meeting digest", "daily digest", "customer meetings today", "what did we learn from calls", or when another chief-* skill needs a summary of recent external meetings.
---

# Daily Meeting Digest

You produce a daily executive readout of external customer and prospect meetings for leadership. Your job is to synthesize meeting transcripts into a skimmable Slack digest.

## Before Starting

1. Read `chief-context/company.yaml` for company context and customer/prospect names
2. Read `chief-context/voice.yaml` for formatting preferences

## Data Pipeline

### Source: Meeting Transcripts in Notion

Meeting transcripts are collected in Notion, sourced from a meeting recorder (currently Fathom).

> **Implementation note:** Fathom does not have an MCP server, so transcripts are manually synced to Notion. This step can be eliminated by swapping Fathom for a meeting recorder that has MCP integration (e.g., Grain, Fireflies) — the recorder would feed transcripts directly to this skill, cutting out the Notion intermediary. The rest of the pipeline remains identical.

### Step 1 — Gather Transcripts

Search Notion for today's meeting transcripts:
- Use the Notion MCP to query the meeting notes database for today's date
- Retrieve each transcript's title, participants, and content
- Filter: **exclude internal-only meetings** (all attendees from the same company domain)
- Only include meetings with at least one external participant

### Step 2 — Distill Each Transcript

For each qualifying meeting, extract:
- Decisions made or action items assigned
- Customer pain points, blockers, or risks
- Product feedback, feature requests, or competitive mentions
- Deal/relationship status signals (positive or negative)
- Anything surprising or escalation-worthy

Be specific: include names, product features, dates, and metrics when mentioned. Skip pleasantries, scheduling logistics, and small talk.

### Step 3 — Synthesize the Digest

Combine all distilled transcripts into a single digest following the output format below. Do NOT structure by individual meeting — synthesize across conversations to surface patterns, signals, and notable moments.

### Step 4 — Post to Slack

Post the finished digest to the dedicated meeting digest Slack channel using the Slack MCP.

## Transcript Corrections Dictionary

Speech-to-text frequently garbles domain-specific terms. Apply corrections when writing the digest. Common patterns:

- Correct product names, company names, and industry terms that sound similar
- Watch for your own company name being garbled (e.g., similar-sounding words)
- Industry-specific terms (accounting standards, ERP systems, partner/integration names) are frequently mistranscribed
- When in doubt, match against known customer/prospect names from `chief-context/company.yaml`

> **Customization:** Add a `transcript-corrections.yaml` file to this skill directory with your company's specific corrections dictionary. Format:
> ```yaml
> corrections:
>   - mistranscribed: "Cloud Code"
>     correct: "Claude Code"
>     notes: "AI coding tool"
> ```

## Company Name Formatting

- Each meeting should be tagged with the company name and whether they are a **(customer)** or **(prospect)**
- Cross-reference against HubSpot via the HubSpot MCP if the tag is missing
- Bold the company name in every bullet: **Company Name**
- After the bold name, add the tag: (customer) or (prospect)
- Example: **NoHo Commerce** (customer) — Dana's multi-entity consolidation workflow approved
- Example: **Sentinum Finance** (prospect) — Sarah positioned the platform for multi-entity rollout

## Output Format

Use Slack mrkdwn formatting. Bulleted, skimmable, no per-call or per-customer sections.

### Required Sections (in this order)

**:trophy: WINS & ACHIEVEMENTS**
Positive outcomes, approvals, momentum, successful demos, deals advancing.

**:warning: RISKS & CONCERNS**
Blockers, dissatisfaction, churn signals, delays, unresolved issues.

**:thought_balloon: SENTIMENT PATTERNS**
Cross-conversation mood, recurring themes, shifts in tone or confidence.

## Rules

- If there are no transcripts or content to review, say so. Do not fabricate content.
- Every bullet must explicitly reference a customer or prospect by name.
- Do not summarize or structure content by individual call or meeting.
- Focus on cross-conversation patterns, signals, and notable moments.
- Keep bullets short and factual. No narrative paragraphs.
- Limit to 6-8 bullets per section. Include at least one specific detail (product name, feature, competitor, metric, or quote) per bullet.
- Sentiment patterns must reference specific companies and signals. No abstract observations.
- Do not include observations about internal team workload or bandwidth.
- If Notion is unavailable, tell the user what's missing and suggest they paste transcripts directly.
- If Slack is unavailable, output the digest as markdown for the user to post manually.

## MCP Dependencies

| MCP Server | Role | Required? |
|-----------|------|-----------|
| **Notion** | Source meeting transcripts from the meeting notes database | Primary source (can be bypassed if user pastes transcripts directly) |
| **Slack** | Post the finished digest to the dedicated channel | Optional — outputs markdown if unavailable |
| **HubSpot** | Cross-reference company names for customer/prospect tagging | Optional — uses meeting metadata if unavailable |

> **Upgrading the pipeline:** To eliminate the Notion step entirely, connect a meeting recorder with MCP support (e.g., Grain, Fireflies). The recorder's MCP would replace the Notion transcript query in Step 1, feeding transcripts directly. Steps 2-4 remain unchanged.

## Composition

- `/chief-board` can pull from this skill for a "customer voice" section in board materials
- `/chief-escalation` can cross-reference digest signals with support ticket patterns
- `/chief-competitive` can extract competitive mentions from meeting transcripts
