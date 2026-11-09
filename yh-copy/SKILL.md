---
name: yh-copy
description: Write or fix any user-facing copy so it does not read as AI-generated, and get the positioning underneath it right. Use for landing pages, comparison pages, pricing pages, blog posts, emails, ads, launch copy, app store listings, in-product strings, and any rewrite where the ask is "make this sound human", "this reads like AI", "stop hedging", "make it punchier", or "why does nobody convert". Also use BEFORE writing marketing copy, to check whether the problem is the words or the positioning under them. Invoke with /yh-copy.
---

# yh-copy

Two jobs. Kill the AI tells, and make sure there is an argument underneath worth reading.

Distilled from the highest-starred anti-slop and marketing skill repos on GitHub (gathered in `kavela/agenttask/marketing-skills-gather/`), then bound to the Kavela design system, which already forbids most of this in section 10.

**The reason any of this matters:** a reader who clocks copy as machine-written discounts the CLAIM, not just the prose. A tell in the headline costs the argument.

---

## 1. The bans, in order of how badly they give you away

**1. "It's not X, it's Y."** The single most recognisable construction in AI writing. Every variant is banned:

```
banned   It's not just a CRM, it's a growth engine.
banned   Not a builder. A team.
banned   X hands you a builder. Kavela hands you a team.   (same move, negation implied)
banned   Passes, not passwords.
banned   The work lands as files, not as chat.
banned   You brief one manager, not sixteen workers.

instead  Say what you want. Kav works out who does it and briefs them.
```

Say the positive thing and stop. If the contrast genuinely carries information, put it in the reader's world: describe what happens to them, concretely, and let the difference be obvious without a rhetorical frame.

**2. The reflexive tricolon.** Three-item lists as the default rhythm. Fine once, damning as a pattern. "Faster, smarter, more reliable" says nothing; "it runs in under two seconds" says one thing.

**3. Metronomic sentence length.** Never three consecutive sentences of similar length. This is the most measurable detection signal there is. Mix a four-word sentence with a thirty-word one.

**4. Parataxis.** Short sentence. Then another. Then another. Reads like a poem and screams machine. Connect thoughts with subordinate clauses, conjunctions, semicolons. Show how ideas relate, do not just stack declarations.

**5. Both-sidesing.** Marketing copy that carefully weighs pros and cons reads as generated. Take a position. Acknowledge the counterpoint in one sentence at most, never with equal weight.

**6. Hedging.** Every hedge is a small confession. "Can help you potentially reduce costs by up to 30%" is four hedges in one line and the reader believes none of it. State it flat or do not state it.

**7. Benefits with no mechanism.** "Save time" is a wish. "Save time by auto-matching invoices to POs" is a claim.

**8. Audience by demographic instead of by state.** "For SMBs" tells nobody whether it is for them. "For teams still approving invoices in email" does.

**9. Claims with no referent.** Industry-leading, best-in-class, world-class, cutting-edge. These signal that nothing specific was available.

**10. Em dashes, and the summarising dash clause.** Kavela bans them outright, everywhere, including code comments.

**11. Question-then-answer openers** ("What if there were a better way? There is."), **the reassuring close** ("and that's what makes all the difference"), **one-word sentences for emphasis**, and **metadiscourse** ("here's why this matters", "the point is").

**12. Emoji as structure.** Every line opening with a tick or a rocket.

Full lexical kill-list: `references/banned-language.md`. Read it before writing.

---

## 2. Is it the words, or the positioning?

Rewriting copy that sits on broken positioning is redecorating a house with no foundation. Say so when you see it.

**Positioning is broken, not the copy, when:** strong copy variants all test flat; sales calls need a long explanation of what the thing even is; price objections dominate (wrong comparison anchor); or wins cluster in a segment nobody targets.

**The five inputs, in this order:**
1. **Competitive alternatives.** What they would actually do without you, including a spreadsheet, an intern, and nothing. Doing nothing leads most markets.
2. **Unique attributes.** What you have that those do not. Features, but also model, data, distribution, price structure.
3. **Value.** What those attributes let someone DO. Attributes are facts; value is the reason to care.
4. **Best-fit segment.** Who feels that value most. Positioning to everyone who could buy dilutes to nothing.
5. **Category frame.** The highest-leverage choice, because it sets the competitors, the expectations and the price anchor all at once.

**The statement:**
```
For [segment] who [the situation that makes them must-buy],
[product] is a [category frame] that [the one value claim],
unlike [primary alternative], because [the attribute that makes it credible].
```

**The test that matters: could the nearest competitor paste their own name into this clause?** If yes, it is decoration. Rework until at least the "unlike/because" pair is unpasteable.

Offer design and pricing structure: `references/positioning.md`.

---

## 3. What to do instead

- **Be specific.** "You paste your treasury address and it tells you you will run out of USDC in 47 days" beats "powerful analytics".
- **Show the artifact.** Write the replacement headline, not the note saying the headline is vague.
- **Real numbers only.** Three real numbers beat thirty invented ones. Never fabricate a figure, a quote, or an anecdote to get specificity; honest vagueness beats fake precision.
- **Name real things.** Verifiable names, products, dates.
- **Use contractions**, and let a sentence be ugly sometimes.
- **Include the friction.** The part that was annoying is the part that sounds human.

---

## 4. Kavela bindings (these override anything above on a Kavela surface)

- **No em dash, no en dash, anywhere**, including code comments. Non-negotiable.
- **No emoji** in a product surface.
- **Model opacity is absolute.** Tiers are KAV-Lite, KAV-Pro, KAV-Max plus a capability framing. Never a real model or vendor name in copy a user can see, and never in a way that implies what powers a tier.
- **Never claim** compliance you do not hold (SOC 2, HIPAA, ISO 27001), self-hosting, on-prem, "fully autonomous", "no human needed", "replaces your team", or "guaranteed".
- **Examples must reflect real Kavela capability**: an agent with skills, connectors, containers, memory and projects, built by a maker and run by users on their own project. Not generic personal to-do automation.
- **Numbers must be real and current.** Verified today: 1,084 connector providers (`mcp-server/tn/connector-catalog/out/connector-providers.json`), 16 curated hires, six approval shapes, 100% skill retrieval under 200 skills.
- The design system's own list is section 10 of `KAVELA-DESIGN-SYSTEM.md`, and its section 11 hard-fail list governs the visual side.
- `scripts/lint_voice.py` is the mechanical check, but note it is scoped in CI to `content/blog` only.

---

## 5. Self-check, run before delivering anything

1. Any "not X, it's Y", in any disguise, including an implied negation across two sentences?
2. Three consecutive sentences of similar length?
3. Anything grouped in threes by reflex?
4. Any hedge that should be a flat statement?
5. Any benefit without its mechanism?
6. Any claim with no referent, no number, no name?
7. Any em dash, en dash, or emoji?
8. Did I weigh both sides evenly instead of taking a position?
9. Could a competitor paste their name into this and have it still read true?
10. Could any AI have written this for any company? If yes, it is not finished.
