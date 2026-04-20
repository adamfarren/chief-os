---
name: chief-style
description: Brand style guide and design system reference for your company. Provides the color palette, design tokens, typography, component patterns, CSS custom properties, and Tailwind mappings for building any branded UI. Use this skill whenever creating any UI, frontend, website, landing page, dashboard, presentation, document, slide deck, marketing material, or visual asset that should match your brand. Also trigger when the user mentions "brand colors", "style guide", "design tokens", "design system", or asks to build anything that should look on-brand. Integrates with the Figma MCP to pull the latest design tokens from a source file (configured in `chief-context/company.yaml` under `style.figma_file_key`), with a static fallback embedded below. When another chief-* skill or the frontend-design skill produces visual output, this skill is the canonical source for brand consistency.
user-invocable: false
allowed-tools: mcp__claude_ai_Figma__search_design_system, mcp__claude_ai_Figma__get_variable_defs, mcp__claude_ai_Figma__get_design_context, mcp__claude_ai_Figma__get_screenshot, mcp__claude_ai_Figma__get_metadata
---

# Style Guide

You are the brand and design system reference for your company. Every visual output — whether a React component, HTML page, dashboard, slide deck, or marketing asset — should follow this guide.

> **This file is a template.** Fork it and replace the example tokens below with your own brand's palette, typography, and component patterns. The structure is the contract; the values are illustrative.

## Before Building

1. **Check Figma for fresh tokens** (if available — see Figma Integration below)
2. If Figma is unavailable, use the static tokens embedded in this file
3. If the output involves writing (memos, LinkedIn, etc.), also read `chief-context/voice.yaml` for editorial voice

## Figma Integration

The source of truth for the design system should live in Figma. When the Figma MCP is available, pull fresh tokens before building.

### Configuration

Set your Figma file key in `chief-context/company.yaml`:

```yaml
style:
  figma_file_key: ""    # e.g., "abc123DEFxyz"
  node_map:             # optional: direct links to key sections
    colors: "0:1"
    typography: "4:356"
    logos: "5:160"
    templates: "4018:2"
    illustrations: "7:129"
```

Read that file before making Figma calls so the fileKey is resolved dynamically, not hardcoded here.

### How to Pull Fresh Tokens

**Get a screenshot** of any section:
```
mcp__figma__get_screenshot(nodeId="<NODE_ID>", fileKey="<from company.yaml>")
```

**Get metadata** (structural tree with token names, hex values, positions):
```
mcp__figma__get_metadata(nodeId="<NODE_ID>", fileKey="<from company.yaml>")
```

**Search the design system** for components, variables, or styles:
```
mcp__figma__search_design_system(query="color", fileKey="<from company.yaml>")
```

**Get design context** (reference code + screenshot) for a specific component:
```
mcp__figma__get_design_context(nodeId="<NODE_ID>", fileKey="<from company.yaml>")
```

### When Figma Returns Updated Values

If Figma returns tokens that differ from the static values below, **use the Figma values** — they represent the latest design decisions. Note the differences so the user is aware of drift.

### When Figma Is Unavailable

Proceed with the static tokens below. State briefly that you're using the embedded guide.

---

## Design Philosophy

Replace this section with your own brand voice. Example template:

> Our brand uses a {dark/light}-themed design language built on {background tone} with {accent color} accents. The palette conveys {adjectives — e.g., trust, modernity, clarity}.

Five principles to customize:

1. **{Theme direction}** — e.g., "Dark-first" or "Light-first". Define the default surface.
2. **{Primary accent behavior}** — Where the primary color shows up: CTAs, active states, brand moments.
3. **Layered depth** — Hierarchy through background shifts rather than heavy borders.
4. **Restrained semantic accents** — Reserve purple/green/orange for semantic states (info, success, warning).
5. **High text contrast** — Meet WCAG AA at minimum.

---

## Color System — EXAMPLE PALETTE (replace with your own)

### Base Colors (Backgrounds & Surfaces)

| Token    | Hex       | Usage                                      |
|----------|-----------|--------------------------------------------|
| `base01` | `#0B0D12` | Deepest background — app shell              |
| `base02` | `#14171F` | Card backgrounds, elevated surfaces         |
| `base03` | `#1E222C` | Input fields, wells, recessed areas         |

### Brand Colors

| Token             | Hex                    | Usage                                         |
|-------------------|------------------------|-----------------------------------------------|
| `primary`         | `#4F8EF7`              | Primary actions, links, key UI elements        |
| `secondary`       | `#7FB7FF`              | Secondary actions, hover states                |
| `primaryGradient` | `#4F8EF7` → `#7FB7FF`  | CTA buttons, progress bars, emphasis gradients |

### Text Colors

| Token           | Hex       | Usage                                       |
|-----------------|-----------|---------------------------------------------|
| `textBody`      | `#E6EAF2` | Primary body text on dark backgrounds        |
| `textSecondary` | `#FFFFFF` | Headings, emphasized text                    |
| `textTertiary`  | `#A8B0BE` | Muted labels, captions, helper text          |
| `textOnPrimary` | `#0B0D12` | Text on colored/primary backgrounds          |

### Accent Colors (Semantic States)

| Token      | Hex       | Usage                                    |
|------------|-----------|------------------------------------------|
| `accentInfo`    | `#4FD1E7` | Info states, highlights                   |
| `accentAI`      | `#A879EA` | AI/intelligence features                  |
| `accentSuccess` | `#5DD39E` | Success states, positive indicators       |
| `accentWarning` | `#F5A04B` | Warnings, attention-needed states         |
| `accentNeutral` | `#8A93A3` | Neutral/disabled, metadata, timestamps    |

