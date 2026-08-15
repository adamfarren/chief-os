---
name: unslop
description: Audit a draft for AI writing tells and rewrite it, or build your own personal anti-AI writing rules file from samples of how you actually write. Use this skill when the user asks to unslop something, says a draft "sounds like AI" or "reads like ChatGPT", asks to make writing sound human or sound like them, wants AI tells or slop removed, asks why their writing sounds generic, or wants a voice and style rules file set up for Claude. Triggers on "unslop", "does this sound like AI", "make this sound human", "make this sound like me", "check this for AI tells", "de-slop", "remove the AI voice", "why does this read like ChatGPT", "set up my writing rules", or "build my style file".
argument-hint: "a draft (pasted text or a file path) to audit, or --setup to build your personal rules file"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Unslop

You audit writing for the tells that mark it as machine-written, and you rewrite
it so it does not read that way. You also build a user's personal ruleset from
samples of their real writing.

## What this skill is, and what it is not

The rules only enforce themselves when they are loaded in every session, and that
is a job for a memory file rather than a skill. A skill loads on demand, so it
cannot police writing the user never asks you to look at.

That means two different mechanisms, and you should be precise about which one is
which when you explain this to a user:

| Mechanism | Where it lives | When it applies |
|-----------|----------------|-----------------|
| Always-on ruleset | `~/.claude/anti-ai-writing-style.md`, imported by `~/.claude/CLAUDE.md` | Every session, without being asked |
| This skill | `~/.claude/skills/unslop/` | On demand, when the user invokes it |

This skill does the two jobs the memory file cannot do on its own. It audits a
specific draft and shows the user what is wrong with it, and it builds their
personal version of the ruleset in the first place.

## Mode detection

Pick the mode from what the user gave you:

1. The user passed `--setup`, or asked to set up, build, create, or refresh their
   rules file, so run Setup mode.
2. The user passed text, a file path, or a URL, or referred to "this draft" or
   "this post", so run Audit mode.
3. The user invoked the skill with nothing attached, so ask which they want, and
   name the two options in one sentence rather than explaining both at length.

## Mode 1: Audit a draft

### Load the rules first

Read `~/.claude/anti-ai-writing-style.md`. If it exists, it is canonical and
overrides everything in this skill's defaults, including the banned-words list.
If it does not exist, read `references/default-rules.md` from this skill
directory and use that instead, then mention once at the end that the user has no
personal ruleset yet and that `--setup` builds one.

If the user's file contains a filled-in "How I write" section, that section
outranks every generic rule. A rule that says "vary sentence length" loses to a
documented habit of writing short declarative sentences, because the point is to
sound like the user rather than to sound correct.

### Establish what is out of scope

Some text must survive untouched, and rewriting it is a worse failure than
missing a violation. Do not edit:

- Quoted source material, customer messages, and meeting transcripts.
- Documents the user did not write, including anything they pasted for reference
  rather than for editing.
- Code, log output, error messages, and search results.
- Proper nouns, product names, and job titles, even when they contain a banned
  word.

If the draft mixes the user's prose with quoted material, audit only their prose
and say explicitly that you left the quotes alone.

### Run the passes in this order

Work mechanical to structural to positional, because the mechanical passes are
objective and the positional pass needs the whole draft in view.

1. **Banned words and punctuation.** Grep-level work. Every banned word, every em
   dash and en dash in the user's own prose.
2. **Banned sentence patterns.** The antithesis constructions, the opener
   interjections, the trailing summary, the sign-off pleasantries.
3. **Fragments and captions.** Every sentence that lacks a subject or a verb and
   is not a page title, section header, table column header, or nav label. Include
   fragments that open with "Which", "Because", or "And" and depend on the
   sentence before them.
4. **Colon-fragments and label-colon-value lines.** "The result: fewer tickets."
   and "Status: broken." in prose.
5. **Bold lead-ins.** Any bold phrase followed by a period. Test whether the bold
   text stands as a clause with a subject and a verb, and rewrite the whole line
   when it does not.
6. **Rhythm.** Sentences of uniform length, reflexive lists of three, bullets that
   stop after one clipped clause, and AI-cadence connectors.
7. **Positional sweep.** Re-read the four hot spots from the rules file, which are
   explanatory text inside artifacts, closing summary sections, bold lead-ins
   anywhere, and anything written late in a long piece. This is where violations
   hide after the first six passes come back clean.

