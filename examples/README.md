# Examples

These are fully filled-in fictional configs showing the intended shape of `chief-context/` data. The fictional company is **Meridian Ledger** — an AI-native accounting and financial close platform at Series B.

Use them as a reference when filling in your own `chief-context/company.yaml`, `chief-context/org.yaml`, and `chief-context/voice.yaml`.

## Files

- `company.example.yaml` — company strategy, metrics, initiatives, positioning, fundraising status
- `org.example.yaml` — leadership, teams, investors, board
- `voice.example.yaml` — editorial voice rules used by writing skills (memos, LinkedIn, etc.)

## How to use

After cloning the repo and running `./install.sh`, you have empty template files in `~/.claude/skills/chief-context/`. To get started quickly:

```bash
# Copy the fictional Meridian Ledger examples into your local chief-context
# (useful for exploring the system before filling in your real company)
cp examples/company.example.yaml ~/.claude/skills/chief-context/company.yaml
cp examples/org.example.yaml     ~/.claude/skills/chief-context/org.yaml
cp examples/voice.example.yaml   ~/.claude/skills/chief-context/voice.yaml
```

Then run `/chief-context` to review, or open the yaml files directly and replace with your real data.

## Important

- **Do not commit your real company data to any public fork of this repo.** The yamls in `chief-context/` inside your `~/.claude/skills/` are local to your machine only.
- If you're maintaining a private fork with your real data, keep your `chief-context/` content out of PRs back to this public repo.

The same fictional context is also used by the skill tests in `tests/test-context/` — feel free to mirror that pattern when adding your own test scenarios.
