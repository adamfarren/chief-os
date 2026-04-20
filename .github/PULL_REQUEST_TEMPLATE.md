<!--
Thanks for opening a PR. A few quick asks before you submit.

DO NOT include company-specific data in this PR — no real customer names, employee PII, Slack/Notion/Jira IDs, or API keys. If your change requires such data, put it in your private fork instead.
-->

## What does this change?

<!-- One or two sentences. What did you change, and why? -->

## Which skill(s) does this touch?

<!-- e.g. chief-investor, company-update, chief (router) -->

## How to verify

<!-- How should a reviewer confirm this works? Include the prompt you ran, the expected output, or the test you updated. -->

## Checklist

- [ ] No company-specific data (customer names, employee PII, real IDs, credentials)
- [ ] `skills/<skill>/SKILL.md` frontmatter is correct if a skill was added or renamed
- [ ] `skills/chief/SKILL.md` router table and routing logic updated if the skill set changed
- [ ] `install.sh` `PUBLIC_SKILLS` list updated if a skill was added or removed
- [ ] `README.md` and `CLAUDE.md` updated if the skill surface area changed
- [ ] `tests/<skill>/` updated with fictional Meridian Ledger context if behavior changed
- [ ] Ran `./install.sh --status` locally and confirmed expected state

## Related issues

<!-- Link any issues this closes or relates to: e.g. Closes #12 -->
