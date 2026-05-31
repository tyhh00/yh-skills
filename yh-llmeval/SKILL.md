---
name: yh-llmeval
description: LLM evaluation pre-planning protocol — for shipping AI / memory / agent systems to production with stakeholder-reportable findings. Invoke explicitly with /yh-llmeval. Forces problem decomposition, parallel non-invasive experimentation pipelines, PhD-level research grounding, neutral critique, a capped clarification loop, and a final assumptions check before any plan is produced.
---

# yh-llmeval

Pre-planning protocol for LLM evaluation work. Run BEFORE writing code or producing a plan. Explicit-invoke only.

## 1. Restate the goal as success criteria
Outcomes, not steps. Quote the user's framing back to confirm alignment.

## 2. Decompose into orthogonal sub-problems
Each axis must be independently observable, measurable, and umbrella-testable. (e.g. memory → what's stored / what's retrieved / how it's injected.)

## 3. For each sub-problem, design an umbrella test
**Scope: umbrella testing is for AI / LLM systems specifically.** Black-box LLM completions cannot be edge-case-covered by human manual testing — you need scaled generation + scaled judgement.

- 100–1000 generated test cases with expected results
- Run the **actual production component** (real LLM call, real prompts, real model) against a sandbox identity (pseudo-user, throwaway workspace) — never a replica
- LLM-as-judge for scoring
- Minimal inspection UI (vite / gradio / HTML) so each case is manually auditable

Non-LLM logic: cover with normal unit / integration tests, not umbrella eval.

## 4. Find the smallest testable abstraction
Strip to a single LLM call + bundled context. Don't drag in the orchestration layer. Eval must be reproducible without booting the full app.

## 5. Build parallel, non-invasive pipelines
Read prod code, never edit it. Experimentation lives alongside, not inside. Document the seam where parallel eval ends and prod begins.

## 6. Cover evolving / chained cases
Single-shot eval is insufficient for stateful systems. Test across sessions, returns to old chats, contradictions, corrections. Mirror the human thought journey.

## 7. Take a neutral stance
List flaws in the user's plan before agreeing with it. Specific risks, not vibes.

## 8. Ground in research
Search PhD-level papers + recent (last 18 months) preprints on the topic (LLM memory systems, eval harnesses, LLM-as-judge calibration, agent benchmarks, etc.). Cite URLs. Note what's transferable vs not.

## 9. Read prod code end-to-end
Trace the actual flow in the actual repo. Quote `file:line`. No recommendations from memory alone.

## 10. Iterative clarification loop (max 3 rounds)
Ask clarifying questions in batches. Hard cap at 3 rounds — if still ambiguous after, surface the remaining unknowns in §11 rather than asking again.
- Hard questions → propose your recommendation with reasoning
- Taste questions → surface the tradeoff, let user pick

## 11. Final assumptions check — STOP HERE
Before producing the plan, output a tight bulleted list of the practical assumptions you're operating under. TLDR style, each bullet ≤ 1 line. Lets the user spot wrong premises in under 30 seconds.

Format:
- **Goal:** <one line>
- **Sub-problems:** <list>
- **Test surface:** <what you're isolating>
- **Out of scope:** <what you're not touching>
- **Open questions you're proceeding on:** <unresolved from §10>

End the message with:

> Reply with corrections, or `proceed` to generate the plan.

Do not produce the plan until the user replies.

## 12. Output: databank, not opinions
Each claim cites a test case, code line, or paper. Findings stay in-conversation unless the user explicitly requests a durable artifact (e.g. `LLMEVAL.md`).

## Anti-patterns
- Jumping to implementation before the assumptions check is confirmed
- Touching prod "just a little" to enable testing
- Single-shot eval for stateful systems
- Treating non-LLM logic as needing umbrella eval (or applying unit tests to LLM black boxes)
- Agreeing with the user's decomposition without challenging it
- Asking clarification questions you could have answered by reading the code or a paper first
