---
name: k-analyze
description: Cross-artifact consistency gate for a Kay change. Reads the proposal, delta specs, design, and tasks and checks they agree with each other and with the canonical specs — builds a requirement-to-task coverage matrix and flags uncovered requirements, orphan tasks, and canonical mismatches. Read-only except its own analysis.md report. Invoke with /k-analyze <change-id>.
argument-hint: "<change-id>"
allowed-tools: shell
---

# /k-analyze — cross-artifact consistency gate

The `change-id` is in the prompt arguments. If empty, list `.kay/changes/` (ignoring
`archive/`) and ask which one.

This command is a **gate**, not a builder. **Cross-artifact** means it compares the
change's separate documents — proposal, requirements, design, task list — against
each other and against the current truth in `.kay/specs/`, instead of reading each in
isolation. It writes nothing except its own report.

## Step 0 — Guard

- If `.kay/` does not exist → tell the user to run `/k-init` first and **stop**.
- If `.kay/changes/<id>/` does not exist → report `<id>` was not found, list the
  in-flight changes, and **stop**.

## Step 1 — Load (read-only)

Read the change's `proposal.md`, every `specs/*.md` delta, `design.md`, and
`tasks.md`. For each capability the delta touches, read the matching canonical spec
`.kay/specs/<capability>/spec.md` if it exists. Read `.kay/reference/spec-format.md`
— its five EARS forms are the source of truth for the Step 3 rigor check.

**Read-only contract:** treat every file above as read-only. The only file this
command writes is its own report, `.kay/changes/<id>/analysis.md`. Recommend fixes;
let the human apply them.

## Step 2 — Coverage matrix

A **coverage matrix** maps each delta requirement to its scenarios and to the tasks
that implement it, so a gap is visible at a glance. For each delta requirement:

- list its scenario name(s);
- list the task(s) whose citation names that requirement title.

Record the matrix in `analysis.md`. A requirement with no matching task shows an
empty task cell — that's a finding for Step 3.

## Step 3 — Consistency checks

Run each check and collect findings. Each finding names the artifact, the problem,
and a recommended fix.

1. **Uncovered requirements** — any delta requirement no task cites → recommend
   adding a task.
2. **Orphan / scope-creep tasks** — any task citing no delta requirement → flag as a
   possible orphan (plumbing tasks like "create the folder" are *possible* orphans,
   not hard errors).
3. **Canonical mismatch** — for each MODIFIED or REMOVED requirement, check its title
   matches an existing requirement in the canonical spec. Skip capabilities the change
   only ADDs (a brand-new capability has no canonical spec yet).
4. **Design gap** — any delta requirement the `design.md` never addresses → recommend
   the design cover it.
5. **Proposal scope** — any delta requirement outside the proposal's stated scope /
   non-goals → flag as scope drift.
6. **EARS rigor & testability** — for each ADDED or MODIFIED requirement, check its
   statement matches one of the five EARS forms in `spec-format.md`, and that the
   behavior is concrete enough to mark pass/fail. Flag vague ones ("… be fast", "… be
   user-friendly") and recommend a checkable behavior.

## Step 4 — Report

Write `.kay/changes/<id>/analysis.md` with: a one-line verdict (clean, or N issues
found); the coverage matrix; and an issues list (each finding with its artifact, the
problem in plain language, and a recommended fix). Overwrite any previous report —
each run is a fresh snapshot.

Then commit it on the branch so it travels with the change:

```
git add .kay/changes/<id>/analysis.md
git commit -m "analyze(<id>): consistency report"
```

If `git status --porcelain .kay/changes/<id>/analysis.md` is empty, say "report
unchanged — nothing to commit" and continue.

## Step 5 — Gate (warn + explicit override)

- **If issues remain:** surface them with recommended fixes, then — per the gate
  policy — ask the user to address them or consciously override before proceeding.
  Don't hard-block; don't pass silently.
- **If clean:** report the artifacts are mutually consistent and name
  `/k-build <id>` as the next step.

## Rules

- Obey the constitution: flag quality-vs-speed trade-offs; gloss jargon on first use.
- Read-only except for `analysis.md`. Never edit the artifacts you judge.
- This is a gate, not a fixer — recommend, then let the human decide.
