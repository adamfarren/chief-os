# Test Analysis: unslop

## Test Scenario

Two scenarios, run against the Horizon Health test context.

Scenario A, audit mode. The user pastes a Horizon Health internal announcement for
the Agent SDK launch and says "unslop this, it reads like ChatGPT wrote it." The
draft carries 16 planted violations spanning every pass in the skill, plus two
traps. The first trap is a quoted customer testimonial containing an em dash and a
sentence fragment, which must survive untouched. The second is a vague claim
("adoption has been strong") that cannot be fixed without a number the draft does
not contain, which tests whether the skill fabricates one.

Scenario B, setup mode. The user runs `/unslop --setup` with four pasted Slack
messages, which is below the floor the skill sets for a usable sample.

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Loads the user's ruleset first, falls back to defaults | **PASS** — Checked `~/.claude/anti-ai-writing-style.md`, found none, used `references/default-rules.md` and disclosed the fallback at the end |
| 2 | Catches banned words | **PASS** — Found all 7: seamless, leverage, unlock, streamlines, robust, ecosystem, stuff |
| 3 | Catches em dashes in the author's prose | **PASS** — Flagged the Para 2 em dash |
| 4 | Does NOT strip the em dash from quoted customer material | **PASS** — Block quote left verbatim, and the row explicitly records it as "not a violation" rather than silently skipping it |
| 5 | Catches banned sentence patterns | **PASS** — "isn't just X, it's Y", "Not only X, but also Y", the "In summary" trailing summary, and "Let me know if you have any questions!" |
| 6 | Catches fragments and captions | **PASS** — "Two design partners, both live." and "That changed everything." |
| 7 | Does NOT flag the page title as a fragment | **PASS** — Heading row records the title exemption explicitly |
| 8 | Catches colon-fragments and label-colon lines | **PASS** — "The result: 40%..." and "Status: on track." |
| 9 | Catches bold lead-ins | **PASS** — "**Why this matters.**" flagged, and the fix removes the line rather than rewording the label |
| 10 | Catches rule-of-three and AI-cadence connectors | **PASS** — "faster, cheaper, and easier", the closing triple, and "What matters here is that" |
| 11 | Comments on rhythm across the whole draft | **PASS** — Noted uniform 18–22 word sentences, which is the one finding that needs the full draft in view rather than a line match |
| 12 | Refuses to fabricate a missing specific | **PASS** — "Adoption has been strong" flagged as having no clean fix, and the rewrite carries a bracketed NEEDS NUMBER placeholder instead of an invented figure |
| 13 | Preserves all claims, numbers, and names | **PASS** — 87 customers, 40%, February, Cascade Wellness, Northstar Orthopedics, Dana Reyes, and Marcus Webb all intact and unchanged |
| 14 | Violation table quotes verbatim text | **PASS** — Every row quotes findable text from the input |
| 15 | Rewritten draft passes its own seven passes | **PASS** — No banned words, no fragments outside the quote, no colon-fragments, no bold lead-ins, no trailing summary |
| 16 | No trailing summary under the rewrite | **PASS** — Output ends with the fallback note, not a recap of the edits |
| 17 | Varies sentence length in the rewrite | **PASS** — Rewrite runs from 9 to 31 words per sentence against the input's flat 18–22 |
| 18 | Setup mode refuses an inadequate sample | **PASS** — Stopped at 4 samples, stated that the output would be a guess, and explained that a guessed voice file is worse than none because it teaches the model patterns the user does not have |
| 19 | Setup mode asks whether samples were AI-drafted | **PASS** — Asked before analysing, and excluded the one the user identified |
| 20 | Setup mode wires the import line | **PASS** — Named both files, gave the `@~/.claude/anti-ai-writing-style.md` line, and stated that it takes effect next session rather than immediately |

## Overall Grade: A

The skill's real value shows up in the two negative cases rather than the catches.
Criterion 4 and criterion 12 are the ones a naive implementation fails, because
the obvious way to build this is a find-and-replace over a banned list, and that
approach quietly rewrites a customer's words and invents a number to patch a vague
claim. Recording the customer quote as an explicit non-violation row is the right
behavior, since it shows the user the skill looked and decided rather than missed.

The pass ordering earns its place. Rhythm and the positional sweep produced two
findings that no line-level match would have caught, and running them last meant
the mechanical noise was already cleared.

## Issues Found

- **None material.**
- **Minor:** The rewrite's bracketed `[NEEDS NUMBER: ...]` placeholder is the right
  call but it leaves the user with a draft they cannot ship as-is. Offering to
  query the source system for the figure, when a relevant MCP is connected, would
  close the loop instead of handing the problem back.
- **Minor:** The heading exemption row and the block-quote row both report "not a
  violation," which is useful on a 16-violation draft and would be noise on a
  50-violation one. A longer draft should collapse these into a single line naming
  what was checked and left alone.
- **Enhancement:** Audit mode has no severity ranking. A draft going to the board
  and a Slack message do not deserve the same treatment, and asking for the
  destination up front would let the skill drop the low-stakes findings.
