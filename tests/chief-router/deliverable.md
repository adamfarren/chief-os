# Router Test Results

## Test 1: "Prep me for my Battery Ventures meeting tomorrow"

**Routing Decision:** `/chief-fundraise` → `/chief-investor`

**Reasoning:** The request mentions a specific investor firm and a meeting. This is a fundraising context (meeting prep during an active raise). The router would:
1. First check the fundraise pipeline status via `/chief-fundraise` to understand where Battery Ventures is in the process (stage, prior conversations, outstanding follow-ups)
2. Then trigger `/chief-investor` to generate a full meeting brief (firm research, attendee profiles, rapport flags, pitch customization)
3. Both skills read from `/chief-context` for current metrics and positioning

**Workflow:**
- `/chief-fundraise` checks HubSpot for Battery Ventures deal record and prior meeting history
- `/chief-investor` generates the comprehensive brief with all 8 required sections
- Output: a complete investor brief contextualized within the fundraise pipeline

**Matches SKILL.md example:** Yes — the SKILL.md explicitly lists "Prep me for my Battery meeting" → `/chief-fundraise` + `/chief-investor`

## Test 2: "What's happening in support this week?"

**Routing Decision:** `/chief-escalation`

**Reasoning:** Direct match to escalation synthesizer. The phrase "what's happening in support" maps cleanly to the weekly escalation digest capability. No multi-skill composition needed.

**Workflow:**
- `/chief-escalation` pulls from Pylon (tickets), Slack (support channels), HubSpot (customer context)
- Produces the escalation digest with CEO-level filtering
- Output: weekly digest with metrics, escalations, at-risk accounts, build opportunities

**Matches SKILL.md routing logic:** Yes — single-skill route to the most specific skill.

## Test 3: "Analyze this term sheet and write a board memo recommending we sign"

**Routing Decision:** `/chief-deal` → `/chief-memo`

**Reasoning:** Two distinct tasks in one request: (1) analyze the term sheet and (2) write a board memo with the recommendation. These map to two skills that compose sequentially.

**Workflow:**
1. `/chief-deal` extracts terms, flags risks, models financial impact, produces the analysis
2. `/chief-memo` takes the deal analysis and writes a board-ready recommendation memo using the strategy memo format
3. Both read from `/chief-context` for current financial position and board context
4. Output: two documents — the deal analysis and the board recommendation memo

**Matches SKILL.md example:** Yes — explicitly listed as a composition example.

## Test 4: First-Time Setup Detection

**Scenario:** User runs `/chief` and `chief-context/company.yaml` has all empty fields.

**Expected behavior per SKILL.md:**
1. Detect empty context files
2. Welcome message: "Let's set up your Chief of Staff. I need some context about your company."
3. Walk through company.yaml, org.yaml, and voice.yaml setup interactively
4. Confirm: "Your Chief of Staff is ready. Try `/chief-investor [firm name]` or `/chief-memo` to get started."

**Routing Decision:** No sub-skill dispatch. Router handles setup directly, reading and writing the context files via `/chief-context` conventions.

**Matches SKILL.md:** Yes — explicitly defined in the "First-Time Setup" section.

## Test 5: Ambiguous Request

**Scenario:** User says "help me with the Sequoia situation"

**Expected behavior:** The router should ask a clarifying question rather than guessing:
- "I can help with that. Are you looking for:
  - **Investor meeting prep** — I'll generate a brief for your next Sequoia meeting (`/chief-investor`)
  - **Fundraise status** — I'll show where Sequoia is in the pipeline (`/chief-fundraise`)
  - **Board materials** — I'll pull together an update for Sequoia (`/chief-board`)
  
  Which one do you need?"

**Matches SKILL.md:** Yes — rule 4: "If unclear, ask."
