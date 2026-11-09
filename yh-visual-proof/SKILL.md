---
name: yh-visual-proof
description: Visual proof that delegated frontend work actually works, built on /yh-fe-integration. Drive the real UI through the happy path plus the edge cases a busy human would never walk themselves, capture every state that matters (including the live in-between ones: loading, streaming, toasts, open menus, motion), take a before and after for every change, and publish one Claude artifact that shows each flow step by step with a verdict. The person who delegated sees what is confirmed in 30 seconds and fine-tunes by commenting on frames. Use when the ask is "provably show it working", "show me the full flow", "take screenshots", "try it on a few test cases", "before and after", "make an artifact showing it's ready", or before reporting UI work done to someone who can't easily check it. Invoke with /yh-visual-proof.
---

# /yh-visual-proof — show it working, in pictures

The person who handed you this job can't walk a twelve-step flow through five edge cases, and they still care how it feels. Your "done" means nothing to them until they can see it. This skill turns the driving you do under `/yh-fe-integration` into one published page: every flow walked on the real UI, each state captured, a before and after wherever something changed, a verdict per flow. They should know what is confirmed within 30 seconds and be able to tune the rest by pointing at a frame.

**It runs on top of `/yh-fe-integration`.** That skill owns how you drive: real browser, type don't inject, server truth in the network panel, root-cause every bug, drive past human handoffs. Run it first if it hasn't run this session and keep to its rules. This skill adds what to capture and how to show it.

## 1. Write the cases before opening the browser

Put them in `<evidence>/cases.md`. Each case: goal in one line · setup (account, data, URL) · steps · what working looks like to the user (the outcome, never a proxy like a 200 or a DB row).

- The happy path, end to end.
- 3 to 6 edge cases, picked for what the human would find tedious to reproduce: the gated or blocked branch, the empty state, bad input or an error, long or messy real content, reload or reopen mid-flow, the second persona's view, phone width.
- If there are more, keep the ones that prove the feature and list the rest as "Not tried" on the page.

## 2. Capture the before first

If you are about to change anything, capture its before frames now, with the same viewport, account, data and scroll position you will use for the after. Once the code moves, the before is gone. If you already edited, rebuild it from the previous commit or label the pair "after only".

## 3. Capture the live states

Evidence goes in `.yh-fe-evidence/<feature>-<DDMMYY>/` in the repo you are working in, named `<case>-<nn>-<state>.png` (`gate-03-card-shown.png`). Save every frame to disk: claude-in-chrome `computer` screenshot with `save_to_disk: true`, playwright `browser_take_screenshot` with `filename`, chrome-devtools `take_screenshot` with `filePath`. Log each frame as one line in `<evidence>/frames.md`: file · what the user did · what they now see (the rendered text you read) · Confirmed or Failed.

- **One frame per state the user would notice, not per click:** the entry point, each step's result, the settled outcome, and the view after a reload.
- **Catch the in-between states on purpose.** Loading, streaming, skeletons, toasts, open menus, hover tips, a button going from disabled to enabled. The product feel lives there. Screenshot straight after the action, before `wait_for`, then again once it settles.
- **A still can't prove motion.** For jitter, layout shift or animation, record it: a GIF (`gif_creator`) for the human to watch, plus a requestAnimationFrame recorder (row tops, heights, scrollTop per frame) when you claim "no jumps". Don't edit FE code during a recorded run, because hot reload replays the flow. Playwright's `.click()` scrolls first, so use `el.click()` in `evaluate` for motion runs.
- **Pair key frames with server truth:** the response-body lines that prove the outcome happened, not just rendered.
- **Desktop (1440) and phone (390)** for every surface you touched.
- **One feel note per step:** time from click to visible result (measured), any shift or flicker, copy that reads wrong, a click that shouldn't be needed.
- **Failures stay in.** Keep a failing frame and caption it with what was expected. Root-cause it per `/yh-fe-integration`, fix it, and the fix becomes a before/after pair.
- **Never stage a frame.** No DevTools-edited DOM, no injected state. Seeded setup (API, fixtures) is fine, and the case says so.
- **No secrets or real customer data in a frame.** Use test accounts, and crop when you can't avoid it.

## 4. Build the page

Load `artifact-design` first. Shrink frames before publishing (`sips -s format jpeg -s formatOptions 80 -Z 1600 in.png --out frames/in.jpg`) and ship them through the publish `files` map as `frames/<name>.jpg`, not as base64. Stay well under 16MB.

Top to bottom:
1. **Verdict line**, true even if they read nothing else: `5 of 6 flows confirmed on staging · failing: invite with expired link · checked 9 Nov 14:20 · commit abc123 · as test+1`.
2. **Flow index:** one row per case with a status word (Confirmed, Failed, Not tried) linking to its section. Words, not coloured dots.
3. **Each flow as a filmstrip:** frames in order, click to enlarge, captioned "what the user did → what they see". Expected vs observed when they differ. Server-truth excerpt and feel note in a fold.
4. **Before / after** side by side at the same size, or a drag slider, each labelled with its commit.
5. **Phone view** of each surface you touched.
6. **Tune list:** what they may want to adjust (copy, spacing, timing, order), each item tied to a frame and phrased so they can answer in a word.
7. **Gaps:** what you didn't confirm and why, and what only they can check (external dashboards, real payments, other people's inboxes).

Footer: URL, environment, commit, and how to rerun each case.

## 5. Hand it over, then tune

- Reply with the verdict line and the link. Don't paste frames into chat.
- They tune by commenting on frames. Read and answer with `ArtifactComments`. For each comment: make the change, recapture only the frames it touches as a new before/after, republish, and reply on the comment with what changed.
- One URL for the life of the feature. Republish the same file; never a new link per round.

## The bar

Every "Confirmed" has a frame they can see. Every change has a before and an after. Failures are shown, not dropped. The in-between states are captured, not just the end screens. The verdict line is true if it's the only thing they read.
