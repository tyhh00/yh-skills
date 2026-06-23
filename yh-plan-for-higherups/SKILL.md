---
name: yh-plan-for-higherups
description: Write a tight, bottom-up proposal that helps a PM or tech lead make a build-vs-buy, vendor, or architecture decision fast. Educates and de-risks the decision instead of announcing a conclusion: maps product goals to capabilities, compares options in a scannable side-by-side with a verdict column, separates validated-from-assumed, shows usage-based economics with a break-even and an upgrade trigger, and ends with a low-commitment ask. Use when packaging eng findings or research for higher-ups, pitching a provider or tool choice, or turning an investigation into a decision doc. Sibling to /yh-plan (which is the internal eng plan); this one is for upward communication. Invoke with /yh-plan-for-higherups.
---

# /yh-plan-for-higherups: the upward-proposal method

A discipline for writing the one-pager that lets a busy PM or tech lead decide in minutes. It is the inverse of an internal eng plan: the audience is the decision-maker, not the implementer. Your job is to **educate and de-risk their decision**, expose the tradeoff space, and make a recommendation with the reasoning visible enough to challenge. Not to announce what you already chose.

**The shape:** goals -> capabilities -> comparison -> proof -> economics -> ask. Lead with what we want to ship, end with a low-commitment yes.

## Prime directives

1. **Terse. Kill preamble.** Every sentence earns its place. No throat-clearing, no restating the obvious, no "in this document we will." If a higher-up has to wade, you have failed. Cut length ruthlessly.
2. **Educate over conclude.** Show the good, the bad, and the nuance of each option so the reader understands the tradeoff, not just your pick. A reader who only learns your answer cannot challenge it or own it.
3. **Comparison = scannable side-by-side with a verdict.** One row per capability, one column per option, a final Edge/verdict column readable in one pass. Never cram capability + limitation + competitor into a single cell. The reader should get the shape of the decision from the table alone.
4. **Validated vs assumed, always split.** Distinguish what you proved (tested live), what is documented but untested, and what is gated or unavailable. Ground every claim in a real test or source, never vendor marketing. This is what makes a higher-up trust it.
5. **Economics in their terms.** Total cost, how it scales with usage, the break-even between tiers, and the real cost lever (usually an architecture choice, not headcount). Favor a low-commitment, reversible posture: start small, prove the load, upgrade on a defined trigger.
6. **Name the limitations and open questions before the ask.** What you could not verify, what needs a vendor conversation, what to load-test first. Honesty here is leverage, not weakness.
7. **End with the ask plus why it is low-risk.** One concrete recommendation, the smallest reversible first step, and the sentence that says why saying yes costs little.
8. **No em-dashes. Use arrows (->) for flows.** Match the house voice.

## The standard sections

Adapt as needed, but this order works:

1. **Header** - title, author, audience, status ("Proposal for discussion, not a locked decision").
2. **What this is** - one or two sentences. The through-line: goals -> capabilities -> pricing -> best-fit.
3. **Assumptions: product feature mapping** - a table of what we want to ship, the data/primitive it needs, how the chosen option serves it, and the limitation. This is the spine of the proposal.
4. **Option vs option** - the scannable side-by-side with the Edge column, plus one takeaway line under it.
5. **The deciding factor** - the single insight the whole decision hinges on, with the measured evidence behind it.
6. **Validated vs assumed** - proven live / documented-not-tested / gated.
7. **Economics** - pricing table, why it is cheap for us, the cost lever, the break-even, the tier recommendation.
8. **Integration** - how each feature wires up, terse.
9. **Open questions before commit** - the honest list.
10. **The ask** - the recommendation and why it is low-risk.

## The bar

Terse over thorough · educate over conclude · scannable comparison with a verdict · prove it (validated vs assumed) · economics with a break-even and an upgrade trigger · honest limitations · low-commitment reversible ask · no em-dashes. Write the page a busy decision-maker can act on in five minutes.
