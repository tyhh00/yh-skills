---
name: consistent-design
description: Build UI where every color, spacing, radius, icon, and typography choice is grounded 1:1 in an existing usage. Use whenever you write or change any front-end/UI/styling code (a component, a modal, a page, a Tailwind class, a token). The rule: treat each design decision like code that must COMPILE against the existing design system. A token that does not resolve to (a) a real design-system token AND (b) an existing usage for the same UX purpose is a compile error, not a style choice. No invented hex, no arbitrary colors, no random spacing, no guessed icons, no reinvented shells. Every choice is proven with file:line and a one-line UX rationale, delivered as a grounding table alongside the component. When there is no existing precedent, ask; do not invent. Invoke with /consistent-design.
---

# /consistent-design — Design decisions are compiled, not improvised

The one belief this skill enforces: **a UI is code, and its colors/spacing/icons are typed values that must resolve against the existing system.** "It looks fine" is not a passing build. Every visible choice must trace to something already in the codebase, used for the same purpose. If it can't, it doesn't ship — you either find the right existing source or you ask.

This exists because the default failure mode is *inventing*: a garish `bg-accent-red/20` card that clashes with the surface it sits on, a random icon, a hand-picked hex, a bespoke modal when a two-pane shell already exists. Each of those is a compile error that a human then has to catch and reject. This skill catches them first.

## Stance (read first)

- **Reuse is the default; invention is a bug.** Before writing a single class, assume the component, the shell, the token, and the icon already exist somewhere. Your job is to *find and lift* them, not to author new ones.
- **Every decision is typed.** A color is not "blue-ish" — it is a named token (`--color-...` / a theme utility). A spacing is not "some padding" — it is the scale the system uses. Raw hex, arbitrary px, and one-off values are untyped and therefore rejected.
- **Same token, same purpose.** Lifting a token is not enough; it must be lifted from a usage that means the same thing. Error text color comes from where the system already colors errors, not from "a red I liked."
- **Look before you build.** If there is a live surface (a screenshot, a running page, the sibling this renders next to), read it first. You are matching a real thing, not designing in a vacuum.
- **Prove it or cut it.** The deliverable includes a grounding table: element → exact class/icon → source `file:line` → the UX concept that justifies it. A row you can't fill is a choice you can't make.
- **No precedent → ask, don't invent.** If nothing in the system covers what you need, that is a signal to stop and ask the human (`ask_user_question`), or to flag it explicitly — never to quietly make something up.

## Phase 0 — Find the ground truth

Before writing UI, pin the sources of truth:

1. **The design-system token file.** Where the colors/spacing/radius/typography live (e.g. a theme CSS with `@theme`, a tokens file, a Tailwind config). This is the *type system*. You may only use names defined here.
2. **The component library.** The sanctioned primitives/compounds/patterns (buttons, dialogs, inputs, meters). You compose these; you do not re-implement a button/modal/popover inline.
3. **The project's UI rules.** Read the repo's `CLAUDE.md` / style docs for the className util to use (`clsx` vs `cn`/`twMerge`/`cva`), the CSS-first vs variant pattern, deprecated dirs to avoid, naming conventions.
4. **The nearest sibling + the live render.** The component that will sit *next to* yours in the UI, and — if available — a screenshot or the running page. Its classes are your strongest precedent. If the user hands you a screenshot or a URL, look at it.

## Phase 1 — Derive every element from an existing usage

Decompose the thing you're building into its atoms — **surface/box, text (each role: title/body/caption), icon, button, badge/pill, spacing/radius/shadow** — and for **each atom**:

1. **Grep the codebase** for an existing component using that atom for the **same UX purpose** (an error line, a warning label, a tier badge, a primary action, an info sub-text, a panel container).
2. **Lift its exact classes verbatim.** Same token, same size, same weight. Do not "improve" it.
3. **Record the source** (`file:line`) and the **UX concept** that makes it the right precedent.

Concrete precedents to hunt for (map yours to theirs):
- **Surface / container** → the panel/card/composer already on that screen (match its `bg-*` + `border-*` + `rounded-*`).
- **Error / blocking text** → wherever the system renders form/validation/error copy.
- **Warning / attention** → wherever it renders a soft warning (past-due, near-limit).
- **Neutral info sub-text** → the label/caption pattern (e.g. an info-cell's caption).
- **Primary / secondary action** → the existing primary button and the existing secondary/text-link in the *same context* (a modal's CTA vs a text link).
- **Badge / pill / status chip** → the existing tier/status/discount pill (lift the ring + tint + text token together).
- **Icon** → the icon the analogous existing component uses (and its exact `size`/`strokeWidth`). If the analogous component uses **no** icon, you use none.

## Phase 2 — The grounding table (required deliverable)

Ship the component **with** a table proving every choice. No table, not done.

| Element | Exact class / icon | Source (file:line) | UX concept (why this, here) |
|---|---|---|---|
| Box surface | `rounded-… border … bg-…` | `path:line` | the surface it sits on / next to |
| Title (blocking) | `text-… text-<error-token>` | `path:line` | the system's error/blocking treatment |
| Sub-text | `text-… text-<muted>` | `path:line` | the info/caption pattern |
| CTA | `variant=… size=…` | `path:line` | the existing action button for this job |
| Icon | reused / none | `path:line` | the analogous component's icon (or its absence) |

Every cell filled = a build that compiles. A blank cell = stop and resolve it (find a better source, or ask).

## The compile check (run it on every token)

For any class/token you're about to write, both must pass or you don't use it:
1. **Resolves in the type system** — the token name exists in the design-system file (`grep` it). No raw hex, no `#…`, no arbitrary `bg-[…]`/`p-[…]` outside the scale unless the system itself does.
2. **Has a same-purpose usage** — an existing component uses it for the same UX concept (`grep` it). If it exists but only for a *different* purpose, it's the wrong token.

## Reject-list (these are compile errors, not styles)

- Inventing a color (raw hex / arbitrary Tailwind color) instead of a token.
- A token used for a purpose it isn't used for elsewhere ("a red I liked" for a non-error).
- Garish accent-tinted cards on a surface that uses a neutral raised token — match the surface, tint only the small signal (icon/label) if the system does.
- Inventing an icon (or its size/stroke) instead of reusing the analogous component's icon; adding an icon where the analogous component has none.
- Reimplementing a button/modal/input/popover inline instead of composing the library primitive.
- Guessing spacing/radius/shadow instead of the token scale.
- Copy with em-dashes or filler when the house style forbids it — check the style doc.

## Deliverable

The component (composing existing primitives, using only typed tokens lifted from same-purpose usages) **plus** the grounding table. State plainly which atoms had a clean precedent and which (if any) had none — the latter are the only places a human decision is needed, and you surface them rather than invent.