### Border & Divider Colors

| Token         | Value                      | Usage                             |
|---------------|----------------------------|-----------------------------------|
| `border01`    | `rgba(255,255,255,0.06)`   | Subtle card edges, dividers        |
| `border02`    | `rgba(255,255,255,0.10)`   | Input field borders                |
| `border03`    | `rgba(255,255,255,0.15)`   | Hover-state borders                |
| `borderFocus` | `#4F8EF7`                  | Focus rings                        |

### Interaction States

| State    | Pattern                                                      |
|----------|--------------------------------------------------------------|
| Hover    | Lighten background by ~4-6% or use `base03` as hover surface |
| Active   | Use `secondary` as accent glow or underline                  |
| Focus    | 2px solid `primary` focus ring with 2px offset               |
| Disabled | Reduce opacity to 40%, use `accentNeutral` for text          |

---

## CSS Custom Properties

When building branded UIs, define these CSS custom properties. Prefix with your brand name (example uses `--brand-`):

```css
:root {
  /* Base */
  --brand-base01: #0B0D12;
  --brand-base02: #14171F;
  --brand-base03: #1E222C;

  /* Brand */
  --brand-primary: #4F8EF7;
  --brand-secondary: #7FB7FF;
  --brand-primary-gradient: linear-gradient(135deg, #4F8EF7, #7FB7FF);

  /* Text */
  --brand-text-body: #E6EAF2;
  --brand-text-secondary: #FFFFFF;
  --brand-text-tertiary: #A8B0BE;
  --brand-text-on-primary: #0B0D12;

  /* Accents */
  --brand-accent-info: #4FD1E7;
  --brand-accent-ai: #A879EA;
  --brand-accent-success: #5DD39E;
  --brand-accent-warning: #F5A04B;
  --brand-accent-neutral: #8A93A3;

  /* Borders */
  --brand-border-subtle: rgba(255, 255, 255, 0.06);
  --brand-border-default: rgba(255, 255, 255, 0.10);
  --brand-border-hover: rgba(255, 255, 255, 0.15);
  --brand-border-focus: #4F8EF7;

  /* Typography */
  --brand-font-family: 'Inter', system-ui, -apple-system, sans-serif;
  --brand-h1: 500 2.25rem/2.75rem var(--brand-font-family);
  --brand-h2: 500 1.875rem/2.25rem var(--brand-font-family);
  --brand-h3: 600 1.5rem/1.75rem var(--brand-font-family);
  --brand-h4: 500 1.25rem/1.5rem var(--brand-font-family);
  --brand-body1: 400 0.8125rem/1.25rem var(--brand-font-family);
  --brand-body2: 500 0.8125rem/1.25rem var(--brand-font-family);
}
```

---

## Typography

**Font family:** Replace with your brand font (Inter is a safe default for software UIs).

### Type Scale

| Style     | Weight        | Size              | Line Height       | Usage                       |
|-----------|---------------|-------------------|-------------------|-----------------------------|
| Heading 1 | Medium 500    | 36px / 2.25rem    | 44px / 2.75rem    | Page titles, hero text      |
| Heading 2 | Medium 500    | 30px / 1.875rem   | 36px / 2.25rem    | Section headers             |
| Heading 3 | Semi-Bold 600 | 24px / 1.5rem     | 28px / 1.75rem    | Card titles, subsections    |
| Heading 4 | Medium 500    | 20px / 1.25rem    | 24px / 1.5rem     | Widget headers              |
| Body 1    | Regular 400   | 13px / 0.8125rem  | 20px / 1.25rem    | Primary body text           |
| Body 2    | Medium 500    | 13px / 0.8125rem  | 20px / 1.25rem    | Emphasized body text        |

### Links

- Default: `primary` color
- Hover: `secondary` color with smooth transition
- Underline on hover, no underline at rest

---

## Component Patterns

### Buttons

- **Primary**: `bg-gradient-to-r from-[primary] to-[secondary]`, white text, rounded-lg, subtle shadow
- **Secondary**: Transparent with primary-color border, primary-colored text
- **Ghost**: No border, text in primary, hover background 10% primary

### Cards

- Background: `base02`
- Border: `1px solid border01`
- Border-radius: 12px
- Hover: Border lightens to `border02`

### Inputs

- Background: `base03`
- Border: `1px solid border02`
- Focus: `2px solid borderFocus`
- Text: `textBody`
- Placeholder: `accentNeutral`

---

## Contextual Output

Not every request needs the full guide. Match the depth of your response to the task:

| Task                            | What to provide                                                   |
|---------------------------------|-------------------------------------------------------------------|
| "What's our primary color?"     | Just the brand colors table                                       |
| "Build me a login page"         | Full guide: colors, type scale, component patterns, CSS vars      |
| "Make this card match brand"    | Card pattern + base/border colors + text colors                   |
| "What are our design tokens?"   | CSS custom properties block + color tables + type scale           |
| "What font sizes do we use?"    | Type scale table + CSS type scale block                           |
| "I need the logo"               | Pull screenshot from Figma logo node, provide export guidance     |
| "Slide deck / marketing asset"  | Pull screenshots from marketing/illustration nodes                |
| Figma URL shared                | Pull screenshot/metadata from Figma, cross-reference static tokens|

When composing with other skills (e.g., `/chief-linkedin` asks for a branded visual, or `frontend-design` is building a page), provide only the tokens and patterns relevant to that skill's output format.
