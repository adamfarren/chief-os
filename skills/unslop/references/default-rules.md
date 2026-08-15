# Anti-AI Writing Style

Default ruleset for the `unslop` skill. This is the fallback used when the user
has no personal `~/.claude/anti-ai-writing-style.md`. Their file always wins.

## Banned words

delve, harness, tapestry, leverage, robust, seamless, navigate, unleash,
elevate, pivotal, synergy, holistic, paradigm, ecosystem, journey, unlock,
streamline, optimize, empower, transformative, cutting-edge

Users are expected to add their own domain bans on top of this list, because the
generic set will not catch the words specific to their company. Positioning
language a company has deliberately moved away from belongs there, as does any
internal jargon that appears in a draft only when a model wrote it.

Vague filler nouns:
- "stuff" and "does stuff" are never acceptable. There is always a specific
  noun available: work, logic, components, details, operations.
- "things" should be replaced with the precise noun (items, points, changes,
  tasks, components). If "things" is genuinely the only natural fit, use it but
  say so rather than slipping it in.

## Banned sentence patterns

- "This isn't just X, it's Y."
- "Not only X, but also Y."
- "It's not about X. It's about Y."
- Opening with "Great question!", "Absolutely!", "Certainly!", "Of course!"
- Trailing summaries that restate what was just done ("In summary, we updated
  X, Y, and Z")
- "I hope this helps!" / "Let me know if you have any other questions!"

## Humanize

This applies to everything: chat replies, documents, wiki pages, Slack
messages, board material, marketing copy. There is no format where these stop
applying.

- **Write in complete sentences. Always.** A sentence needs a subject and a
  verb. "Two connections, both one-time." is not a sentence, it is a caption,
  and captions are how AI writes when it wants to sound punchy. The only
  exceptions are page titles, section headers, table column headers, and nav
  labels. Anything a person reads as a thought gets to be a real sentence.
- **No clipped fragment sentences for punch.** AI writes a full setup sentence
  and then a two-word fragment as the payoff ("That reshaped intake."). Fold it
  into prose that carries its own reasoning. If a sentence only works as the
  beat after the one before it, combine them.
- **No colon-fragment constructions.** "The result: fewer tickets." and "One
  catch: it only syncs daily." are the same tell in a different hat. Write "The
  result is fewer tickets."
- **No label-colon-value lines in prose.** "Status: broken." belongs in a
  table. In prose, say what is broken and why.
- **Vary sentence length.** AI writes every sentence the same length and
  resolves each one into a neat conclusion. Let some run long and explain, let
  others land plainly.
- **Break the reflexive rule-of-three.** "cheaper, faster, and fits a virtual
  model" is a reflex. Use two, or four, or a full sentence, when three is not
  actually the truth.
- **Every bullet gets a real second sentence**, a why or a concrete
  follow-through, not one clipped clause.
- **Kill AI-cadence connectors on sight:** "What matters here is that", "The
  common thread is", "That is the throughline", "at the intersection of",
  "genuinely" and "quietly" as filler, and any sentence that announces its own
  structure ("Six questions cut through the noise").
- **Read-back test.** If it sounds like a press release or a generic blog, it
  is not done. If it sounds like someone who knows the domain talking to a
  peer, it is right.
- **Say it out loud test.** Read the first line of every callout, bullet, and
  section back as if speaking it to the reader. If you would not say it that way
  out loud, rewrite it as the sentence you would actually say.

## Where the drift actually happens

The drift is positional and predictable, so more rules do not fix it and knowing
where to look does. Run the say-it-out-loud test hardest on these, in this order:

1. **Explanatory text inside generated artifacts.** Callouts, document intros,
   table captions, README sections. These read as interface copy rather than
   prose, so they slip past the check entirely. A note that opens "What this
   section is for." is the same violation as a chat message that opens that way.
2. **Summary sections at the end of a long response.** The pull to sound punchy
   is strongest here.
3. **Bold lead-ins anywhere.** A bold phrase followed by a period is a label
   pretending to be a sentence. If the bold text cannot stand as a clause with a
   subject and a verb, rewrite the whole line.
4. **Anything written late in a long session.** The further in, the more likely
   the last thing written has drifted. Treat session length as the risk signal
   and reread rather than assuming earlier compliance carries forward.

Fix these silently. Do not announce the correction and do not explain the
pattern back to the reader, just write it properly.

## Banned punctuation

- Em dashes and en dashes (the long ones). Use a regular hyphen instead.
- This covers the user's own writing only. Leave them alone in quoted source
  material, customer messages, meeting transcripts, existing documents the user
  did not write, code, and search results. Never rewrite someone else's words to
  strip one.

## Formatting

- Use bullets and tables aggressively over prose.
- Keep paragraphs to three sentences maximum.
- Never use horizontal rules between sections.
- No bold or italics for inline emphasis in informal output. Reserve formatting
  for headers and lists.
- Default to no comments in code.

## How I write

This section is a placeholder in the default ruleset and carries no rules,
because voice is the one part that cannot be shipped as a default. `--setup`
mode exists to fill it in from the user's real writing samples.

Everything above stops a model sounding like a model. Only this section makes it
sound like a specific person.
