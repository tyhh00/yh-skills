---
name: yh-routine-eng-review
description: Outsider, production-readiness engineering review of a codebase (or a repo / sub-package / diff) by two skeptical senior reviewers at once — a senior cyber-security engineer and a senior Google-level staff engineer. Use whenever the ask is "is this code ready for production?", "review the implementation / code quality", "what does it take to ship this?", "audit the engineering", or before a launch/merge/handoff. Honest, no-cheerleading. Flags parallel/duplicate code paths, bad structure, files larger than they need to be, weak separation of concerns, missing/weak unit tests, and any practice that "can't last" — every finding grounded in real code (file:line), severity-ranked, with a concrete fix and a production-readiness verdict. Fan out fresh-context reviewer agents, then re-verify their findings against the code yourself before reporting. Invoke with /yh-routine-eng-review.
---

# /yh-routine-eng-review — Outsider Production-Readiness Engineering Review

A recurring, outsider engineering review whose only job is to answer one question honestly: **is this code ready for production, and if not, exactly what does it take?** It applies the same evidence standard a strong engineer applies to a PR — but to the whole surface, from two adversarial seats at once: a **senior cyber-security engineer** and a **senior Google-level staff engineer**. It pairs with `/yh-plan` (which produced the plan) and `/yh-fe-integration` (which proved the journeys); this skill is the cold, grounded code-quality gate.

The deliverable is **not reassurance.** A review that only confirms is worthless. The value is catching the duplicate code path, the unbounded query, the missing authz check, or the 1,800-line god-file *before* it becomes load-bearing in production.

## Stance (read this first — it sets everything else)

- **Outsider seat, fresh eyes.** Review as someone who did *not* write the code and owes it no loyalty. Past memories/docs are hints, not truth — the code is truth. If a memory or comment contradicts the code, the code wins; say so.
- **Honest, kind, complete.** Warmth and candor are not in tension. Deliver the uncomfortable read fully. Do not soften a Blocker into a "nit." Do not invent problems to look rigorous either.
- **No cheerleading; no nitpicking theatre.** Every finding must change a ship/no-ship decision or a maintenance cost. If it doesn't, it's noise — cut it.
- **Ground every claim in real code.** Cite `file:line` and quote the exact code. **Never report a finding from memory or from a subagent's unverified word** — that is the #1 failure mode of this skill. Auditors (including the agents you spawn) hallucinate; re-verify each finding against the file yourself before it goes in the report.
- **Severity is a promise.** A "Blocker" means *do not ship*. Calibrate honestly so the label keeps meaning something.
- **"Can it last?" is the through-line.** The bar is not "does it work today" — it's "will a different engineer be able to safely change this in six months without it collapsing?"

## Phase 0 — Scope & ground

Pin down *what* you're reviewing before reading a line — get it via `ask_user_question` if ambiguous:
- **Target:** whole repo · one sub-package · a specific feature/module · a diff/branch/PR. A focused target gets a deeper review; say which you chose.
- **Stack & domain:** language(s), framework, runtime (e.g. Workers/Bun/Node), data layer, what the code *does*. The "best practice for the specific work" depends on this — a payment path, an auth path, and a static page are not held to the same bar.
- **Production context:** who runs it, multi-tenant?, what's the blast radius of a bug, is there a deadline/launch this gates.
- **Baseline:** if this skill has run before, find the prior review (doc/memory) and review the **delta** plus any unresolved findings — don't re-litigate closed items.

Then **build a ground-truth map** before judging: enumerate the modules, the entry points, the data flow, and `git` history if useful. Measure, don't eyeball — line counts per file, test files present vs source files, dependency manifest. Read the actual source-of-truth files.

## Phase 1 — Fan out the review (two seats, by dimension)

