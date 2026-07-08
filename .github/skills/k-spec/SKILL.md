---
name: k-spec
description: Turn an idea into a Kay change — clarify it, then write the proposal, requirements (EARS), design, and task list as a delta against the current specs, on a kay/<id> branch. Use when asked to spec a feature or start a new change. Invoke with /k-spec "<idea>".
argument-hint: "<a short description of the idea>"
allowed-tools: shell
---

# /k-spec — turn an idea into a change

The idea is in the prompt arguments. If none was given, ask the user what they want
to build, then continue. This command produces a change's **spec artifacts** only —
it writes no implementation code (that is `/k-build`'s job).

## Step 0 — Load context

Read `.kay/constitution.md`, `.kay/reference/spec-format.md`, and
`.kay/reference/glossary.md`. Scan `.kay/specs/` to learn the current truth and which
capabilities already exist. Scan `.kay/changes/` (ignoring `archive/`) for in-flight
changes so you don't duplicate one.

If `.kay/` does not exist, tell the user to run `/k-init` first and stop.

## Step 1 — Clarify (one question at a time)

Ask only what you genuinely need to make the requirement unambiguous:

- the concrete outcome / success condition,
- scope boundaries and explicit non-goals,
- which existing capabilities it touches,
- any constraints (compatibility, dependencies).

Ask **one question, wait for the answer, then ask the next.** Stop as soon as the
requirement is clear — don't pad with questions you can already answer. Gloss any
jargon.

## Step 1b — Approval gate (recap, then explicit go-ahead)

Before creating **any** branch, folder, file, or commit, present a short recap and
**stop** until the user explicitly approves. A clarifying exchange is **not** consent
— answering questions tells you *what* to build, not that you *may* build it.

Recap these parts:

- **What** — the change in a sentence or two.
- **Scope** — what's included, and the notable non-goals.
- **Key decisions** — the choices you're making, with your recommendation where one
  answer is sounder; flag any quality-vs-speed trade-off.
- **Proposed change-id** — the kebab-case id you'll use (e.g. `add-clear-completed`).

Then wait. Only an **explicit affirmative** ("go ahead", "approved", "build it")
advances. A decline, edits, or a non-committal reply ("looks ok", silence) is **not**
consent — fold in feedback and re-present.

## Step 2 — Name and branch

Derive the short kebab-case `change-id` (the one approved at the gate). Confirm it's
not already taken under `.kay/changes/`. Then create the branch and folders:

```
git checkout -b kay/<change-id> 2>/dev/null || git checkout kay/<change-id>
mkdir -p .kay/changes/<change-id>/specs
```

## Step 3 — Proposal

Write `.kay/changes/<change-id>/proposal.md`:

- **Why** — the problem, in plain language.
- **What** — the change in one paragraph.
- **Scope** — what's included.
- **Non-goals** — what's deliberately out.
- **Success criteria** — measurable conditions for "done".

## Step 4 — Delta specs

Identify the affected capabilities. For each, write
`.kay/changes/<change-id>/specs/<capability>.md` in the **delta format** from
`spec-format.md` (ADDED / MODIFIED / REMOVED, EARS requirements, **at least one
GIVEN/WHEN/THEN scenario per requirement**). Scenarios are what `/k-verify` runs
later — make them concrete and checkable. Before writing MODIFIED or REMOVED entries,
read the matching canonical spec so the delta references real requirements.

## Step 5 — Design

Write `.kay/changes/<change-id>/design.md`: the approach, key decisions, alternatives
briefly considered, risks and edge cases, and the files you expect to touch. Where a
decision trades quality or maintainability for speed, **flag it and recommend the
sounder option**.

## Step 6 — Tasks

Write `.kay/changes/<change-id>/tasks.md` as an ordered `- [ ]` checklist of small,
independently checkable steps. Lean test-first where a test runner exists.

Make tasks **traceable** — this is what `/k-analyze` checks next:

- Each task is small enough to check on its own (one behavior or edit).
- **Every task cites the requirement it satisfies** — e.g. `— satisfies "<Requirement
  title>" / scenario "<scenario name>"`.
- **Every delta requirement is cited by at least one task.** A requirement with no
  task is a coverage hole; a task citing no requirement is possible scope creep — fix
  either before moving on.

## Step 7 — Quality gate (warn + override)

Self-review the change: every requirement has a scenario; nothing contradicts the
canonical specs; an implementer wouldn't need to ask you anything; scope stays within
the proposal; the design is buildable. List any issues with recommended fixes, and —
per the gate policy — ask the user to fix them or consciously override before
continuing.

## Step 8 — Commit on the branch

Commit the artifacts on `kay/<change-id>` so the change is durable. Stage **only the
change's own folder** — never `git add -A`:

```
git add .kay/changes/<change-id>/
git commit -m "spec(<change-id>): proposal, delta specs, design, tasks"
```

If `git status --porcelain .kay/changes/<change-id>/` is empty, say "already
committed — nothing new" and continue (don't create an empty commit).

## Step 9 — Hand off

Tell the user the change is specced and committed on `kay/<change-id>`, and the next
step is `/k-analyze <change-id>` — the consistency gate before building.

## Rules

- Obey the constitution: flag quality-vs-speed trade-offs; gloss jargon on first use.
- Write no implementation code here.
- One question at a time in the clarify gate.
- A clarifying exchange is not consent: create no branch, file, or commit until the
  Step 1b approval gate has an explicit go-ahead.
