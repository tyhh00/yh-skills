# yh-skills

A pack of rigorous, production-grade [Claude Code](https://docs.claude.com/en/docs/claude-code) skills for planning and reviewing engineering and product work — distilled from how I actually drive AI through complex, ship-to-production tasks.

The throughline: **ground every claim in real code, lock every decision with the user, and never cheerlead.**

## Skills

| Skill | Invoke | What it does |
|---|---|---|
| **yh-plan** | `/yh-plan` | Product→engineering planning method. Phased + decision-locked: clarify product, ground every claim in real code (`file:line`), fence scope, lock each decision via questions (good/bad + one **recommended**), produce PR-level plans (add-vs-edit, single source of truth, no duplicate paths, unit + Playwright E2E), and on completion recap assumptions/grounding/structure/what's-new and spawn an outside auditor. |
| **yh-auditproduct** | `/yh-auditproduct` | Skeptical CEO-level product / positioning review. Applies engineering-grade rigor to market claims — uniqueness checks, layer separation, source discipline, table-stakes-vs-moat — and ends on a forcing function: name one real buyer who'll pay this week. |
| **yh-llmeval** | `/yh-llmeval` | LLM-evaluation pre-planning protocol. Problem decomposition, umbrella tests (100–1000 generated cases + LLM-as-judge), parallel non-invasive pipelines, research grounding, a capped clarification loop, and a final assumptions check before any plan is produced. |
| **yh-fe-integration** | `/yh-fe-integration` | Frontend-integration + end-to-end verification method for *after* the backend is built. Wire the FE to real APIs, then **prove every user journey by driving the real browser** (chrome-devtools / playwright MCP), not curl: one isolated context per persona, type don't inject, server-truth from the network panel, streamlined dead-end-free navigation, human handoff for captcha/login/external dashboards, root-cause every bug by bisection (never hand off a render bug), and close with cases-tested + honest gaps. |

## Install

Clone, then symlink each skill into your Claude Code skills directory:

```bash
git clone https://github.com/tyhh00/yh-skills.git
cd yh-skills
# user-level (available in every project):
ln -s "$PWD/yh-plan"            ~/.claude/skills/yh-plan
ln -s "$PWD/yh-auditproduct"    ~/.claude/skills/yh-auditproduct
ln -s "$PWD/yh-llmeval"         ~/.claude/skills/yh-llmeval
ln -s "$PWD/yh-fe-integration"  ~/.claude/skills/yh-fe-integration
```

Or copy any `yh-*/` directory into a project's `.claude/skills/`. Invoke with the slash command (e.g. `/yh-plan`).

## License

MIT — see [LICENSE](LICENSE).
