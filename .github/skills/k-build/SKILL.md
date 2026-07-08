---
name: k-build
description: Implement a Kay change to its spec, on the change's kay/<id> branch. Works through the task list, enforces test-first where a test runner exists, and keeps the spec true to the code. Invoke with /k-build <change-id>.
argument-hint: "<change-id>"
allowed-tools: shell
---

# /k-build — implement a change to its spec

The `change-id` is in the prompt arguments. If empty, list `.kay/changes/` and ask
which one.

## Step 0 — Load context

Read the change's `proposal.md`, `design.md`, `tasks.md`, and every delta spec under
`.kay/changes/<id>/specs/`. Read `.kay/constitution.md` and
`.kay/reference/spec-format.md`.

Make sure you're on the change branch (`git checkout kay/<id>`) and the spec work is
committed.

**Detect the test runner.** From the constitution's Stack section, read the "Test
runner" field. A named tool (`pytest`, `jest`, `go test`, …) means the project **has
a test runner** → test-first is enforced in Step 1. A value of "none" / "behavioral"
/ empty means **no test runner** → take the fallback path. State which mode you're in
before implementing.

## Step 1 — Implement, task by task

Work through `tasks.md` in order.

**Where the project HAS a test runner — enforce test-first (TDD).** For each
*testable* task (one a test could exercise — not a docs/config edit):

1. **Write the test first**, for the task's requirement/scenario.
2. **Run it and watch it fail** (red) — a test never seen to fail proves nothing.
3. **Implement** the smallest change that makes it pass.
4. **Run it again and watch it pass** (green).
5. Only then check the task off (`- [x]`).

If you catch yourself implementing a testable task **without** a failing test first,
stop: flag it and either add the test or get a conscious override (warn + override).
Non-testable tasks (docs, config) need no test — note them as such.

**Where the project has NO test runner — fallback.** State plainly that test-first
doesn't apply, then implement the smallest change per task and rely on the sanity
check in Step 3. (`/k-verify` will exercise each spec scenario for real later.)

Either way: implement the smallest change that satisfies the task and its referenced
requirement, then check it off in `tasks.md`. Stay within the proposal's scope — if
you catch yourself doing something not in `tasks.md`, either fold it into `design.md`
or drop it as scope creep.

## Step 2 — Keep the spec living

If implementation forces a divergence from the delta spec — a requirement was wrong,
a scenario needs adjusting, an edge case appears — **update the delta spec to match
what you actually built**, and note why in `design.md`. Never let spec and code drift
apart; a wrong spec is worse than no spec.

## Step 3 — Sanity check

Run whatever build / test / lint the stack provides and confirm it's green. For a
project with no test runner, do a structural check instead (files exist, the thing
runs, output looks right). Report exactly what you ran and the result.

## Step 4 — Commit and hand off

Commit the work on the branch with a clear message:

```
git add -A
git commit -m "build(<id>): implement <short summary>"
```

Tell the user the change is built on `kay/<id>` and the next step is
`/k-verify <id>`.

## Rules

- Obey the constitution: flag quality-vs-speed trade-offs; gloss jargon on first use.
- Stay within the change's scope.
- Spec and code must agree when you finish.
