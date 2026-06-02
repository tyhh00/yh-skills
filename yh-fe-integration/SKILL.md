---
name: yh-fe-integration
description: Frontend-integration + end-to-end verification method for AFTER the backend is built and verified. Wire the FE to the real APIs, build the UI surfaces, then PROVE every user journey by driving the real browser (chrome-devtools / playwright MCP) — not curl. Use when the ask is "integrate the UI for this feature", "finish the frontend", "make sure the user can actually do X end to end", "test the button flows", or "is this feature fully implemented?". Enforces: drive the real click-path (one isolated context per persona), streamlined dead-end-free navigation, server-truth via the network panel, never claim a fix you haven't watched render, root-cause every bug (bisect with logs, don't hand off), human handoff for captcha/login/external dashboards, and a close-out of cases-tested + honest gaps. Invoke with /yh-fe-integration.
---

# /yh-fe-integration — Frontend Integration & End-to-End Verification

The backend is done and verified. This skill is the next mile: making the feature **real for a human** — wired UI, streamlined journeys, and proof that every button works on the actual surface a user touches. "Fully implemented" is not "the code compiles" or "the API returns 200." It is: *a person can complete the entire journey on the real UI, with zero dead-ends, and I watched it happen.*

It pairs with `/yh-plan` (which produced the PR plan) and hands off to a designer agent (which does visual polish). This skill owns the gap between them: integration + functional E2E verification.

## Prime directives (every phase, no exceptions)

1. **Drive the real browser, not the API.** Test the click-path a user takes (discover → act → pay → access → manage). APIs are for *setup* and for *verifying the read-model after a UI action* — never a substitute for the click. If you only curled it, you have not tested it.
2. **Never claim it works until you've SEEN it work.** No "should render," no "the handler exists so it's fine." Render it, screenshot it, read the rendered text. A fix you haven't watched succeed is a hypothesis, and you report it as one.
3. **Root-cause every bug; do not hand off.** A UI not showing up is findable. Bisect with logs until you hit the exact layer. Handing a "simple" render bug to another agent instead of debugging it is the failure mode the user hates most.
4. **One persona per isolated context.** Each role (publisher / consumer / fresh non-subscriber) gets its own browser context with its own cookies. Keep a tab→role map. Drive each journey on the surface *that persona actually uses*.
5. **Streamline ruthlessly.** Minimal clicks, obvious nav, no dead-ends. The path to the goal must make perfect sense; a wrong-guess URL must redirect, not show "not found." If buying takes more than the obvious clicks, that's a bug.
6. **Ground in real code first.** Re-read the files; line numbers drift between sessions. Find the working sibling surface and copy its mount-gate / theme tokens / runtime exactly — don't reinvent. Single source of truth, no duplicate code paths.
7. **Close with cases + gaps.** End every run with a numbered list of what you tested (each with its proof) and an honest list of what you did *not* confirm — especially what only the human can verify.

## Phase 0 — Preconditions & grounding

- **Confirm the BE is actually done + verified.** If not, stop — this is the wrong skill. Note the deployed version, the endpoints, and their proven contracts (request/response shape, including the *gated/blocked* responses).
- **Ground the FE.** Grep + read the real components, the API client, the router. Cite `file:line`. Find the **reference implementation** — the nearest sibling surface that already works — and match its structure (auth gate, layout chrome, theme tokens, edge/runtime, prop timing). Reinventing the mount pattern is how you get subtle render bugs.
- **Map the personas and their surfaces** before touching code.

## Phase 1 — Wire the FE to the real backend

