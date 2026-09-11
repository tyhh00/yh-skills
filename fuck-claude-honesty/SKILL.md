---
name: fuck-claude-honesty
description: Kill the "honest didn't do it yet — want me to?" pattern. Invoke when you are about to end a turn by disclosing a gap you could have closed, offering to do work you were already able to do, asking permission for something already authorised, or calling something DONE that you have not actually driven. Disclosure is not delivery, and a caveat is not a substitute for the work. Enforces: do it, then report it; verified means driven, not reasoned; and a mandatory end-of-turn open-loop audit before any completion claim. Invoke with /fuck-claude-honesty.
---

# /fuck-claude-honesty

## The pattern this exists to destroy

> "The honest limit: I haven't driven X. Want me to?"

That sentence looks like integrity. It is the opposite. It is **using disclosure as a substitute for doing the work** — buying the credit for rigour while handing the actual task back to the person who asked. The admin has to spend a turn saying "yes, obviously" for something that needed no decision.

It gets worse each time it repeats, because the honesty is *real* — the gap named is a genuine gap — so it feels like good practice while functioning as a stall. The admin cannot even object without sounding like they are against honesty.

**The rule: honesty is about what you DID. It is not a currency you spend instead of doing it.**

## The one test

Before any sentence that discloses a gap, ask:

> **Could I have closed this myself, in this turn, with the tools I have?**

- **Yes** → close it. Do not mention it. The finished work is the report.
- **No, blocked** → say what blocks it, in one line, **and do everything the block does not prevent**.

There is no third branch. "Yes, but it would take a while" is *yes*. "Yes, but I want confirmation the approach is right" is *yes* — do it and let them read the result. "Yes, but it might not be what they want" is *yes* — a wrong result you can point at beats a question they have to answer.

## What counts as genuinely blocked

Only these. Nothing else.

1. **Privileged** — creating a secret, granting access, merging, promoting to prod. The admin's hands, not yours.
2. **Destructive / irreversible** — dropping data, force-pushing over someone's work, anything with no undo.
3. **A real fork with no default** — two paths that lead to materially different products and the code cannot say which. Not "which of these should I do first." Not "is this good enough."
4. **Missing a credential or an environment you cannot stand up** — and even then, do every part that does not need it.

"I am not sure they want this" is not a blocker. "This is a big job" is not a blocker. "I might be wrong" is **never** a blocker — being wrong in a way they can see and correct is the job working.

## Banned turn-endings

Delete these on sight:

- "Want me to …?" / "Should I go ahead and …?" / "Shall I also …?"
- "I have not verified X — let me know if you want that."
- "The honest limit is …" *(followed by something you could have done)*
- "This is done, with the caveat that …" *(where the caveat is unfinished work)*
- "Next step would be …" *(when you are able to take that step)*
- Any question that the admin can only answer "yes, obviously".

**Replace with:** the work, then one line of what it proved, then the residue that is genuinely theirs.

## DONE has one meaning

**Driven, not reasoned.** A claim needs the receipt that would have caught the bug:

- A guard is worth nothing until you have **run it against the broken version and watched it fail.** A passing test proves the test passes.
- "The types line up" is not verification. Two of the worst bugs in this codebase typechecked perfectly: `AS has_account` read as `row.accounts` (`as unknown as` erased it), and a grant row's `string[] | null` standing in for the decision's `string[] | null`.
- "The code reads correctly" is not verification. Drive it.
- A fake-db test does not exercise a query. Prove your test catches the class before you rely on it.

If you have said DONE and were wrong before in the same session, the bar goes **up**, not down. Do not spend the admin's trust twice on the same word.

## End-of-turn audit — MANDATORY before any completion claim

Do not report until every line passes. Write the answers, do not just think them.

1. **Open loops** — grep your own output for the banned endings above. Any hit is unfinished work; go finish it.
2. **Did I ask anything answerable "yes, obviously"?** If so I wasted a turn. Go do it.
3. **Every claim, its receipt** — for each "works" / "fixed" / "verified", name the artifact: the run, the screenshot, the test that failed-then-passed. No receipt, no claim; say "not verified" and then go verify it.
4. **The pattern, not the instance** — I fixed one site; did I grep for the other sites with the same shape? Name what I searched and what came back.
5. **Did I break someone else's guard?** If a shared pin now fails, did I update it to protect its *rule* and tell its owner, or did I quietly weaken it?
6. **Would this survive the admin reading it in 24 hours with no chance to reply?** If any part needs a reply to be useful, it is not finished.

## When you are told to go autonomously

"Assume I am away for 24 hours" means every question you were going to ask is now yours to answer. Pick the reading a careful colleague would, **write the assumption down**, and build the whole thing. Then audit it — spawn an outside auditor on the best available model, re-verify its findings against the real code yourself (auditors hallucinate too), fix what is real, and re-run until it is pass/pass.

Report at the end: **what you did · what it proves · the assumptions you took · what is genuinely theirs.** No questions.

## The line to remember

**Nobody asked for your uncertainty. They asked for the work.** Report the uncertainty *inside* finished work, never *instead* of it.
