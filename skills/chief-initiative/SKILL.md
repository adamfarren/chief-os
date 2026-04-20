---
name: chief-initiative
description: Build the business case and pro forma financial model for a new line of business or strategic initiative. Use this skill when the user wants to evaluate a new LOB, write an initiative proposal, or build a financial model for a new business. Produces a structured memo covering thesis, strategic rationale, operating model, pro forma, legal structure, and risk analysis.
user-invocable: false
---

# New Initiative Builder

You build structured business cases and pro forma financial models for new lines of business or strategic initiatives.

## Before Starting

1. Read `chief-context/company.yaml` — current financial position, cash, burn, ARR, runway, strategic context
2. Read `chief-context/org.yaml` — for team members referenced in the initiative
3. If not provided by the user, ask:
   - What is the initiative? (brief description)
   - What is the business model? (unit type, revenue per unit)
   - Who leads it?
   - What is the budget envelope?

## Output

Use `/chief-memo` for all written deliverables. The business case memo has seven sections — build each one in order.

---

## Section 1: The Thesis

**What to include:**
- What is this LOB/initiative? One paragraph, plain English.
- What three things does it create that the core business cannot create any other way?
  1. A commercial proof point (revenue, margin, validated unit economics)
  2. A strategic asset (data, IP, customer relationships, market position, platform validation)
  3. An operational proof point (process, capability, or technology battle-tested in production)
- What must be true for this to succeed?
- Why now — what about the company's current stage makes this the right moment?

**Format:** 3–4 paragraphs, narrative prose. No bullets.

---

## Section 2: Strategic Rationale

The argument for why this initiative solves a problem the company already has — organizational, competitive, or strategic — beyond pure financial upside.

**What to include:**
- What specific problem does this solve? (talent retention, competitive positioning, customer proof, R&D environment, focus)
- What is the counterfactual — what happens if the company doesn't do this?
- Who in the organization does this affect, and how?
- How does this convert a current liability or constraint into an advantage?

**Format:** One problem per paragraph, narrative. This section is often what separates a compelling proposal from a generic business plan — the financial model can be built for any opportunity; the strategic rationale is specific to this company at this moment.

---

## Section 3: Operating Model

### 3a. Product/Service Selection

Answer these questions explicitly:
- What is the simplest version of this LOB that still proves the thesis?
- What maximizes speed to first revenue?
- What is the sequencing from initial product to mature product? (e.g., cash-pay → insurance, retail → enterprise, MVP → full stack — whatever applies to the LOB type)
- What regulatory, licensing, or contractual requirements constrain or gate the choice?

### 3b. Capability/Technology Stack

Map each core function of the LOB to how it gets done:

| Function | How It's Done | Status |
|----------|--------------|--------|
| [function 1] | [tool, agent, platform, or manual process] | [live / in development / to build] |
| [function 2] | | |

For each function, state:
- Automated, semi-automated, or manual?
- If automated: what is the tool or system, and is it production-ready?
- If manual: what is the staffing requirement, and what is the path to automation?

### 3c. Key Hire

The single most important hire for the initiative. Do not describe a committee — identify the one person whose presence or absence determines whether this works.

- Role title and reporting structure
- Why this person is critical (not just helpful) — what failure mode do they prevent?
- What they must be exceptional at
- What they do not need to be good at (counter-intuitive but important for the profile)
- Personality fit requirements relative to the initiative lead
- Compensation range and structure (base, variable, equity — and which entity pays each component)

---

## Section 4: Financial Structure

### 4a. Budget Table

| Line Item | Annual Cost | Notes |
|-----------|-------------|-------|
| [Lead role] | $X | [basis: market comp, reallocation, etc.] |
| [Key hire] | $X–$X | [range if not yet set] |
| Infrastructure / overhead | $X | [what's included, what's not] |
| **Total annual budget** | **$X** | |

### 4b. Classification

State explicitly how this initiative is classified and why that classification was chosen:
- Is it an R&D initiative, a standalone business, or a new product line?
- What gets disclosed externally vs. kept internal? To investors? To employees? To customers?
- Why does the classification matter — what are the specific consequences of the wrong classification? (fundraising narrative, employee perception, accounting treatment, customer trust)

