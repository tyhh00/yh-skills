---
name: yh-plan
description: Rigorous product→engineering planning method for any non-trivial feature, sprint, or system change headed to production — especially multi-step work across real code. Phased and decision-locked: clarify product (motivation-first journey), ground every claim in real code (file:line), fence scope, lock an assumptions checklist, lock each decision via ask_user_question with good/bad + one (recommended). Gates the work behind three hard checkpoints before any code — human-vetted architecture + user-journey diagrams, a zero-open assumptions lock, and a scoped production-readiness test plan — tracked by a STATUS lifecycle. Produces PR-level plans (add-vs-edit, single-source-of-truth, no duplicate paths, unit + Playwright E2E, a human-action split), and on completion recaps assumptions/grounding/structure/what's-new and spawns an outside auditor agent. Invoke with /yh-plan.
---

# /yh-plan — the planning method

A discipline for taking work to production. It trades speed-of-first-draft for **grounded, decision-locked, reviewable** plans. A wrong assumption compounds, so this method front-loads clarification and code-grounding, then gates the plan behind three hard checkpoints — **vetted diagrams, locked assumptions, a scoped test plan** — so the work is *right before any code is written*.

**The shape:** phases that pause for the user. You think → present a tight synthesis → **ask** → lock the answer → build on it → continue. This works *with* context limits on purpose — each cycle distills the user's real intent and stacks on the last, so a long plan stays coherent across many turns. The phases feed three **graduation gates** (Gate D→E); nothing graduates to code until all three pass, and a one-line **STATUS** always says which gate is unmet.

## Prime directives (every phase, no exceptions)

1. **`ask_user_question` for ANYTHING needing the user's input.** Never bury a decision in a prose prompt and hope they answer it. Batch open decisions into questions so the reply/ask loop is tight. If you catch yourself writing "should I X or Y?" in prose — stop, make it an `ask_user_question`.
2. **Every hard/complicated option gets good/bad + exactly one `(recommended)`.** State *why* each option is good or bad in real terms (liability, drift, cost, reversibility, UX, best-practice), then tag your pick. Trivial choices with an obvious default: just pick it and say so.
3. **Reasoning in the response text; decisions locked via questions.** Put analysis, tradeoffs, and findings in the message; convert the *fork* into an `ask_user_question`. After each answer, restate it as "locked" so the thread has a spine.
4. **Ground in real code before claiming anything.** Read the source-of-truth files, cite `file:line`, and *show* you've seen the exact code you'll modify. Never write a plan (or an audit) from memory or a subagent's unverified report — that is the #1 failure mode. Verify table names, columns, endpoints, and line numbers by direct read/grep.
5. **One thing at a time; continue after thinking.** Don't dump the whole plan. Research → present → ask → lock → write that piece → next. Keep going across turns.
6. **Diagrams and the test plan are GATES, not artifacts.** They are the things the approver actually reviews to say yes — not a nice-to-have you produce after deciding. No vetted diagrams, OR any open assumption, OR no vetted test plan → no graduation → no code. Treat them as load-bearing.

## Phase A — Product planning, motivation-first (skip if already well-defined)

