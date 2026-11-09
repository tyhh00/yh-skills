# Sources: where real pain lives, how to pull it, how to grade it

## The ladder (try in this order, one retry each, then mark the source unreachable)

| Source | What it gives you | How to pull it |
|---|---|---|
| **GitHub issues** | The loudest developer pain, with numbers: reactions and comments, live | `gh api -X GET search/issues -f q='repo:OWNER/REPO is:issue "PHRASE" in:title' -f sort=reactions -f order=desc -f per_page=10 --jq '.items[] \| [.reactions.total_count, .comments, .created_at[:10], .title, .html_url] \| @tsv'`. Search also matches issue bodies, so keep `in:title` or the hits drift off topic. One issue: `gh api repos/OWNER/REPO/issues/N --jq '.reactions.total_count, .comments'` |
| **Hacker News** | Launch-thread sentiment, points and comment counts | Stories: `https://hn.algolia.com/api/v1/search?query=Q&tags=story`. Comments: `tags=comment`. Each hit has `points`, `num_comments`, `created_at`, `objectID` (the link is `news.ycombinator.com/item?id=<objectID>`) |
| **Product forums** (Discourse: community.n8n.io, community.zapier.com, forum.cursor.com, community.openai.com, community.make.com) | The pains of people who already pay for it | Append `.json` to a topic URL for `posts_count`, `like_count`, `created_at`, `title`. Search: `https://<forum>/search.json?q=Q` |
| **Review sites** (Trustpilot, G2 via AWS Marketplace) | Billing and support pain, the theme share across many reviews | `https://www.trustpilot.com/review/<domain>`: the score, the review count, the 1-star share, then read the 15 to 20 newest and count the themes ("billing in 13 of 15") |
| **Status pages** | The vendor admitting it, in its own words | `status.<vendor>.com/history`. An incident title is a primary source |
| **Reddit** | The words users actually use; the place the blog-blocked crawlers miss | `https://www.reddit.com/r/a+b+c/search.rss?q=Q&restrict_sr=on&sort=relevance&t=year&limit=100` with a browser User-Agent. No login needed. JSON and HTML get blocked; RSS does not. Bulk runs: `scripts/reddit_rss_counts.py` |
| **A page that returns 403 or a bot wall** | The same page as text | `https://r.jina.ai/<full url>`. A headless browser is usually bot-blocked too: one try, not five |
| **Vendor docs and changelogs** | What the product says it can't do ("works best when your laptop is awake") | A vendor admitting a limit counts as primary evidence for that limit |

**Leads only, never evidence:** listicles ("top 10 n8n problems"), SEO comparison blogs, AI overviews, a competitor's marketing page about another competitor. Follow them to the primary thread, or drop them. Anything you could only find secondhand is graded **W**.

## Reddit, specifically

- It rate-limits even RSS: pace 8s per request, wait 60s on a 429, checkpoint after every request. Expect about 30 minutes for 48 searches (6 families x 8 clusters).
- Start it in the background as soon as a draft cluster list exists, not at the end. Log to a file and check the log; `| tail` hides all output until the run exits.
- **Do not score with the counts.** Keyword matches pull in off-topic posts ("silently nerfed the quota" is a cost complaint, not a silent failure), searches cap at 100, and some come back empty. Use the counts only to say "bigger here than on GitHub", and use the **titles** as quotes.
- The best single signal you will get anywhere: users already titling threads with the words of your candidate line ("How did you find out an n8n workflow silently stopped?").
- When the founder says wrap up, stop it, fold in what finished, and name the cells that didn't.

## Loudness grade (one per pain, per product)

| Grade | Weight | Rule |
|---|---|---|
| **H** | 3 | 100+ reactions on an issue, 200+ HN points on a thread about it, or a dominant theme across 100+ reviews |
| **M** | 2 | 20 to 99 reactions, or 3 to 9 separate threads |
| **L** | 1 | One thread, or under 20 reactions |
| **W** | 0.5 | Only found secondhand (a blog quoting Reddit, a review summary) |

Grade the pain from its strongest primary signal, write the numbers next to it in the data (`#16157 r=726 c=1499`), and never round a W up because the quote is good.

## Statistics: the bar for a number on a public page

For each candidate stat, record: the exact wording, n, the date, the method (survey, telemetry, RCT, interviews), what it actually measured, who paid for it, and how it is commonly misquoted. Then one "use as" line.

- **Use:** large-n surveys with a published method (Stack Overflow Developer Survey: 66% of n=31,476 say "almost right, but not quite" is their top AI frustration).
- **Label as a prediction:** analyst forecasts ("Gartner predicts over 40% of agentic AI projects will be canceled by end of 2027"). Never "40% fail".
- **Skip:** a figure that is widely misquoted (MIT NANDA's "95%" is interview-based, about custom enterprise GenAI tools, not "95% of AI projects fail"), a study its own authors mark out of date (METR's July 2025 RCT), vendor-sponsored figures you only found secondhand.
- **No credible number exists:** say it in words. Never invent precision.

The stat the page shows is the statistical form of the hero's pain, not the most impressive number found.