Spawn **fresh-context reviewer agents** (the `Agent` tool) so each reads the code without your priors. Run the two seats across the dimensions below. Scale the fan-out to the target: a small diff → one or two agents; "audit the whole service" → one agent per dimension, both seats. Each agent must return **grounded findings only**: `file:line` + quoted code + why it matters + severity + a concrete fix. Tell them to default to "no finding" when unsure rather than pad the list.

### Seat A — Senior staff (Google-level) engineer lens
Design-review rigor; the bar is "would this survive a strict CL review and still be safe to change in a year."

1. **Separation of concerns & architecture.** Clear layers (transport / domain / data)? Dependencies point one way? Business logic leaking into controllers/handlers or into the DB layer? God-objects/utils-dumping-grounds? Wrong abstraction level.
2. **Duplicate / parallel code paths — flag hard.** The cardinal sin: a second route/function/branch that does "the same thing but for guest/free/mode-X" copy-pasted from the original. Find them; propose one source of truth (extend the existing function behind a flag/option), don't bless the fork.
3. **File & function size / complexity.** No file larger than it needs to be. Flag god-files (rule of thumb: a source file pushing ~400–600+ lines, or a function past ~50–75, earns scrutiny — judge by responsibilities, not the number alone), deep nesting, high branching, long parameter lists. Recommend the split and the seam.
4. **Modularity & longevity ("can it last?").** Right-sized abstractions (not premature, not absent), honest names, no dead/commented-out code, no copy-paste constants, stable module boundaries, no circular deps. Will the next engineer find it?
5. **Tests — presence *and* meaning.** Do unit tests exist for the logic that matters? Do they assert behavior or just execute lines? Critical paths and error branches covered? Flaky/time/network-dependent tests? Coverage of the *risky* code, not a vanity %. Call out untested load-bearing code as a Blocker for that path.
6. **Reliability & operability.** Error handling (swallowed errors? bare catch?), idempotency where retried, transactions where multi-write, timeouts/retries on I/O, resource lifecycle (connections/handles/listeners closed; no fire-and-forget that races cleanup), structured logging + metrics/traces for the hot paths. Graceful degradation.
7. **Performance & scale.** N+1 queries, unbounded reads (missing pagination/limits), work in a loop that should be batched, missing indexes for the query shape, accidental O(n²), caching gaps on hot paths, payloads with no ceiling.
8. **Maintainability & hygiene.** Typing discipline (no escape-hatch `any`/`as` at boundaries), lint/format consistency, config & secrets via env not literals, error messages that help, docs where the *why* is non-obvious, no checked-in noise.

### Seat B — Senior cyber-security engineer lens
Adversarial; assume a hostile caller. Threat-model the trust boundaries first, then hunt.

