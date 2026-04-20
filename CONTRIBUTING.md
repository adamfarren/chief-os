# Contributing to Chief OS

Thanks for considering a contribution. Chief OS is a package of Claude Code skills that give you an AI Chief of Staff — memos, briefs, board materials, pipeline updates, and more. The goal is to stay generic enough that any founder or exec can fork, fill in their company context, and have a working Chief of Staff in minutes.

## Ground rules

- **No company-specific data in this repo.** Customer names, employee PII, internal Slack channel IDs, Notion page IDs, Jira tickets, or any data that identifies a real company belongs in your private fork — not in PRs to this repo.
- **Template-shaped contributions.** Any IDs, URLs, file keys, or workspace slugs should be read from `chief-context/company.yaml` or `chief-context/org.yaml`, not hardcoded.
- **Keep skills composable.** If a skill needs data from another skill, have it call that skill rather than duplicating logic.

## Quickstart for contributors

```bash
git clone https://github.com/<your-fork>/chief-os.git
cd chief-os
./install.sh --status         # see what's linked where
./install.sh                  # symlink public skills into ~/.claude/skills/
```

Edit SKILL.md files in `skills/<skill-name>/`. Changes go directly to the repo working tree (via the symlink).

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` with this frontmatter:

   ```markdown
   ---
   name: <skill-name>
   description: <one paragraph — what it does, when to use it, what triggers it>
   argument-hint: "<optional: shape of expected user input>"
   allowed-tools: <space-separated list of MCP tools this skill may call>
   ---
   ```

2. Add the skill to `PUBLIC_SKILLS` in `install.sh`.
3. Add a row to the router table in `skills/chief/SKILL.md` (`## Available Skills`).
4. Add a routing rule to the same file's `## Routing Logic` section.
5. Add a short description to `README.md` under the skill tree and the appropriate capability section.
6. Add a test scenario to `tests/<skill-name>/` with `deliverable.md` + `analysis.md`, using the fictional Meridian Ledger context.
7. Update `tests/README.md` with your test entry.

## SKILL.md frontmatter contract

| Field            | Required | Purpose                                                     |
|------------------|----------|-------------------------------------------------------------|
| `name`           | yes      | Must match the directory name                                |
| `description`    | yes      | First paragraph of what Claude sees when routing requests    |
| `argument-hint`  | no       | Shape/examples of the argument string the skill expects      |
| `allowed-tools`  | no       | Explicit allowlist of MCP tools; omit to allow all           |
| `user-invocable` | no       | `false` if only callable by other skills (default `true`)    |

## Testing

Each skill has a test directory under `tests/<skill-name>/` with:

- `deliverable.md` — the output the skill produces with the fictional context
- `analysis.md` — success criteria and grade

Re-run tests after significant changes by following `tests/README.md`.

## Commit style

- Use imperative present tense: "Add X", "Fix Y", "Generalize Z" — not "Added" or "Adds".
- Reference the affected skill in the message: "chief-style: swap hardcoded fileKey for config lookup".
- Keep commits focused — one skill or concern per commit.

## PR checklist

- [ ] No company-specific data (names, IDs, PII, internal URLs)
- [ ] SKILL.md frontmatter is present and correct
- [ ] Router table in `skills/chief/SKILL.md` is updated if the skill set changed
- [ ] Tests in `tests/<skill-name>/` updated to reflect behavior changes
- [ ] `install.sh` PUBLIC_SKILLS list updated if a skill was added or removed
- [ ] README.md reflects any new or renamed skills

## Questions or problems

Open an issue — use the templates in `.github/ISSUE_TEMPLATE/`.
