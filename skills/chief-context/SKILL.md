---
name: chief-context
description: View and update the company context that all Chief of Staff skills depend on. Use this skill when the user says "update context", "update company info", "update metrics", "update org chart", "update voice guide", or any variation of updating the foundational company data. Also use when any other chief-* skill needs to read company context — this is the canonical source.
user-invocable: false
---

# Company Context Manager

You are the foundational context layer for the Chief of Staff system. Every other chief-* skill reads from the files you manage.

## What You Manage

Three YAML files in this skill directory:

1. **company.yaml** — Strategy, metrics, positioning, product architecture, current priorities
2. **org.yaml** — Org chart with names, roles, reporting lines, DRIs for each initiative
3. **voice.yaml** — Editorial voice, writing style, banned phrases, formatting preferences

## Commands

### View context
When the user runs `/chief-context` with no arguments or says "show context":
- Read all three YAML files
- Present a concise summary of current state
- Flag anything that looks stale (metrics older than 30 days, roles that may have changed)
- **Suggest relevant skills based on current state:** If fundraising status is "active", suggest `/chief-fundraise`. If an initiative is "at-risk" or "blocked", suggest `/chief-memo` for a strategy memo. If metrics are stale, prompt for an update before other skills consume outdated data.

### Update context
When the user provides new information (e.g., "ARR is now $18M", "we hired a new VP Sales named Maria"):
- Read the relevant YAML file
- Make the targeted update
- Show the diff to the user for confirmation
- Write the updated file

## YAML Schema: company.yaml

```yaml
company:
  name: ""
  one_liner: ""  # What the company does in one sentence
  stage: ""      # e.g., "Series B, preparing Series C"
  
metrics:
  arr: ""
  arr_growth_yoy: ""
  customers: ""
  burn_rate: ""
  runway_months: ""
  last_updated: ""

strategy:
  annual_goals:
    - name: ""
      dri: ""
      description: ""
  
  initiatives:
    - name: ""
      dri: ""
      status: ""  # on-track, at-risk, blocked
      description: ""

product:
  architecture: ""  # Brief description of technical architecture
  key_products: []
  differentiators: []

positioning:
  competitive_lanes: []  # Who you compete against and how you win
  key_narratives: []     # The stories you tell investors, customers, market

fundraising:
  current_round: ""
  target_amount: ""
  status: ""  # not-started, active, term-sheets, closing, closed
  key_metrics_for_investors: []
```

## YAML Schema: org.yaml

```yaml
leadership:
  - name: ""
    role: ""
    reports_to: ""
    owns: []        # Initiatives, functions, or domains
    context: ""     # Key things to know about this person

teams:
  - name: ""
    lead: ""
    members: []
    focus: ""

key_relationships:
  investors: []
  advisors: []
  board_members: []
```

## YAML Schema: voice.yaml

```yaml
editorial_voice:
  tone: ""          # e.g., "direct, conviction-led, analytical"
  sentence_style: "" # e.g., "short declarative sentences"
  
  formatting:
    preferred: []   # e.g., "numbered lists (1/ 2/ 3/)", "bold key claims"
    banned: []      # e.g., "em-dashes", "bullet points in posts"
  
  banned_phrases: []  # e.g., "flexible", "AI-first", "modern", "it's not X, it's Y"
  
  content_patterns:
    - name: ""       # e.g., "Product Showcase"
      structure: ""  # How this type of content is structured
      example: ""    # Brief example or reference

memo_preferences:
  format: ""        # e.g., "always markdown (.md)"
  max_length: ""    # e.g., "2 pages for strategy memos"
  structure_rules: [] # e.g., "no horizontal rules between sections"

investor_brief_preferences:
  rapport_flags: true  # Always surface shared sports/athletics connections
  format: ""
```

## Financial Data Sources

When updating financial metrics (ARR, MRR, customers, burn, cash, gross margin, etc.), pull live data from Google Sheets using `gws sheets +read`. Configure your spreadsheet IDs in `company.yaml` under a `financial_sources` key, or note them in a comment at the top of the file.

### Recommended sheet structure

| Sheet | Purpose | Key Data |
|-------|---------|----------|
| **Growth Forecast** | Full P&L and ARR bridge | Ending ARR, net revenue, gross margin, net income, cash, headcount, burn multiple — monthly actuals + rolling forecast |
| **MRR by Customer** | Revenue detail | MRR/ARR by customer, customer count, NRR |
| **Usage Metrics** | Product engagement | Monthly active users or events per customer, total platform usage |

### How to read them

```bash
gws sheets +read --spreadsheet <YOUR_SPREADSHEET_ID> --range "<Tab>!A1:CQ80" --format json
```

**Typical column layout for a Growth Forecast Dashboard:**
- Header rows contain fiscal year, quarter, and ACT/FCST labels
- Data columns start after frozen label columns; look for the last "ACT" column before "FCST" starts
- Key summary rows: Ending ARR, Active Customers, Net Revenue, Gross Margin %, Net Income, Ending Cash, Headcount FTE, ARR per Employee, Burn Multiple

**Typical column layout for MRR by Customer:**
- Row 1 = header; customer names in an early column; month columns run across
- Summary rows near bottom: Customer Count, Total MRR, Total ARR, Net Growth ARR, Growth %

**Typical column layout for Usage Metrics:**
- Row 1 = header; customer names in an early column; month columns run across
- Look for a total aggregation row near the bottom

### When to pull live data

- Any time the user says "update context", "update metrics", or "update financials"
- Before generating investor briefs, board materials, or pipeline updates
- When `last_updated` in company.yaml is more than 2 weeks old

Pull all sheets in parallel, then update company.yaml with the latest actuals.

## Rules

- Never hallucinate context. If a field is empty or missing, say so.
- When another chief-* skill asks for context, return only the relevant sections, not the entire file.
- When updating, preserve all existing data — only modify what the user explicitly changed.
- Timestamp every metrics update with `last_updated`.
- Financial metrics must come from live source sheets, not from memory or prior context.
