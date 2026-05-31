---
name: yh-plan
description: Rigorous product→engineering planning method for any non-trivial feature, sprint, or system change headed to production — especially multi-step work across real code. Phased and decision-locked: clarify product, ground every claim in real code (file:line), fence scope, lock each decision via ask_user_question with good/bad + one (recommended), produce PR-level plans (add-vs-edit, single-source-of-truth, no duplicate paths, unit + Playwright E2E), and on completion recap assumptions/grounding/structure/what's-new and spawn an outside auditor agent. Invoke with /yh-plan.
---

# /yh-plan — the planning method

A discipline for taking work to production. It trades speed-of-first-draft for **grounded, decision-locked, reviewable** plans. A wrong assumption compounds, so this method front-loads clarification and code-grounding: get the plan right *before* any code is written.

**The shape:** phases that pause for the user. You think → present a tight synthesis → **ask** → lock the answer → build on it → continue. This works *with* context limits on purpose — each cycle distills the user's real intent and stacks on the last, so a long plan stays coherent across many turns.

## Prime directives (every phase, no exceptions)

1. **`ask_user_question` for ANYTHING needing the user's input.** Never bury a decision in a prose prompt and hope they answer it. Batch open decisions into questions so the reply/ask loop is tight. If you catch yourself writing "should I X or Y?" in prose — stop, make it an `ask_user_question`.
2. **Every hard/complicated option gets good/bad + exactly one `(recommended)`.** State *why* each option is good or bad in real terms (liability, drift, cost, reversibility, UX, best-practice), then tag your pick. Trivial choices with an obvious default: just pick it and say so.
3. **Reasoning in the response text; decisions locked via questions.** Put analysis, tradeoffs, and findings in the message; convert the *fork* into an `ask_user_question`. After each answer, restate it as "locked" so the thread has a spine.
4. **Ground in real code before claiming anything.** Read the source-of-truth files, cite `file:line`, and *show* you've seen the exact code you'll modify. Never write a plan (or an audit) from memory or a subagent's unverified report — that is the #1 failure mode. Verify table names, columns, endpoints, and line numbers by direct read/grep.
5. **One thing at a time; continue after thinking.** Don't dump the whole plan. Research → present → ask → lock → write that piece → next. Keep going across turns.

## Phase A — Product planning (skip if already well-defined)

You cannot engineer a moving target. If the product model isn't crisp, plan the *product* first.
- Clarify, via `ask_user_question`: the **moat / positioning**, the **monetization model** (who pays whom), the **scope** (what's in / explicitly out), and the **core user journeys**.
- Lock each answer; build the next question on it.
- Capture the locked product decisions in a doc + memory before touching engineering.

## Gate A→B — is the product well-defined?

Proceed to engineering only when the moat, monetization, scope boundaries, and primary journeys are **locked and written down**. If the user's prior nudging already pins these (a clear product spec exists), **skip Phase A** and go straight to grounding.

## Phase B — Grounding (prove you saw the right code)

Before proposing changes:
- **Audit the actual code.** Grep + read the real files in the repo(s) in question. Map the current state: relevant tables, modules, endpoints, existing patterns.
- **Cite `file:line`** for everything you'll touch. Distinguish what *exists* from what you'll *add*.
- **Correct your own priors against the code** — if a doc/memory/assumption contradicts the code, the code wins; say so out loud.
- Produce a short **current-state ground-truth** section a reviewer can check.

## Phase C — Scope + assumptions

- **List every assumption** in chat (numbered); invite correction. Never proceed on a silent assumption.
- **Fence the scope:** what's in this sprint vs explicitly out, as a visible list. No silent scope creep; no silent narrowing of the original ask.
- For anything you'd remove/deprecate: **flag it (Cut / Relocate / Hide) and get explicit sign-off** — never a silent drop.

## Phase D — Decision-lock loop

For each open technical fork:
- Present options with **good/bad** grounded in real consequences (drift, liability, cost, reversibility, UX, best-practice).
- Tag one **`(recommended)`** with your reasoning.
- **`ask_user_question`** → lock the answer → restate it → let the next fork build on it.
- Validate "best practice / industry standard" claims against **current sources**, not memory.

## Phase E — PR-level engineering plan

Write the plan as discrete PRs. For each PR:
- **Goal** · **Add vs Edit vs Drop** (with `file:line`) · **what's done** · **tests** · a **user-usable hook** (a button on a bare test page that exercises it end-to-end) · **risks/sequencing**.
- **Single source of truth per concern; NO parallel/duplicate code paths** — extend existing functions behind flags/opts; one module per concern; cite the precedent if one exists.
- Bake in **reliability, SLA, auditability, modularization** (idempotency, transactions, structured logs, RLS).
- **Tests:** unit (CI-blocking) + **Playwright E2E** proving the user journey is never bugged/blocked — including permission-blockage where relevant. Note any **test fixtures the user must provide** (e.g. multi-user accounts) and request them just-in-time.
- Keep every edit grounded in real code; iterate in rounds with the user.

## Phase F — Completion ritual (on "plan marked complete")

When the user marks a plan (or a sub-task) complete, post a **final recap message** covering:
- **Assumptions** that underpin it (and which remain open).
- **Grounding** — the real SOT files you read, so a reviewer trusts it isn't invented.
- **Code structure** across the repo(s) — how the new pieces fit the existing architecture.
- **What's NEW** vs what's edited.
- **Why it's best-practice engineering** (the patterns + their justification).

Then **spawn an outside auditor agent** (the `Agent` tool, fresh context) to audit: does every cited `file:line` exist? is add-vs-edit correct? hallucination check, scope-fence check. Default to a **single** auditor; use a small multi-lens panel only if the user asks. **Re-verify the auditor's findings against the code yourself before acting** — an auditor can hallucinate too.

## The 10x bar (enforce throughout)

Ground first · product before engineering · clarify before writing · one decision at a time, locked and built upon · phased to respect context limits · single source of truth, no duplicate paths · explicit scope fences (no silent creep/narrowing/removal) · PR-by-PR with add-vs-edit + tests + user-usable verification · justify best-practice from current sources · outside-review before handoff.
