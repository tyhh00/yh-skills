---
name: yh-methodological-research
description: Evidence-ranked research where real user pain, not desk reasoning, picks the answer, whether that is a landing hero, a value prop, a positioning line, the stat to show, or which pain to build for next. Use when the founder calls a line "slop" or "not sharp", or asks "what should the landing say", "research the competitors' pain points", "map the competitor landscape", "what do users actually complain about", "derive the value line", "what should we statistically say", or "does our product resolve it". Fans out parallel researchers over primary sources (GitHub issues with live reaction counts, Hacker News, product forums, Trustpilot, Reddit via .rss), grades loudness, clusters pains across products, checks in code which ones the product resolves, scores and stress-tests the ranking, generates a draw.io landscape map from the data, and derives every slot of the decision from the ranking. Invoke with /yh-methodological-research.
---

# /yh-methodological-research: let ranked real pain pick the answer

Distilled from the Kavela landing work of 181026. Eight rounds of asking "what is the real value?" of the product's own features (v0 to v8) produced lines the founder called slop. One round of primary-source pain research across 19 competitors produced the hero in a single pass: *"AI automations that don't fail silently."* n8n users were already titling Reddit threads "How did you find out an n8n workflow silently stopped?".

**The lesson:** a line derived from how the product works is a commodity. A line derived from a pain users already complain about loudly gets recognised in seconds. Lenses, paste tests and recursive self-critique are desk work, not research. This skill replaces them with a pipeline whose output is a ranking, and the ranking picks.

Every artifact this produces, worked end to end: `kavela/prop_research/competitormap/`.

## Stance

- **The data picks; the founder decides.** Present the ranking and a slot-by-slot recommendation, then lock the pick with `ask_user_question`. The founder's call on what makes a headline overrides the score: cost and limits was the loudest cluster and still "doesn't feel like a headliner". Once it's locked, don't re-litigate it.
- **Primary sources, or it's WEAK.** GitHub issues, HN threads, product forums, review sites, status pages, Reddit threads. A listicle, an SEO blog or an AI overview is a lead to follow, never evidence.
- **"Not found" doesn't mean "doesn't exist".** Every report names what it couldn't reach, and the final doc has a "Coverage gaps, said plainly" section.
- **The shape is real; the decimals aren't.** Loudness counts measure noise, not a statistical sample. Never print a priority score on a public surface.
- **Verify only what the decision needs.** "Does the product resolve this pain?" is answered by one file:line showing the feature exists. It doesn't need prod flag state, capacity math or infra internals (founder: "assume all on, just verify the feature exists"). If a claim would need that depth, claim less.
- **Run in parallel from the first minute.** Use one researcher per product group, all in the background. A serial crawl is the failure mode (founder: "spawn a workflow to verify else ure just gna take forever").
- **Keep chat short while it runs.** Post one line per report as it lands, saying what's loudest. The detail goes in the data file.

## The pipeline

**0. Frame (no research yet).** Write down three things:
- the decision (a landing hero? a roadmap pick?);
- the audience, as named segments;
- the landscape, breadth first: what the audience would name, the platforms they already pay for that are edging in, adjacent categories, the DIY path (a VPS, CI plus scripts), the service alternative (agencies, consultants), and doing nothing.

Aim for 5 to 8 product groups, plus one for statistics. A template, pain list or AI overview the founder pastes is a lead: it gets a group, and it gets verified like everything else. In 181026, two items on the founder's pasted n8n list (canvas friction, no end-user mode) never confirmed in a primary source.

**1. Fan out.** Launch one pain researcher per group and one statistics researcher in a single message, in the background, from the briefs in `references/briefs.md`. Each is capped at about 12 calls and a 600-word ranked report with verbatim quotes, numbers, URLs, dates and a coverage note. Source commands and the grading rubric are in `references/sources.md`.

**2. Encode as each report lands.** Every pain goes into the data file (schema below), with:
- its text: users' words, short, with the signal numbers in brackets;
- its grade: H, M, L or W, by the rubric;
- its cluster id.

The data file is the single source of truth. The doc, the diagram and the ranking all come from it.

**3. Cluster.** Merge the same pain across products into about 8 to 12 clusters. Name each one in users' words ("It fails silently, or says done when it isn't"), never in mechanism words ("observability", "orchestration").

**4. Check resolution in the code.** Mark each cluster `yes`, `partial` or `no`, with a one-line "how" and the file:line. Fan out the verifier brief when there are more than about 5. Re-check yourself anything the hero depends on, and anything a verifier marked missing.
- **partial:** only the solved half is ever claimed.
- **no:** never claimed. It's a roadmap input.

**5. Score and stress-test.** Run `python3 scripts/landscape_drawio.py data.json landscape.drawio`. It prints:
- the ranking: priority = loudness summed over every product reporting the cluster × the resolve factor (yes 1, partial 0.5, no 0);
- a re-score with H weighted 5;
- an overlap check of the diagram's layout.

If #1 flips under the re-score, the ranking is not decisive. Say so, and widen the research before recommending. (The bundled 4-product example flips; the full 19-product set holds.)