- Add typed API-client functions for the real endpoints (match the existing client's conventions and error handling). Build components off the reference surface.
- **No parallel paths:** extend existing functions / reuse the working component; one module per concern. Cite the precedent.
- **Typecheck 0 after every edit** (both repos if split). Deploy the backend where webhooks/redirects require the live worker; run the FE locally for fast iteration.

## Phase 2 — Map the complete journey & make it discoverable

Before testing, write down the *whole* journey end to end, every step a real user takes — and the streamlined path through it.
- **Enumerate every step + every persona's view.** Discover → act → external step → return → access → manage → change → cancel. The branches matter as much as the happy path.
- **Discoverability:** there must be an obvious entry point everywhere a user would look (account menu, page header, sidebar). Client-side nav, no full re-renders or dead states. A plausible wrong URL must redirect to the real surface.
- **Streamline:** collapse navigation. A conversion gate should go *straight* to checkout, not "view plans → find page → find tier." Name the minimal click-path and make the UI match it.

## Phase 3 — Drive the real UI (the chrome-devtools / playwright discipline)

This is the core loop. Concrete rules, each learned the hard way:

- **Snapshot to get element uids before interacting. uids go stale** after any DOM change (navigation, stream, re-render) — re-snapshot, don't reuse an old handle.
- **Use the real fill/type tool — NEVER JS-inject values into inputs.** React controlled inputs ignore injected values; the submit button stays disabled and your "send" silently no-ops. This is the single biggest time-waster — if a button won't enable, you almost certainly injected instead of typed.
- **`wait_for` the state to settle, then read it** — the rendered banner text, the balance, the new row. Don't assert on a mid-stream snapshot.
- **Verify server-truth in the network panel.** Read the actual response body (SSE/JSON) of the request your click fired — don't infer success from pixels. This is how you separate "FE didn't render" from "server didn't send."
- **Screenshot as evidence for every claim.** A claim of "it works" is backed by an image or a response body, or it isn't made.
- **Guard destructive test actions on identity.** Before a cancel/delete on a shared account, decode the JWT email claim or hit `/me` and only proceed if it matches the intended persona. Auto-accept `confirm()` dialogs only after that guard.
- **One isolated context per persona; keep the tab→role map current** so you never act as the wrong user.
- **Force fresh code when iterating.** Navigate fresh / hard-reload to bust HMR + browser cache. If a just-added log won't fire, check the compiled chunk on disk to see what's *actually* shipped before blaming your code.

## Phase 4 — Human-in-the-loop handoffs

Some steps only a human can do: **captcha, login / fresh test accounts, payment confirmation in real flows, anything on an external dashboard (Stripe, etc.).**
- Drive **all the way to the handoff** on the user-facing surface, set it up cleanly (open the login on a fresh isolated context, navigate to the exact screen), then hand off with a precise ask via `ask_user_question` or a one-line instruction.
- **Continue past it** once the human signals done — re-verify identity, then resume the journey. E2E is not done at the handoff; it's done past it.
- Never fake or skip the human step; never assume it succeeded — confirm, then proceed.

## Phase 5 — Test every case, including the gated branches

- Walk the **happy path** and **every blocked/gated branch** (preview limit hit, missing connection, insufficient credits, cancel-at-period-end, downgrade). **The branch is where things silently die** — a feature that streams fine but dead-ends on the gate is not implemented.
- Verify side effects through the UI where possible (balance deducted from the right account, allotment granted, MRR/usage updated), falling back to the read-model API only to confirm what the UI can't show.
- **When you find a bug, root-cause it (don't hand off):**
  - Get empirical data, don't theorize. Drop a `console.log`/probe and **bisect the ladder:** request fired? (network) → server sent the right payload? (response body) → FE received it? (probe at the parser) → reached the handler? (probe in the case) → state set? → rendered? **Find the first NO.**
  - **Rule out tooling confounds first:** React-injection (Phase 3), Fast Refresh not recompiling a huge file, stale uids, browser cache. Don't blame code for a stale bundle.
  - **The contract-mismatch class:** happy path renders but one branch silently dies → suspect a serialization/framing mismatch on *that branch's* payload (e.g. an SSE `data:`-framed event hitting an NDJSON `JSON.parse(line)` parser → throws → silently skipped). Fix the emit to match the stream the FE actually parses; one fix often repairs every sibling gate.
  - Fix the loop, not just the leaf: if a gate was mis-framed, the others probably are too.

## Phase 6 — Close out: cases tested + honest gaps

Report, every run:
- **Cases tested** — numbered, each with its proof (screenshot / response body / read-model delta). UI-first.
- **Gaps — what was NOT confirmed together:**
  - **Only-the-human-can-verify:** external dashboards, payout ledgers, third-party split/fee accounting, webhook delivery logs. Never let "I verified our read-model recorded 70/30" masquerade as "the third party actually did the split" — say which one you saw.
  - **Untested:** cases you didn't reach (needs a test clock, a second account, a real key), and explicitly deferred items.
- Be precise about the difference between *built*, *wired*, and *verified-on-the-real-UI*.

## Phase 7 — Catalog & hand off to the designer

- After integration, write a **UI-changes catalog**: every surface touched · what the user can now do · the backend it calls · who built it (which commit/agent) · polish-needed flags. This is the **gate before any visual-polish / designer agent** runs.
- **Functional wiring is yours; visual polish is the designer's** — but flag the obvious breakers you saw (hardcoded RGBA that breaks dark mode, bare unstyled inputs, colored alert panels where the theme wants monochrome).

## The 10x bar (enforce throughout)

Real browser over curl · one persona per context · type, don't inject · server-truth in the network panel · screenshot every claim · streamlined, dead-end-free paths · drive to the human handoff and past it · root-cause by bisection, never hand off a render bug · single source of truth, no duplicate paths · close with cases + the gaps only a human can fill.
