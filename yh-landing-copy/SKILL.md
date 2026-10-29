---
name: yh-landing-copy
description: The founder's rules for landing-page and marketing copy (and the product pictures beside it), learned the hard way on the Kavela landing. Use BEFORE writing or rewriting any landing headline, section title, lead line, feature row, pricing card, CTA or product-picture string, and as a self-check before showing copy to the founder. Bans opening on a comparison or a negative ("You don't X. You Y."), every "it's not X, it's Y" variant, the brand name in description text without approval, generic or familiar simplifications, welcome talk, and coloured text or icons on coloured backgrounds. Says the value the reader gets, as succinctly as possible. Invoke with /yh-landing-copy.
---

# /yh-landing-copy

Write as the founder's partner would after a 30-minute coffee chat about what Kavela can really do for the reader: no warm-up, no welcome, straight to the value they get.

## The rules (hard)

1. **Never open on a comparison or a negative.** No "You don't X. You Y.", no "No more X", no "Never X again", no "Stop doing X" as the first thing said. Open on what the reader gets.
   - Bad: "You don't build complicated flowcharts. You just tell Kavela what you want done, and it builds the routine for you."
   - Good: "One prompt gets you a running workflow, with the agents, apps and steps set up for you."

2. **Every variant of "it's not X, it's Y" is banned.** That includes "X, not Y", "not just X, but Y", "doesn't X, it Y", "less X, more Y", and "instead of X". State Y directly, with what it gets the reader.

3. **No brand name in description text without explicit approval.** Titles may carry it when the founder wrote it. Lines and descriptions say what the reader gets, so the subject is the reader or the thing they get, never "[Brand] does…".
   - Bad: "Kavela automatically picks the right AI workers."
   - Good: "The right AI workers are picked or created for the job, with the tools they need."

4. **Value first, as succinctly as possible.** One idea per line. Cut every word that does not change what the reader understands. The how-to belongs in demos, docs and the founder's channels, never on the landing ("Sell the value, not the how to").

5. **No over-generalising, and no simplifying into things the reader has already heard.**
   - Banned: "seamless", "powerful", "all-in-one", "supercharge" and "unlock"; "in plain English" or "in plain words"; "no code"; "AI that does it for you".
   - Name the concrete thing instead: the app, the result, the number, the place it lands.

6. **No welcoming.** No "Welcome to", "Meet", "Introducing", "Say hello to", "Imagine if", "Ready to…?" openers, and no throat-clearing before the value.

7. **No coloured text or coloured icons on a coloured background, ever.** That means no teal text on a teal tint, and no tinted icon tiles or tinted chips with coloured words.
   - State uses neutral chips with ink words.
   - Colour is allowed on a white or neutral ground for the product's own state words: "passed" in teal, "Working" in the Kav gradient.
   - A person's message is drawn in the product's real chat box (warm off-white input, hairline, dark send button), never a tinted bubble.

8. **Positive framing.** A capability is said as the gain, never as a fix for a weakness. Bad: "Deterministic code still gets its processes without bloating context." Good: "Your workflows pair agentic reasoning with code that runs the same way every time, so the agent's context stays clear for the decisions that need it."

9. **True, in the product's own words.**
   - Every claim must be something the product does today; check the code.
   - Product names are spelled as the product spells them: Agent Vault, Kav Mail.
   - Every number comes from its source, e.g. lib/pricing-v3.ts for plans; no invented stats.
   - Display artifacts (like a 60-day run strip) imply rather than state a stat. They never go in a title.

10. **House mechanics.**
    - No em or en dashes.
    - No emojis.
    - No eyebrow labels.
    - No colons in headings. An audience heading is two lines: who it is for in ink, the value in grey.
    - Titles in the founder's case style.
    - Hyphenated words kept whole across line breaks.

## How to work

- **When the founder gives the words, use them verbatim.** Only flag, in one line each, a line that is untrue in the product or breaks a rule above, and propose the closest true version.
- **When the founder gives a direction but not the words, write the shortest line that says the value.** Show it against the rules before shipping.
- **Never rewrite a line just to lower a readability score.** Readability is a check, not a goal; a lower grade that turns a line generic is worse.
- **Pictures beside copy reuse the approved composed fragments.** A context surface sits behind, the one surface the line is about in front, on the Kav glow. Never box-arrow-box, never decorative charts, never side-by-side audience columns.

## Self-check before showing anything

- Does the first sentence of every block say what the reader gets? (Not a comparison, not a negative, not a welcome.)
- Grep for "not ", "n't", "never", "no ", "instead", "rather than", "unlike", "just": is each one doing honest work, never framing?
- Does the brand name appear in any description line? Remove it unless approved.
- Could a competitor paste their name into this line unchanged? Then name the concrete thing.
- Is any coloured word or icon sitting on a tinted background? Make the ground neutral.
- Is every claim true today, and every number sourced?