1. **AuthN/AuthZ.** Is every privileged path actually gated? Object-level authz (IDOR) — can user A act on user B's resource? Tenant/row isolation (RLS or equivalent) enforced, not assumed? Default-deny?
2. **Injection & untrusted input.** SQL/NoSQL injection, command injection, SSRF (server-side fetch of user-controlled URLs), path traversal, template/prototype pollution, unsafe deserialization. Is input validated/parameterized at the boundary?
3. **Secrets & crypto.** Secrets in source/history/logs? Keys rotated/scoped? Crypto misuse (weak/rolled-own, predictable randomness, plaintext at rest where it shouldn't be)? Tokens scoped & expiring?
4. **Data exposure.** Over-broad API responses (leaking internal fields/PII), verbose errors/stack traces to clients, logging of secrets/PII, missing redaction.
5. **Abuse & resource safety.** Rate limiting / quotas on expensive or auth endpoints, unbounded request bodies, ReDoS, billing/credit paths that can be driven negative or double-spent, race conditions on money/state (check-then-act without a lock/atomic op).
6. **Dependencies & supply chain.** Known-CVE packages, unpinned/abandoned deps, dangerous transitive surface, postinstall risk.
7. **Web/platform specifics (when relevant).** CORS too open, missing security headers, XSS (stored/reflected/DOM), CSRF on state-changing routes, cookie flags, SSRF via webhooks, open redirects.

> Map the dimensions to the target. A pure backend service skips XSS/CSRF; a payments path makes Seat-B item 5 mandatory; a static site collapses most of Seat B. Name the dimensions you ran and the ones you deliberately skipped (and why).

## Phase 2 — Re-verify (kill false positives yourself)

The agents are inputs, not the report. For **every** finding before it ships:
- Open the cited `file:line` and confirm the code actually says what the finding claims. Drop or correct anything that doesn't survive — wrong line, misread control flow, "vulnerability" that's gated upstream, "duplicate" that's actually a justified specialization.
- De-duplicate overlapping findings across the two seats into one entry.
- Down/upgrade severity against reality (a SQLi behind an internal-only admin gate is not the same Blocker as one on a public route — say so).
- Confirm each finding is **actionable**: it names the fix, not just the smell.

This step is non-negotiable — it's the difference between a review the user trusts and a wall of plausible-sounding noise.

## Phase 3 — Severity & the production-readiness verdict

Rank every surviving finding:
- **🔴 Blocker** — do not ship. Security hole, data-loss/corruption risk, money path that can be abused, load-bearing logic with zero tests, a crash/footgun a normal user will hit.
- **🟠 High** — ship only with eyes open + a fast follow. Will bite in production or in the next change; real maintenance debt with a near-term cost.
- **🟡 Medium** — should fix before this area grows. Structural smell, duplicate path, oversized file, weak test, missing observability.
- **🔵 Low / Nit** — worth noting, not gating.

Then give the **verdict**: `Ship` / `Ship with fast-follows` / `Do not ship`, with the one-line reason. State the production-readiness gap as *work*, not vibes.

## Phase 4 — Deliver: the punch list + "what it takes"

Lead with the **single most important finding**, even (especially) if it's the uncomfortable one. Then:
1. **Verdict + readiness scorecard** — one line per dimension (Architecture, Duplication, File size, Tests, Reliability, Security, Performance, Hygiene): ✅ solid / ⚠️ gaps / ❌ not ready, each with the why.
2. **Prioritized punch list** — every finding as: **severity · `file:line` · what's wrong (quoted code) · why it can't last in prod · the fix**. Ordered by severity, then blast radius.
3. **The meta-patterns** — the behavioral read across findings is often more valuable than any single one (e.g. "every new mode is a copy-pasted fork," "tests exist but assert nothing," "errors are swallowed everywhere," "no authz layer — each handler re-checks ad hoc"). Name them plainly.
4. **What it takes to reach production** — the gaps as a concrete, ordered remediation plan: Blockers first, the fast-follows, then the structural debt — with rough effort. This is the answer to "what does it take to ship."
5. **Keep what's right.** Name the genuinely good engineering you saw — not flattery, but so the team knows what to preserve through the fixes.

Keep findings **in-conversation by default.** Write a durable artifact (e.g. `ENG-REVIEW.md` / a memory) only if the user asks or if this is an explicitly recurring baseline.

## Anti-patterns (of the review itself)

- Reporting a finding you didn't open the file to confirm (or that a subagent asserted and you trusted).
- Coverage-% worship — a high number over meaningless tests is a *failure* to flag, not a pass.
- Style nits dressed up as Blockers; real Blockers buried under nits.
- One-size bar — holding a static page to a payment path's standard, or vice-versa.
- Reviewing the diff while blind to the architecture it lands in (and the duplicate it quietly forks from).
- "Looks fine" with no evidence — the same vibes-based pass this skill exists to replace.
- Inventing problems to look thorough. Calibrate; an honest "this area is solid" is a finding too.

## The 10x bar (enforce throughout)

Outsider eyes, code is truth · two seats (staff + security) every run · ground every finding in `file:line` and re-verify it yourself · hunt duplicate/parallel paths and oversized files specifically · tests must assert, not just execute · severity is a promise · lead with the worst news · name the meta-pattern · end on "what it takes to ship," ordered · keep the part that's right.
