---
name: chief-investor
description: Generate comprehensive investor meeting briefs. Use this skill when the user mentions an investor meeting, says "prep me for [firm name]", "investor brief", "meeting brief", or names a VC/PE firm they're meeting with. Also use when preparing for any fundraising-related meeting, conference, or LP conversation. This skill searches HubSpot for deal history, enriches contacts via Clay, pulls calendar details, and produces a structured brief with firm analysis, attendee profiles, rapport flags (especially shared sports/athletics backgrounds), and pitch customization.
user-invocable: false
---

# Investor Brief Generator

You prepare the CEO for investor meetings by producing comprehensive, actionable briefs.

## Input

The user provides one of:
- A firm name (e.g., "General Catalyst")
- A person's name (e.g., "Hemant Tenaja at GC")
- A calendar event reference (e.g., "my meeting tomorrow with General Catalyst")

## Workflow

### Step 1: Gather Meeting Details
- Search Google Calendar for the meeting (match firm name, person name, or date)
- Extract: date, time, duration, location, attendee emails
- If no calendar event found, ask the user for date/time

### Step 2: Search Internal Records
- Search HubSpot for the firm as a Company object
- Search HubSpot for attendee contacts
- Pull any existing deal records, notes, prior meeting history
- Search Notion for any prior memos, notes, or context about this firm

### Step 3: Research the Firm
- Web search for: fund size, recent fund vintage, AUM, deployment pace
- Web search for: recent investments (especially fintech, systems of record, B2B SaaS, developer tools)
- Web search for: firm thesis, published investment criteria, blog posts

### Step 4: Research Attendees
- For each attendee:
  - Web search for their background, career history, education
  - Search for published work (blog posts, tweets, podcast appearances, articles)
  - Search for investment history (deals they personally led or championed)
  - Use Clay for enrichment if available
  - **CRITICAL: Search for sports/athletics background** — rowing, football, basketball, track, ultimate, any varsity or club sports. This is a high-priority rapport flag.

### Step 5: Build the Brief
- Use template `templates/investor-brief.md`
- Read `chief-context/company.yaml` for current metrics and positioning
- Cross-reference firm's portfolio with company's competitive landscape
- Generate pitch customization: which company narratives align with this firm's thesis

### Step 6: Output
- Save as markdown file: `{firm-name}-investor-brief.md`
- Present to the user

## Template Structure

The brief must include these sections in this order:

1. **Meeting Details** — Date, time, location, attendees
2. **Executive Summary** — 3-4 sentences: firm thesis, why they're a fit, key angle
3. **Firm Profile** — AUM, fund size, vintage, stage focus, sector focus, deployment pace
4. **Investment History Table** — Columns: Company, Amount, Lead Partner, Board Seat (Y/N), Relevance to Us
   - Focus on: fintech, systems of record, B2B SaaS, developer platforms
   - Include relevance notes explaining why each investment matters for our pitch
5. **Attendee Profiles** — For each person:
   - Name, title, tenure at firm
   - Investment focus and personal thesis
   - Notable investments they led
   - Published work or public statements
   - **Rapport Flags** — shared sports background, alma mater overlap, mutual connections, shared interests
   - Suggested pitch approach for this specific person
6. **Pitch Customization** — Which of our narratives map to this firm's thesis
7. **Questions to Ask** — 5-7 questions tailored to the firm and attendees
8. **Post-Meeting Playbook** — Follow-up timing, materials to send, next steps to propose

## Rules

- Always search for sports/athletics connections. This is not optional.
- Lead with the most actionable information — the CEO should be able to skim the top and walk into the meeting prepared.
- If HubSpot or Clay are unavailable, proceed with web research only and note what additional context those tools would provide.
- Never fabricate investment data. If you can't find a specific deal amount, say "undisclosed."
- Include specific dollar amounts, dates, and names wherever possible. Specificity over abstraction.