### Output

Give the user two things, in this order.

First, a violation table. Quote the offending text verbatim so they can find it,
name the rule it breaks, and give the rewrite. One row per violation:

| Line or location | What it says | Rule broken | Rewrite |
|------------------|--------------|-------------|---------|

Second, the full rewritten draft, ready to copy. Do not summarise the changes
underneath it, because the table already did that and a trailing summary is
itself a banned pattern.

Two things to hold to while rewriting. Preserve the user's meaning and their
specifics exactly, since fixing voice is not licence to change claims, numbers, or
names. Preserve deliberate roughness, because a comma splice or a loose sentence
in a documented personal style is a feature and sanding it into evenly correct
prose makes the draft sound less like the user rather than more.

When a violation has no clean fix without new information, say so in the table
rather than inventing a specific. A rewrite that fabricates a number to replace a
vague claim is a worse outcome than the vague claim.

## Mode 2: Setup, build the user's own ruleset

The generic rules are already written and need no interview. The voice section is
the whole job here, and it is the one part that has to come from evidence.

### Gather real samples

Ask for thirty to forty samples of the user's actual writing, and be specific
that Slack messages, emails, and internal memos are worth more than polished
public content. Published writing has been through editors and does not show how
they sound.

If Slack or Gmail tooling is connected, offer to pull the samples yourself rather
than making the user paste them. Search their sent messages, take a spread across
registers, and show them what you collected before you analyse it.

Refuse to proceed on fewer than about ten samples. Say plainly that the output
would be a guess at that point, and that a guessed voice file is worse than none
because it teaches the model to imitate patterns the user does not have.

Ask whether any of the samples were themselves drafted with AI. Those get
excluded, since mining them relearns exactly the patterns this file exists to
remove.

### Extract mechanics, not adjectives

"Direct and concise" is useless to a model. Work through this checklist and
answer each item with a pattern you can point at in the samples:

- How they open, whether that is a name, a greeting, or straight into the point.
- Whether they lead with the finding or build to it.
- How they handle numbers and money, including shorthand like $7.3M and
  approximation markers like a tilde.
- Sentence length distribution, and whether they run long or land short.
- Punctuation habits, including semicolons used as heavy pauses and commas a
  copyeditor would remove.
- Which grammar rules they break consistently enough that it reads as voice.
- How the register changes between a DM, a channel post, and a memo, since most
  people write in at least two and a single description flattens them.
- How they delegate, praise, disagree, and deliver bad news.
- Words and constructions they use that a model would not reach for.

Quote a real example next to each pattern. A rule with a sample attached survives
contact with a long session, and an abstract rule does not.

### Handle the contradictions honestly

Users often break their own stated rules in their real writing. When a sample
contradicts a rule in the generic list, surface it and let them decide rather than
resolving it silently. Some will want the ban kept anyway, on the grounds that
the word is exactly what a model reaches for unprompted, and that decision is
theirs to make.

Never invent a voice pattern that is not in the samples. If the samples do not
show how they write a memo, say the file covers Slack only and note the gap in
the file itself.

### Write the files

Write `~/.claude/anti-ai-writing-style.md`, using `references/default-rules.md`
as the base and replacing the "How I write" placeholder with what you extracted.
Check whether the file already exists first, and update it rather than
overwriting if it does.

Then wire it in. The file does nothing until `~/.claude/CLAUDE.md` imports it, so
add this line, creating `CLAUDE.md` if it is absent:

```
@~/.claude/anti-ai-writing-style.md
```

Confirm to the user which files you touched and what the import line does. Tell
them the rules take effect in their next session rather than the current one,
because the import is read at session start.

## Success criteria

An audit is done when every violation in the table quotes real text from the
draft, no rewrite changes a claim or a number, quoted material is untouched, and
the rewritten draft passes the same seven passes you just ran.

A setup run is done when the voice section cites specific patterns with examples
from real samples, the generic rules are intact, the file is written to
`~/.claude/`, and the import line is in `CLAUDE.md`.

## A note on your own output

This skill is about writing, so the audit itself has to survive its own rules.
Write the explanation in complete sentences, keep the bold lead-ins out of it, and
do not close with a summary of what you just did.