You cannot engineer a moving target. If the product model isn't crisp, plan the *product* first — and plan it from the **user's motivation**, not the mechanics.
- Clarify, via `ask_user_question`: the **moat / positioning**, the **monetization model** (who pays whom), the **scope** (what's in / explicitly out), and the **core user journeys**.
- **Map each journey motivation-first.** For every surface the feature touches, map it from a *new* user's point of view: their **intent / the question in their head**, the **"natural why"** that makes them proceed to the next step, and the **friction** where the product fails to answer it. This is NOT a mechanical "given a click, what happens" state machine — the state machine is necessary but secondary. If a step has no natural why, that's a product hole, not an engineering detail.
- Lock each answer; build the next question on it.
- Iterate the high-level shape until the user signals it **"feels good"**, then capture the locked product decisions in a doc + memory before touching engineering.

## Gate A→B — is the product well-defined?

Proceed to engineering only when the moat, monetization, scope boundaries, and primary journeys are **locked, "feels good", and written down**. If the user's prior nudging already pins these (a clear product spec exists), **skip Phase A** and go straight to grounding.

## Phase B — Grounding (prove you saw the right code)

Before proposing changes:
- **Audit the actual code.** Grep + read the real files in the repo(s) in question. Map the current state: relevant tables, modules, endpoints, existing patterns.
- **Cite `file:line`** for everything you'll touch. Distinguish what *exists* from what you'll *add*.
- **Correct your own priors against the code** — if a doc/memory/assumption contradicts the code, the code wins; say so out loud.
- Produce a short **current-state ground-truth** section a reviewer can check.

## Phase C — Scope + assumptions-lock

- **Build an assumptions checklist** (numbered) — and treat it as a gate, not a list. Every item is marked either **verified-in-code (`file:line`)** or **confirmed-by-user**. Invite correction. The target is **zero open / unconfirmed assumptions** before code; an unmarked assumption is an open assumption.
- **Fence the scope:** what's in this sprint vs explicitly out, as a visible list. No silent scope creep; no silent narrowing of the original ask.
- For anything you'd remove/deprecate: **flag it (Cut / Relocate / Hide) and get explicit sign-off** — never a silent drop.

## Phase D — Decision-lock loop

For each open technical fork:
- Present options with **good/bad** grounded in real consequences (drift, liability, cost, reversibility, UX, best-practice).
- Tag one **`(recommended)`** with your reasoning.
- **`ask_user_question`** → lock the answer → restate it → let the next fork build on it.
- Validate "best practice / industry standard" claims against **current sources**, not memory.

## Gate D→E — Graduation gates (no code until all three pass)

The plan does not become engineering work until **all three** of these hard gates are met and the approver has signed off. This is the checkpoint between *deciding* and *building*. Skipping any one means the plan is **not** a true pass, no matter how good the prose is.

### Gate 1 — Human-vetted diagrams, TWO views (drawio or equivalent)

The diagrams are the gate, not a decoration. Author **both** views, get the approver to vet **both** as final:

- **(a) System architecture — how it's built.** It must **walk the flow**, not show static boxes: the **entry point(s)**, the **decision tree** (diamonds — say *when* each branch fires), the **effects/outputs** at each terminal, and the major **use-case flows** end-to-end. Shape vocabulary: stadium = entry/exit · rectangle = action · process-bar = container/external op · diamond = decision · document = file/artifact · cylinder = datastore · hexagon = credential.
- **(b) User journey — "what it actually does."** The functional path from the **user's** point of view, NOT the internals: the **starting input**, every **step**, every **decision** and which branch fires, and the **outcome** at the end of each path — the whole journey, **per persona / use-case**. Shape vocabulary: rounded-rectangle / stadium = start & end · rectangle = a step the product takes · **parallelogram = user input / what's shown to the user** · diamond = a decision/branch · document = an artifact the user receives.

Multi-page is expected: an orientation/decision page, one page per major architecture flow, **and** one page per major user journey. The approver vets **both** the architecture and the user-journey views.

### Gate 2 — Assumptions locked (zero open)

The Phase C checklist carries through with **zero open / unconfirmed items** — each marked *verified-in-code (`file:line`)* or *confirmed-by-user*. The approver signs off that the set is locked. One open assumption holds the gate.

### Gate 3 — Production-readiness test plan, scoped + vetted (the final gate)

Scope — end-to-end, before any code clears — the **highest-risk factors** and exactly what **must be proven** for production-scale readiness. Four parts, ALL required:

- **(a) Backend test plan.** Against a real/staging target (request the key/fixtures just-in-time): enumerate how each endpoint is stress-tested, a full **edge-case map**, and an explicit checklist of **≥10 core production-clearance checks** + **≥10 edge-case checks**. Each check states the **call, the input, and the expected result / pass-bar**. *Core* = the must-work-in-prod happy paths (auth, primary mutations/reads, metering, isolation). *Edge* = malformed input, limits/quotas, concurrency/races, auth failure, partial failure, abuse/exfil attempts.
- **(b) Frontend Playwright plan.** The exact UI click-path **per persona**: which page you navigate to, what you click (step by step), and the expected result at each step — driving the real browser on the correct account per role. No API-only "tests." (For the execution discipline, see `/yh-fe-integration`.)
- **(c) Design / theme & layout brief.** *Why this is the best way to design the surface*, plus an explicit **friction check against the canonical user journey** (Gate 1b): does the new surface collide with or add friction to the journey, or slot in cleanly? Name any collision and how it's resolved or accepted.
- **(d) Review artifact — the surface the approver actually reads.** Render the whole test plan as a **single self-contained artifact** (one file, no external deps) that covers every case at a glance: the **risk register**, **every** core + edge backend check (id · call · input · pass-bar · risk), every Playwright path, and the design/friction table. The plan doc is the source of truth; the artifact is what gets reviewed. **No approval without it.**

All four scoped + vetted → a **TRUE pass** → `READY-TO-BUILD`. The checks are later *executed* (backend checks run green, the click-path passes, the design ships without journey collision) at the `NEEDS-AUDIT` stage — those results must pass before `DONE`.

## Phase E — PR-level engineering plan

Write the plan as discrete PRs. For each PR:
- **Goal** · **Add vs Edit vs Drop** (with `file:line`) · **what's done** · **tests** (pointing at the Gate 3 scope) · a **user-usable hook** (a button on a bare test page that exercises it end-to-end) · **risks/sequencing**.
- **Single source of truth per concern; NO parallel/duplicate code paths** — extend existing functions behind flags/opts; one module per concern; cite the precedent if one exists.
- Bake in **reliability, SLA, auditability, modularization** (idempotency, transactions, structured logs, access control).
- **Tests:** unit (CI-blocking) + **Playwright E2E** proving the user journey is never bugged/blocked — including permission-blockage where relevant.
- **Split the work — what I do vs what only the human can.** Maintain an explicit **HUMAN-ACTION-REQUIRED** list: the privileged actions only the human/an admin can perform — secrets/keys to set (name the exact id; flag where case matters), accounts & test fixtures to provide, external-dashboard steps (Stripe / DNS / cloud console), data backfills they must approve, and the vetting/sign-offs owed. One action per line, terse + actionable. I never perform privileged actions; I state plainly which work is mine-on-a-branch and which is theirs, and request fixtures just-in-time.
- Keep every edit grounded in real code; iterate in rounds with the user.

## STATUS — one line, the earliest unmet gate

A plan always carries one current lifecycle status + a one-line "blocked on / unblocks when". **Assign the earliest unmet status** (the first gate that isn't satisfied), and update it whenever the gate state changes — it's the first thing a reader checks:

- `NEEDS-ARCHITECTURE-REVIEW` — diagrams authored, not yet vetted (Gate 1 open).
- `NEEDS-ASSUMPTIONS-LOCK` — diagrams vetted, but the assumptions checklist still has open items (Gate 2 open).
- `NEEDS-TEST-PLAN` — diagrams vetted + assumptions locked, but the production-readiness test plan (Gate 3) isn't authored or not yet vetted.
- `NEEDS-CONFIRMATION` — all three gates essentially met; only minor confirmations outstanding.
- `READY-TO-BUILD` — all three gates passed (diagrams vetted · assumptions locked · test plan vetted); code may proceed.
- `IN-PROGRESS` — actively building.
- `NEEDS-AUDIT` — built, awaiting outside audit / E2E execution (the Gate 3 checks run for real).
- `NEEDS-REVIEW` — awaiting human review of completed work (PR / results).
- `BLOCKED` — waiting on a specific named HUMAN-ACTION-REQUIRED item (name it).
- `DONE` — merged + verified.   `DEFERRED` — parked, not to be built.

## Phase F — Completion ritual (on "plan marked complete")

When the user marks a plan (or a sub-task) complete, post a **final recap message** covering:
- **Assumptions** that underpin it (and which remain open).
- **Grounding** — the real SOT files you read, so a reviewer trusts it isn't invented.
- **Code structure** across the repo(s) — how the new pieces fit the existing architecture.
- **What's NEW** vs what's edited.
- **Why it's best-practice engineering** (the patterns + their justification).

Then **spawn an outside auditor agent** (the `Agent` tool, fresh context) to audit: does every cited `file:line` exist? is add-vs-edit correct? hallucination check, scope-fence check, and a gate check (diagrams cover the flows, assumptions are all closed, test plan covers the real risks). Default to a **single** auditor; use a small multi-lens panel only if the user asks. **Re-verify the auditor's findings against the code yourself before acting** — an auditor can hallucinate too.

## The 10x bar (enforce throughout)

Ground first · product before engineering, motivation-first · clarify before writing · one decision at a time, locked and built upon · phased to respect context limits · **diagrams + assumptions + test plan are hard gates before any code** · single source of truth, no duplicate paths · explicit scope fences (no silent creep/narrowing/removal) · a clean human-action split (never a setup dependency for privileged actions) · PR-by-PR with add-vs-edit + tests + user-usable verification · STATUS always reflects the earliest unmet gate · justify best-practice from current sources · outside-review before handoff.