**6. Second signal: Reddit.** Run `scripts/reddit_rss_counts.py config.json reddit.json` in the background as soon as a draft cluster list exists, logging to a file (`examples/reddit.kavela-181026.json` is a real config). The counts are too noisy to score with. Use them as "bigger here than on GitHub", and use the thread **titles** as quotes. Users titling threads with the words of your candidate line is the strongest confirmation available anywhere.

**7. Statistics.** Use only primary-source numbers, each with its exact wording, n, date, what it measured and its common misquote. Label predictions as predictions. Where no credible number exists, say it in words.

**8. Derive, slot by slot.** Build a table: slot / content / which cluster it comes from. For a landing:

| Slot | Rule |
|---|---|
| **Hero** | The top cluster the product **fully** resolves, written as that pain negated, in users' words. **Literal clarity beats uniqueness:** a clear line will sound like its category (YC: understood in 3 to 5 seconds, 14 words or fewer). Don't run the "could a competitor paste their name in?" test on the hero. |
| **Sub line** | How the pain gets solved: the product's mechanism or the founder's philosophy. This is where the only-us part lives. |
| **Partial clusters** | Only the solved half, in a visual or the footnote ("waits at a limit, then carries on", never "no limits"). |
| **Next clusters** | Feature sections, how it works, scenes, FAQ, in rank order. |
| **Stat strip** | The statistical form of the hero's pain, sourced and linked. |
| **Don't claim** | Every `no` cluster, plus the unsolved half of every `partial`. |

When the founder states the product's philosophy, map each piece to the pain it answers (piece / pain / slot). The pain is the *what*; the philosophy is the *how*. For a roadmap call, invert the table: the loudest `no` and `partial` clusters are the build list.

The page names pains, never competitor brands.

**9. Visualize from the data.** The generator writes the draw.io in three pages:
- **Landscape:** centre, then group, then product, then pain leaves, each coloured by resolution and tagged H, M, L or W.
- **Pain clusters:** each cluster, how it's resolved (with code) and where it goes.
- **Derivation:** the method as run.

Never hand-draw the map: regenerate it from the data. If the draw.io web viewer renders blank headless, trust the overlap check and the XML parse. Don't debug the viewer.

**10. Deliver.** Promote everything to a durable folder (`<repo>/prop_research/<topic>/`):
- **`README.md`:** the decision in one line, plus a file table.
- **`research.md`:** the TLDR, the method as run, the ranking, the evidence per competitor (with links), the stats to use and skip, the derivation and the coverage gaps.
- **The data files:** `data.json`, `landscape.drawio` (with the command that rebuilds it), the Reddit config and output.

In chat, give the TLDR: the recommended line, the top 3 clusters and why, the gaps, and where the files are. Then lock the pick with `ask_user_question`.

## The data file

```json
{
  "product": "Kavela",
  "center": "The job the audience is trying to get done",
  "weights": {"H": 3, "M": 2, "L": 1, "W": 0.5},
  "categories": [
    {"name": "Workflow automation", "side": "right", "competitors": [
      {"name": "n8n", "pains": [
        {"text": "Workflows stop with no error, no log (thread, 33 posts)", "strength": "H", "cluster": "silent"}
      ]}
    ]}
  ],
  "cluster_defs": {
    "silent": {"name": "It fails silently, or says done when it isn't", "resolves": "yes",
               "how": "A reviewer checks every run and sends the gap back.\njudge-deliverables.ts:24"}
  },
  "placement": {"silent": "HERO"},
  "derivation": [{"title": "1. Research", "body": "7 researchers, 19 products, primary sources only"}]
}
```

`side` (`left` or `right`) balances the mind map. `placement` and `derivation` are optional; without `placement`, clusters fall into landing slots by rank. A runnable slice of the real data: `examples/landscape.example.json`.

## What went wrong in 181026 (don't repeat it)

- **Recursive "what's the real value?" loops over the feature list** (v0 to v8). That's wordsmithing, not research. Each round only sharpened the mechanism.
- **The paste test on the hero.** Hunting for an only-us line made it abstract ("Write a workflow in plain English..."). It failed "what is it, where does it run, do I need it".
- **Mechanism words promoted to the headline:** agents, workflows, plain English, cloud. Cloud is table stakes now, and so is "agents".
- **Auditing prod flags, container ceilings and infra internals** when the decision only needed "the feature exists".
- **Verifying serially, and writing long chat updates while waiting.**
- **Letting Reddit counts re-score the ranking.** They confirm; they don't rank.
- **Quoting a stat's headline number without what it measured.**
- **Starting the slow Reddit pull last**, so the wrap-up waited on it.

## Kavela bindings

- **Zero fabrication is a hard rule.** Every claim must be backed by a real source or a real file:line.
- **On the page:** no competitor names, and no partner names or logos without written permission. Cloudflare's and Supabase's playbooks became "playbooks written by the makers of the tools it uses".
- **Copy rules:** no em or en dashes. Finished copy then goes through `/yh-copy`.
- **Verify features in** `kavela/mcp-server/src` (backend) and `kavela/frontend/landing` (frontend), with file:line. Assume flags are on.
- **Copy lives in** `kavela/frontend/landing/app/(v2mkt)/v2/_landing-components/home/content.ts`, with the grounding note beside each claim.
- **Report the TLDR in chat**, never as a pointer to a file.