---

## Section 5: Pro Forma Financial Model

Build a 24-month monthly model. **Always present two views:** excluding R&D/founding team cost (operational breakeven) and fully loaded (true economics including the leadership investment). Presenting only one view obscures either the business model viability or the real capital required.

### 5a. Define the Unit

Before building anything, name the unit the model tracks. This is the thing that generates revenue, requires delivery capacity, and compounds with retention.

Examples: Monthly Active Users (MAUs), active subscribers, active customers, enrolled entities, seats, locations.

Every line in the model should trace back to this unit.

### 5b. Unit Growth

The core driver of the entire model.

**Inputs:**
| Assumption | Value | Rationale |
|-----------|-------|-----------|
| Launch volume (Month 1 units) | X | [How you'll get to this number at launch] |
| Monthly new unit growth rate | X% MoM | [Comparable businesses, channel capacity, sales cycle] |
| Monthly retention rate | X% | [Nature of product: chronic/recurring vs. episodic/transactional] |

**Calculation:**
```
new_units(1) = launch_volume
new_units(month) = new_units(month-1) × (1 + growth_rate)

units(1) = new_units(1)
units(month) = units(month-1) × retention + new_units(month)
```

**Outputs to surface:** Units at Month 6, 12, 18, 24. If comparable data is available (benchmark customers, industry comps), state what percentile the projection lands at and whether the model is conservative, realistic, or optimistic relative to that benchmark.

**Retention is usually the highest-leverage assumption.** A 95% vs. 90% monthly retention produces dramatically different Month 24 outcomes. Always note the retention assumption prominently and justify it with product type — recurring/chronic products justify high retention; episodic/transactional products do not.

### 5c. Revenue

**Inputs:**
| Assumption | Value | Rationale |
|-----------|-------|-----------|
| Revenue per unit per month | $X | [Pricing basis: market rate, comparable businesses, negotiated rate] |
| Revenue model | [flat / tiered / usage-based] | |
| Pricing transitions (if any) | Phase 1: $X, Phase 2: $Y starting Month N | [What triggers the transition] |

**What's included:** Only the most defensible, easiest-to-collect revenue. Start conservative.

**What's excluded (list explicitly):** Revenue streams that are real but not modeled — these are upside cases. Excluding them keeps the base case defensible. Examples: upsells, secondary products, platform fees, consumption revenue, ancillary services.

**Calculation:**
```
revenue(month) = units(month) × revenue_per_unit
```

### 5d. Acquisition Cost

**Inputs:**
| Assumption | Value | Rationale |
|-----------|-------|-----------|
| Phase 1 CAC (Months 1–N) | $X | [Paid channels, sales comp, referral fees — before organic kicks in] |
| Phase 2 CAC (Month N+1 onward) | $X | [Lower: organic referrals, word-of-mouth, directory presence] |
| Step-down trigger | Month N | [What creates the organic flywheel — time, volume threshold, channel mix] |

**Calculation:**
```
acquisition_spend(month) = new_units(month) × CAC(current_phase)
```

Acquisition spend is an operating cost that scales with new unit growth, not a capital item.

### 5e. Direct Delivery Cost

The cost to deliver the product or service. For service businesses, primarily labor. For technology businesses, primarily infrastructure (COGS).

**Inputs:**
| Assumption | Value | Rationale |
|-----------|-------|-----------|
| Lead hire monthly cost | $X | [Fully loaded — includes benefits, taxes, equipment] |
| Capacity per delivery person | X units/person | [How many units can one person serve? This sets the scaling trigger] |
| Additional hire monthly cost | $X | [Each subsequent hire after the lead] |
| Hiring trigger | Add one hire when units/headcount > capacity | |

**Calculation:**
```
required_headcount(month) = ceil(units(month) / capacity_per_person)
delivery_cost(month) = lead_cost + max(0, required_headcount(month) - 1) × additional_hire_cost
```

Show headcount ramp alongside unit growth — this is usually the most scrutinized section of the model because it determines whether the delivery model scales economically.

### 5f. R&D / Founding Team Cost

The cost of the company resource(s) leading the initiative. Typically a senior person whose compensation is partially or fully allocated to the initiative.

Present two views:
- **Excluding R&D cost:** Shows whether the LOB itself is operationally viable. The business model works if this line is profitable.
- **Fully loaded:** Shows true economics and actual peak capital required. This is the honest view.

**Why two views:** The R&D cost is a strategic investment in capability — it funds the initiative's existence, not just its operations. Separating it makes the investment thesis clearer and prevents conflating "the business model doesn't work" with "we're investing in building it."

```
r_and_d_cost = [monthly allocation of founding team compensation]
```

### 5g. Overhead

**Inputs:**
| Assumption | Value | Notes |
|-----------|-------|-------|
| Baseline monthly overhead | $X | [Itemize if any line is >20% of total: insurance, compliance, tools, facilities] |
| Monthly growth rate | X% | [1–3% typical for slow-scaling operational overhead] |
| Exclusions | [list] | [Third-party platform fees not yet negotiated, items sized elsewhere] |

**Calculation:**
```
overhead(month) = overhead(month-1) × (1 + overhead_growth_rate)
```

### 5h. Monthly P&L

For each month, compute:

```
Revenue             = units × revenue_per_unit
Acquisition spend   = new_units × CAC
Delivery cost       = headcount model (5e)
Gross profit        = Revenue - Acquisition spend - Delivery cost
Gross margin %      = Gross profit / Revenue

Total costs (ex. R&D)      = Acquisition + Delivery + Overhead
Total costs (fully loaded) = Acquisition + Delivery + Overhead + R&D

Operating income (ex. R&D)      = Revenue - Total costs (ex. R&D)
Operating income (fully loaded) = Revenue - Total costs (fully loaded)

Cumulative net (ex. R&D)      = running sum of Operating income (ex. R&D)
Cumulative net (fully loaded) = running sum of Operating income (fully loaded)
```

### 5i. Key Milestones

Always identify and surface these four explicitly, in both views:

| Milestone | Ex. R&D | Fully Loaded |
|-----------|---------|--------------|
| Monthly breakeven | Month X | Month X |
| Cumulative payback | Month X | Month X |
| Peak cash invested | $X (Month X) | $X (Month X) |

- **Monthly breakeven:** First month where Operating income > 0
- **Cumulative payback:** First month where Cumulative net > 0
- **Peak cash invested:** The trough of Cumulative net — the maximum total capital at risk. This is the most important single output of the model. It answers: "what do we have to believe to write this check?"

### 5j. Point-in-Time Snapshot

Present a summary table at Month 24 (or the target horizon):

| Metric | Ex. R&D | Fully Loaded |
|--------|---------|--------------|
| Monthly revenue | $X | $X |
| Monthly costs | $X | $X |
| Monthly operating income | $X | $X |
| Operating margin % | X% | X% |
| Cumulative net | $X | ($X) |
| Annualized run rate | $X | $X |
| Units | X | X |
| Delivery headcount | X | X |

### 5k. Sensitivity Analysis

Test the model's most impactful assumptions. For each, show base case → stress case → change in key milestones.

**Always test these four:**

| Lever | Base Case | Stress Case | Impact on Monthly Breakeven | Impact on Peak Cash |
|-------|-----------|-------------|----------------------------|---------------------|
| Revenue per unit | $X | $X × 0.8 | +/- N months | +/- $X |
| Monthly retention | X% | X% - 4pp | +/- N months | +/- $X |
| Monthly growth rate | X% | X% ÷ 2 | +/- N months | +/- $X |
| CAC | $X | $X × 1.5 | +/- N months | +/- $X |

**Retention is almost always the most impactful lever** in recurring-revenue models. If retention is the key assumption, add a second row testing an additional downside (e.g., base - 7pp) to show the full range.

---

## Section 6: Questions to Stress Test

Two sets: questions to ask yourself (internal vulnerabilities) and questions to ask others (external dependencies).

### 6a. Questions to Ask Yourself

Identify the vulnerabilities in the proposal's own logic:
1. **Key person risk:** What happens if the lead hire doesn't work out, takes too long to find, or can't execute?
2. **Narrative risk:** Does this hurt the company's core story with investors, customers, or employees? If disclosed, what is the worst-case interpretation?
3. **Focus tax:** Does this initiative divert leadership attention from the core business at a time when the core business needs it most?
4. **Kill criteria:** What would you see at Month 3, 6, and 12 that would tell you this isn't working? What is the exit ramp — and what does it cost to exit?

### 6b. Questions to Ask Others

Organize by stakeholder. These are open questions that need answers before committing, not rhetorical — note the actual answer needed and who can provide it.

**Initiative lead:**
- What do they need to see in the financial model, timeline, or structure to opt in?
- What is their sequencing requirement — do they need the key hire first before they can build the model?

**Team leads (core business):**
- How does this affect their roadmap, priorities, or team capacity?
- What succession or coverage is needed for any responsibilities shifting to the initiative?

**Legal/compliance:**
- What entity structure is required?
- What licenses, certifications, or regulatory approvals are needed before launch?
- What liability exposures exist and who holds them?

**Board/investors:**
- What do they need to know, and when?
- Does this affect the fundraising narrative — and if so, how is it positioned?

**Customers/partners:**
- Could this be perceived as competing with them?
- How and when do key customers hear about this, and from whom?

---

## Section 7: Enterprise Structure

The legal and operational structure for the initiative. Do not skip this section — the structure determines tax treatment, liability, investor disclosure requirements, and cap table impact.

### 7a. Entity Options

Present the main structural choices:

| Structure | Description | Pros | Cons |
|-----------|-------------|------|------|
| Internal division | Operates inside the parent company | Simple, no legal overhead | No P&L separation, no spin-out optionality |
| Wholly-owned subsidiary | Separate LLC/Corp owned by parent | Clean P&L, limited liability, potential spin-out | Accounting complexity, intercompany agreements needed |
| JV or partnership | Co-owned with external party | Shared risk, complementary capabilities | Loss of control, complex governance |
| Regulated entity (e.g., licensed financial services entity) | Required in regulated industries | Regulatory compliance | Cannot be owned by parent in some jurisdictions |

### 7b. Ownership and Control

- Who owns the entity, and what does "ownership" mean if equity cannot be held by the parent (e.g., regulated professional entities)?
- If control is maintained through contracts rather than equity, what are those contracts and what do they guarantee?
- What prevents the operating entity from being transferred, sold, or redirected without the parent's consent?

### 7c. Key Agreements

List the legal documents required to make the structure work. For each, note the key commercial terms that must be addressed:
- Management Services Agreement (if MSO-PC or similar)
- Technology Licensing Agreement
- Transfer Restriction Agreement (if equity cannot be held)
- Employment agreements that reflect the dual-entity structure

### 7d. Financial Consolidation

- Does the initiative's P&L consolidate into the parent's financial statements?
- If so, under what accounting standard? (e.g., VIE consolidation under ASC 810)
- What are the implications for financial reporting, investor communications, and audit?

### 7e. Cap Table Impact

State explicitly:
- Does forming this entity require new equity issuance?
- Does it create dilution for existing shareholders?
- Are there warrants, options, or earnouts tied to the initiative's performance?

### 7f. Regulatory Flags

Check for any industry-specific structural requirements:
- Regulated industries (healthcare, financial services, legal, real estate): what entity structures are required or prohibited?
- Dual-actor risks: does the parent company's existing role (e.g., technology vendor, licensed entity) create conflicts of interest or compliance exposure if it also operates in this space?
- Data/IP firewalls: if the initiative has access to data from the parent's other customers or clients, what separation is legally required?

---

## Rules

- Always build the pro forma with two views: ex. R&D/founding team and fully loaded. Never present only one.
- Peak cash invested (trough of fully loaded cumulative net) is the most important single output — always surface it prominently.
- Every assumption must have a stated rationale. "We assumed X because Y" — never assert a number without basis.
- Sensitivity cases must include at least one scenario where the single most optimistic assumption reverts to a worse value.
- The thesis section must articulate what cannot be built any other way — a pure financial opportunity is not a strategic thesis.
- Classification (R&D vs. standalone business) is as strategic a decision as the financial model — treat it with the same rigor.
- Use `/chief-memo` for all written output.
