# yh-skills

A pack of rigorous, production-grade [Claude Code](https://docs.claude.com/en/docs/claude-code) skills for planning and reviewing engineering and product work — distilled from how I actually drive AI through complex, ship-to-production tasks.

The throughline: **ground every claim in real code, lock every decision with the user, and never cheerlead.**

## Skills

| Skill | Invoke | What it does |
|---|---|---|
| **yh-plan** | `/yh-plan` | Product→engineering planning method. Phased + decision-locked: clarify product, ground every claim in real code (`file:line`), fence scope, lock each decision via questions (good/bad + one **recommended**), produce PR-level plans (add-vs-edit, single source of truth, no duplicate paths, unit + Playwright E2E), and on completion recap assumptions/grounding/structure/what's-new and spawn an outside auditor. |
| **yh-methodological-research** | `/yh-methodological-research` | Evidence-ranked research where **real user pain, not desk reasoning, picks the answer** (a landing hero, a value prop, the stat to show, the next pain to build for). Fans out parallel researchers over primary sources (GitHub issues with live reaction counts, HN via Algolia, product forums, Trustpilot, Reddit via `.rss`), grades loudness H/M/L/W, clusters pains across products, checks in code which ones the product resolves (`file:line`), scores and **stress-tests the ranking**, generates a draw.io landscape map from the data (bundled stdlib scripts), and derives each slot of the decision from the ranking, with every claim sourced and the coverage gaps said plainly. |
| **yh-llmeval** | `/yh-llmeval` | LLM-evaluation pre-planning protocol. Problem decomposition, umbrella tests (100–1000 generated cases + LLM-as-judge), parallel non-invasive pipelines, research grounding, a capped clarification loop, and a final assumptions check before any plan is produced. |
| **yh-fe-integration** | `/yh-fe-integration` | Frontend-integration + end-to-end verification method for *after* the backend is built. Wire the FE to real APIs, then **prove every user journey by driving the real browser** (chrome-devtools / playwright MCP), not curl: one isolated context per persona, type don't inject, server-truth from the network panel, streamlined dead-end-free navigation, human handoff for captcha/login/external dashboards, root-cause every bug by bisection (never hand off a render bug), and close with cases-tested + honest gaps. |
| **yh-visual-proof** | `/yh-visual-proof` | Add-on to `/yh-fe-integration` for when the person who delegated can't walk the flows themselves. Writes the happy path plus 3–6 edge cases up front, captures **every state a user would notice, including the live in-between ones** (loading, streaming, toasts, open menus, motion via GIF + frame recorder), takes **before/after pairs for every change**, desktop + phone, and publishes **one Claude artifact**: a verdict line, each flow as a captioned filmstrip with server truth and feel notes, a tune list, and honest gaps. The human fine-tunes by commenting on frames; each change is recaptured and republished to the same URL. |
| **yh-routine-eng-review** | `/yh-routine-eng-review` | Outsider, production-readiness code review from two skeptical seats at once — a **senior cyber-security engineer** and a **senior Google-level staff engineer**. Honest, no cheerleading. Fans out fresh-context reviewers across architecture, **duplicate/parallel code paths**, file/function size, separation of concerns, **unit-test presence *and* meaning**, reliability/observability, performance, and the full security surface (authz/IDOR, injection, secrets, abuse) — every finding grounded in `file:line`, **re-verified against the code before reporting**, severity-ranked, and closed with a ship/no-ship verdict plus an ordered "what it takes to ship." |
| **i-am-overstimulated** | `/i-am-overstimulated` | Emergency brevity mode for when the walls of prose have become the problem. Hard output contract: **result on line 1, five lines max**, no preamble, no options survey, no permission-seeking, no honesty theatre. Obvious defaults get taken silently; a genuine blocker comes back as **2–3 asks of 6–10 words, each with a copy-pasteable ref**. Default goal is always end-to-end proof driven by you. Long *work* is fine — long *talk* is the offence. |
| **fuck-claude-honesty** | `/fuck-claude-honesty` | Kills the "honest limit: I haven't done X — want me to?" pattern, where disclosure stands in for delivery. One test before naming any gap: **could I have closed this myself, this turn?** If yes, close it and don't mention it; if genuinely blocked (privileged, irreversible, a real fork, a missing credential), say so in one line and do everything else. **DONE means driven, not reasoned**, and a mandatory end-of-turn open-loop audit runs before any completion claim. |
| **yh-master-planner** | `/yh-master-planner` | Sprint-scale orchestrator: turns a batch of raw items into **founder-vetting-ready engineering plans without building them**. Fans out subagents to ground each item in real code (`file:line`, negative findings included), surfaces disproven premises, runs the heavy decision round to **zero open assumptions**, then fans out one subagent per item to author the full gate set (ENG-PLAN, architecture + user-journey drawios, ASSUMPTIONS, gate-3 test plan in `.md` + `.html`), and puts every high-risk plan through an **adversarial audit by the strongest available model**, re-verified against the code, until no CRITICAL/HIGH findings remain. Written against the Kavela sprint layout; adapt the paths to your repo. |

## Install

Clone, then symlink each skill into your Claude Code skills directory:

```bash
git clone https://github.com/tyhh00/yh-skills.git
cd yh-skills
# user-level (available in every project):
ln -s "$PWD/yh-plan"            ~/.claude/skills/yh-plan
ln -s "$PWD/yh-methodological-research" ~/.claude/skills/yh-methodological-research
ln -s "$PWD/yh-llmeval"         ~/.claude/skills/yh-llmeval
ln -s "$PWD/yh-fe-integration"  ~/.claude/skills/yh-fe-integration
ln -s "$PWD/yh-visual-proof"    ~/.claude/skills/yh-visual-proof
ln -s "$PWD/yh-routine-eng-review" ~/.claude/skills/yh-routine-eng-review
ln -s "$PWD/i-am-overstimulated" ~/.claude/skills/i-am-overstimulated
ln -s "$PWD/fuck-claude-honesty" ~/.claude/skills/fuck-claude-honesty
ln -s "$PWD/yh-master-planner"  ~/.claude/skills/yh-master-planner
```

Or copy any `yh-*/` directory into a project's `.claude/skills/`. Invoke with the slash command (e.g. `/yh-plan`).

## License

MIT — see [LICENSE](LICENSE).
