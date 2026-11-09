---
name: yh-productmoat
description: Spawn the strongest model available in the toolkit as an OUTSIDER auditor to answer, for a product, the fundamental moat questions - what problem it fundamentally solves, the specific industry/technical term for it, whether demand is validated in existing named market data, what the category frontier is and what the product must do to match it, and how its value should be shown to a user so it lands intuitively - ending in a verdict. Use when the founder asks "what are we fundamentally solving", "what is this called", "is this validated", "what's the frontier", "how do we show the magic", "product moat", "verdict bro", or wants an outsider read on the product's position. Invoke with /yh-productmoat.
---

# /yh-productmoat - Outsider product-moat audit, run by the strongest model

## What this skill does

It does NOT answer the questions itself. It spawns the **strongest model available in the current
toolkit** as a fresh-context outsider auditor, hands it the six questions below and the product's
real sources, lets it do market research, then re-checks what comes back before relaying it.

An outsider with no stake and a fresh context sees the product the way a buyer or an investor
does. The session that built the product cannot: it knows the internals too well and has absorbed
the founder's vocabulary.

## Step 1: pick the strongest model

Look at the models the `Agent` tool accepts right now (its `model` option) and pick the most
capable one. As of 2026-09 that is **Fable 5.1** (`model: "fable"`), then Opus. Never default to a
smaller model to save cost, since this is a one-shot high-stakes read. Say in chat which model you
picked, in one line. Use a general-purpose agent type, which needs file reading plus web
search/fetch.

## Step 2: ground the brief (do this before spawning)

Find and list the product's own sources of truth, and check that each path exists:
- The strategy, positioning and user-journey docs. For Kavela this is `kavela/highlevel/`: start at
  `README.md`, then `what-we-are.md`, `code-reality.md` and `open-decisions.md`, plus the founder's
  current memories.
- Which framing is CURRENT, and which older framing must be ignored. For Kavela: agentic workflows
  for businesses, coding work first (`what-we-are.md`), never the old builder/marketplace or
  business-OS stories.
- Where the real product lives (backend and frontend source dirs), plus the newest live E2E
  write-ups, so the auditor can check claims against what the product actually does.

## Step 3: spawn the auditor with exactly these questions

Brief it as a skeptical outsider who has seen a hundred pitches in this space and has no stake.
The prompt must be self-contained, because it has none of your context. Ask, in order:

1. **Fundamentally, what problem is this solving?** One or two plain sentences a buyer would say,
   not the founder's vocabulary.
2. **What is the specific technical / industry term for what this is?** The category name that
   analysts, VCs and buyers actually use. Rank the candidates and say which one a buyer searches for.
3. **Is demand for it validated in existing market data?** Current evidence from credible NAMED
   sources (analyst reports, funding rounds and valuations of the closest companies, public
   revenue or usage, buyer surveys, buyer complaints). Each with source, date and URL. Hard
   numbers separated from hype. Say where evidence is thin or the category is contested.
4. **What is the frontier of this category right now, and what must the product do to match or
   beat it?** Concrete, ranked by importance: the capability, who has it, and whether the product
   has it today (with file paths or evidence).
5. **Intuitive brilliance: how should the value be shown to the user so it lands in seconds?**
   The "oh, this is different" moments, what the surface should show and hide, and where the
   current surfaces help or get in the way. Grounded in the real UI code or screens.
6. **Verdict.** One paragraph: is there a real, defensible product? The single biggest risk, and
   the single highest-leverage next move.

Rules to put in the brief:
- **Zero fabrication.** Every market claim needs a named, dated source with a URL, or it says "no
  source found". No invented numbers, customers or quotes.
- **Trust the code over the docs** where they disagree, and say so.
- **Read-only.** No file edits.
- **A tight report:** about 1,200-1,800 words, the six numbered headings, sources inline, no
  emojis, no em-dashes.

Run it in the background. Do not do the same research yourself while it runs, since that
duplicates it and biases the read.

## Step 4: check before relaying (auditors hallucinate too)

When it returns:
- Spot-check the **citations**. Open the 3-5 most load-bearing URLs (the ones the verdict rests
  on) and confirm they exist and say what is claimed. Drop or flag any that don't.
- Spot-check the **code claims**. For each "the product has X" or "lacks X" that drives a
  recommendation, confirm it in the code (file:line). Correct it if wrong.
- Keep the auditor's verdict as its verdict. Do not soften it or argue with it; add a short
  "checked / corrected" note instead.

## Step 5: report

In chat, not as a pointer to a file:
- The verdict paragraph first.
- One or two lines each for the problem, the category term, how validated demand is (with the
  2-3 strongest sources), the top frontier gaps, and the top "show it" moves.
- The checked/corrected note.

Offer the full report as a durable artifact only if the founder wants to keep or share it.
