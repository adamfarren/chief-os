---
name: whiteboard
description: Create professional diagrams in FigJam using Mermaid.js. Applies brand colors from your style guide automatically. Use when the user asks to diagram, visualize, map, or draw — processes, workflows, architectures, user flows, state machines, timelines, decision trees, or any system or concept that benefits from a visual. Triggers on "draw", "diagram", "whiteboard", "visualize", "flowchart", "map out", "sequence diagram", "show me how X works", or "create a diagram".
user-invocable: true
allowed-tools: mcp__figma__generate_diagram, mcp__figma__get_variable_defs, mcp__figma__search_design_system, Read, Glob
---

# Whiteboard

You create clear, on-brand diagrams in FigJam. Every diagram should be immediately readable and visually consistent with the company's design system.

## Step 1: Get Brand Colors

Run these two sub-steps in parallel:

**1a. Read the local style guide** — try in order:
- `Read ~/.claude/skills/style/SKILL.md`
- `Read ~/.claude/skills/chief-style/SKILL.md`

From the file, extract the static color tokens AND look for a Figma file key (a line like `File key: <KEY>` or `fileKey="<KEY>"`).

**1b. If a Figma file key was found**, pull live tokens immediately — don't wait for 1a to finish:
```
mcp__figma__get_variable_defs(nodeId="4:43", fileKey="<KEY>")
```

**Priority:** Use Figma values when available — they reflect the current design system. If Figma is unavailable or returns no color data, fall back to the static tokens from the style guide file.

From whichever source wins, extract:
- **Primary color** — main brand color (buttons, key elements)
- **Secondary / accent color** — highlight, hover states
- **Base background color** — dark surface or page background
- **Text body color** — primary readable text
- **Semantic accents** — success (green), warning (orange), AI/intelligence (purple), info (cyan)

If no style guide is found, use this neutral tech-dark palette:

| Role       | Hex       | Usage                          |
|------------|-----------|-------------------------------|
| background | `#1e2030` | Default node fill              |
| primary    | `#4a90d9` | Key/start nodes, filled        |
| border     | `#5ba3ef` | Default node stroke            |
| text       | `#e8eaf0` | Node label text                |
| decision   | `#7b68ee` | Fork/decision node stroke      |
| success    | `#50c878` | Positive terminal nodes        |
| warning    | `#ffa552` | Risk or attention nodes        |

## Step 2: Choose Diagram Type

| User intent                                                   | Diagram type       |
|---------------------------------------------------------------|--------------------|
| Workflow, process, architecture, decision tree, data flow     | `flowchart LR`     |
| Top-down hierarchy, org structure, tree                       | `flowchart TD`     |
| API calls, user↔system interactions, time-ordered steps       | `sequenceDiagram`  |
| States, lifecycle, finite state machine                       | `stateDiagram-v2`  |
| Project timeline, roadmap, sprint schedule                    | `gantt`            |

Default to `flowchart LR` when the intent is unclear.

## Step 3: Build the Mermaid Syntax

### Color Styling

Color is only supported in `graph` and `flowchart` diagrams. Use it sparingly — reserve color for semantic roles, not decoration.

Define `classDef` blocks at the top of the diagram using the brand colors from Step 1:

```
classDef primary fill:<PRIMARY>,stroke:<SECONDARY>,color:#FFFFFF
classDef node fill:<BACKGROUND>,stroke:<PRIMARY>,color:<TEXT>
classDef decision fill:<BACKGROUND>,stroke:<ACCENT_CYAN_OR_SECONDARY>,color:<ACCENT_CYAN>
classDef success fill:<BACKGROUND>,stroke:<SUCCESS>,color:<SUCCESS>
classDef warn fill:<BACKGROUND>,stroke:<WARNING>,color:<WARNING>
```

Apply classes using `:::className` inline:
```
A["Start"]:::primary --> B{"Branch?"}:::decision
B -->|"Yes"| C["Process Step"]:::node
B -->|"No"| D["Done"]:::success
```

**Color assignment rules:**
- `primary` — entry points, hero nodes, the "main path" start
- `node` (default) — all standard process/action steps
- `decision` — forks, branches, conditional steps
- `success` — positive exits, completion, confirmed states
- `warn` — risk paths, error exits, attention-needed states
- Prefer dark fill + colored stroke over bright fills — it reads better at presentation scale and honors dark-theme design systems
- Do NOT apply color to `gantt` or `sequenceDiagram`

### Syntax Rules

- Put ALL node text and edge labels in double quotes: `["Node Name"]`, `-->|"Label"|`
- No emojis in Mermaid code
- No `\n` inside Mermaid syntax — use actual line breaks
- Default direction is `LR` for flowcharts unless top-down hierarchy is clearer
- Keep it simple: ≤ 15 nodes unless the user explicitly asks for detail

## Step 4: Generate

Call `mcp__figma__generate_diagram`:
- **`name`** — short, descriptive title (e.g., "Customer Onboarding Flow", "Auth Sequence")
- **`mermaidSyntax`** — the complete diagram code
- **`userIntent`** — what the user is trying to understand or communicate

**After the tool returns, always show the URL as a clickable markdown link.**

## Rules

- **Unsupported types** (class diagrams, ER diagrams, Venn, timeline): tell the user the type isn't supported and suggest the closest alternative
- **Font or positioning requests**: those require manual editing in Figma — share the URL and tell the user to open it there
- **Never call `create_new_file`** before `generate_diagram` — the tool creates its own file
- **Ask a clarifying question only if the subject is truly ambiguous** — prefer making a reasonable interpretation and showing the result; the URL lets the user iterate
