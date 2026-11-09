# Fan-out briefs

Each researcher starts with none of your context, so each brief stands alone. Fill in the
brackets, launch them all in one message in the background, and draft the data file while they
run. Don't redo their searches yourself.

## 1. Pain researcher (one per product group)

```
You are researching what real users complain about, for [GROUP]: [PRODUCT A], [PRODUCT B], [PRODUCT C].
Context: a team is deciding [THE DECISION, e.g. what its landing page leads with]. Its audience is
[AUDIENCE]. You are NOT evaluating that team's product; only report what users of these products say.

Find the pains users report, [YEAR RANGE], ranked loudest first. Primary sources only:
- GitHub issues (pull reaction and comment counts: gh api -X GET search/issues
  -f q='repo:OWNER/REPO is:issue "PHRASE" in:title' -f sort=reactions -f order=desc)
- Hacker News via https://hn.algolia.com/api/v1/search?query=Q&tags=story (or tags=comment)
- Product forums (Discourse: append .json to a topic URL for post counts)
- Trustpilot / review sites (score, review count, theme counts in the newest 15 to 20)
- Official status pages, the vendor's own docs admitting a limit
- Reddit via https://www.reddit.com/r/SUB/search.rss?q=Q&restrict_sr=on&t=year&limit=100
  (browser User-Agent; HTML and JSON are blocked, RSS is not)
- A page that 403s: https://r.jina.ai/<url>
Blogs and listicles are leads: follow them to the primary thread or mark the item WEAK.

[IF THE FOUNDER SUPPLIED A LIST: "Check these leads in primary sources and say which confirmed:
<the list>."]

Report, at most about 600 words:
- Up to 12 pains, loudest first. Each: the pain in one line; one VERBATIM quote; the signal with
  numbers (reactions, comments, points, thread count, review share); the URL and date; WEAK if
  secondhand only.
- A coverage note: which sources you could not reach, and which themes you looked for and did
  not find. "Not found" means not found, not "doesn't exist".
- One line: the pattern across the products.
Cap: about 12 searches or fetches. Read-only, no file edits. No em or en dashes.
```

Groups that covered the 181026 landscape (adapt, don't copy): workflow automation (n8n, Make);
no-code agent builders (Zapier and Zapier Agents, Lindy, Relay); the platform's own vendors' cloud
agents (Claude Code cloud and routines; Codex Cloud, automations, ChatGPT agent, dots); general
computer agents (Manus, Genspark, Comet, Gemini Agent, Zo); background coding agents (Cursor,
Devin, Copilot coding agent, Jules); the DIY path (a VPS, CI + Playwright MCP); the service
alternative (agencies, and any template the founder found).

## 2. Statistics researcher (always one)

```
Find credible statistics for a page that argues: [THE PAIN THEMES, e.g. AI work that is almost
right; automations that break unattended; agents in production].
For each stat: the exact wording, n, the date, the method, what it actually measured, who funded
it, the primary URL, how it is commonly misquoted, and one "use as" line a page could print.
Label predictions as predictions. Flag anything the authors mark out of date. Where no credible
primary number exists for a theme, say so; do not offer a vendor blog figure in its place.
At most about 12 searches or fetches, a report of about 600 words, read-only, no dashes.
```

## 3. Resolution verifier (only when there are more than about 5 clusters to check)

```
For each claim below, answer EXISTS / PARTIAL / MISSING with the file:line that shows it, in two
lines at most. The question is only "does the product do this", not whether it is enabled in
production, how it scales or how well it is built. Read-only.
Repo: [PATHS]. Claims:
1. [cluster]: [what would resolve it]
...
```

Re-check any claim a verifier marks MISSING, and any claim the hero depends on, yourself, in the
code, before it reaches the founder. Verifiers miss things too (a file `grep` treats as binary
looks absent; use `grep -a`).
