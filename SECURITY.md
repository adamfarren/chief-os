# Security Policy

## What this project is

Chief OS is a package of Claude Code skills that orchestrate reads and writes against connected services (Slack, Notion, HubSpot, Pylon, Grain, Google Workspace, Figma, Atlassian, Sentry, and more) via MCP servers. It runs in your local Claude Code environment and uses **your own** MCP credentials — this repo does not ship or request any credentials of its own.

## What to keep out of forks and PRs

Before committing changes, confirm none of the following are present:

- API keys, OAuth tokens, bearer tokens, webhook URLs, service-account JSON
- `.env` files or any file containing secrets (`.gitignore` already excludes `.env` and `.proprietary-terms` — keep it that way)
- Slack workspace URLs, channel IDs (`C...`), user IDs (`U...`), or Slack canvas IDs
- Notion workspace slugs, database IDs, or page IDs for real company data
- HubSpot/Pylon object IDs tied to real customers
- Jira project keys or ticket IDs from private projects
- Employee names, emails, comp data, or any PII
- Customer names, deal sizes, ARR figures, or internal metrics
- Figma file keys for proprietary design systems

If you fork this repo for internal use, put all of the above in `chief-context/company.yaml`, `chief-context/org.yaml`, and `chief-context/voice.yaml` in your **private** fork — never in this public repo.

## Data handling by skills

Skills in this repo read from and write to third-party services via MCP. A few things to understand:

- **Writes happen only after explicit user confirmation.** Publishing to Slack, creating Notion pages, updating HubSpot objects, etc., are gated on the user saying "ship it" / "publish" / equivalent. Do not remove these gates in your fork without understanding the consequences.
- **Log redaction is your responsibility.** Claude Code transcripts may include excerpts of fetched content. If you pipe transcripts to third-party storage, redact accordingly.
- **The router skill (`chief`) runs an MCP health check on startup.** This check pings configured MCP servers and reports status. It does not transmit credentials.

## Reporting a vulnerability

If you find a security issue in this repo — code that could leak credentials, prompt-injection vectors that could coerce a skill into an unintended write, or anything else that affects the safety of users running these skills — please report it privately.

Use GitHub's private vulnerability reporting at
`https://github.com/adamfarren/chief-os/security/advisories/new`

Please do **not** open a public issue for security reports. Do not include real credentials or customer data in your report — use redacted or synthetic examples.

### What to include

- A description of the issue and its impact
- Steps to reproduce, including the skill(s) involved and the MCP configuration if relevant
- Any suggested mitigation

### Response expectations

This is a solo-maintained project. Expect an acknowledgement within 7 days and a fix or decision within 30 days for valid reports. Critical issues will be prioritized.

## Supported versions

This project does not ship versioned releases — `main` is the supported branch. Pin to a commit SHA if you need reproducibility.
