---
name: k-review
description: Quality-gate a verified Kay change, then fold its delta spec into the canonical specs, archive the change, and merge the branch. The last gate before a change becomes the source of truth. Invoke with /k-review <change-id>.
argument-hint: "<change-id>"
allowed-tools: shell
---

# /k-review — quality gate, then fold and merge

The `change-id` is in the prompt arguments. If empty, list `.kay/changes/` and ask
which one.

## Step 0 — Load

Be on the change branch (`git checkout kay/<id>`). Read `proposal.md`, `design.md`,
`tasks.md`, the delta specs, `verification.md`, and `.kay/constitution.md`. Get the
actual diff of the change versus the base branch (`main`):

```
git diff main...kay/<id>
```

## Step 1 — Review as ordered, gated passes

Don't review everything at once and gate once at the end. Run these passes in order,
**gating after each** — a pass with an unresolved blocker or should-fix **halts the
pipeline** until the user fixes or consciously overrides; a clean or not-applicable
pass advances with no prompt.

1. **Security** — hardcoded secrets, injection at trust boundaries, and (where there's
   a package manager) obvious dependency risk. A deliberately small floor, run first
   so a blocker stops everything before more effort.
2. **Core** — the five generic dimensions, as one pass:
   - **Correctness** — does the code do what it claims? Logic errors, unhandled cases.
   - **Maintainability** — clear names, no needless complexity, no dead code.
   - **Spec-compliance** — is every ADDED/MODIFIED requirement actually satisfied by
     the diff? Cross-check against `verification.md`.
   - **Principles** — was quality traded for speed anywhere without being flagged? Is
     user-facing output plain-language, with jargon glossed?
   - **Stack-specific risks** — edge cases, performance, as relevant to the stack.
3. **QA** — does it actually work for users: edge cases, error states, and (for a UI)
   accessibility. Skip with a one-line note if it doesn't fit the stack.

## Step 2 — Record findings (per pass)

In `.kay/changes/<id>/review.md`, give **each pass its own section** (Security / Core
/ QA). Under each, list its findings — each with a **severity** (blocker / should-fix
/ nit), a location, and a recommended fix — or "clean", or "skipped — not applicable:
<why>". Append a pass's section as you finish reviewing it, before its gate.

## Step 3 — Gate each pass (warn + override, fail-fast)

After a pass's findings are recorded, if it has an unresolved **blocker** or
**should-fix**, surface it with the fix and — per the gate policy — require the user
to fix or consciously override **before the next pass runs**. A clean or skipped pass
auto-clears. Offer to fix blockers now. **Fold only after every pass has cleared or
been overridden.**

## Step 4 — Fold (on accept or override)

Apply each delta to the canonical specs under `.kay/specs/`:

- **ADDED** requirements → append to (or create) `.kay/specs/<capability>/spec.md`.
- **MODIFIED** requirements → replace the matching requirement (by title) in the
  canonical spec.
- **REMOVED** requirements → delete them from the canonical spec.

Do this on the change branch. After folding, the canonical spec must read as the
true, current behavior — **no leftover deltas**.

## Step 5 — Archive

Move the change folder to `.kay/changes/archive/<id>/`, keeping proposal, design,
tasks, deltas, analysis, verification, and review as the audit trail:

```
mkdir -p .kay/changes/archive
git mv .kay/changes/<id> .kay/changes/archive/<id>
git add -A && git commit -m "review(<id>): fold specs, archive change"
```

## Step 6 — Merge

Integrate the branch into the base (`main`):

- **Default (local merge):** confirm with the user first, then
  `git checkout main && git merge --no-ff kay/<id>`. Report what landed.
- **If the project uses pull requests** (`gh` is available and a remote is
  configured): `git push -u origin kay/<id>` then `gh pr create --base main --fill`,
  and let a human/CI merge on the platform instead. Confirm before pushing —
  publishing a branch is outward-facing.

Pick the local merge unless the user asks for a PR.

## Step 7 — Suggest next

Summarize what shipped — the change is folded into `.kay/specs/` as living truth and
archived with its full audit trail — and point at the next change.

## Rules

- A change becomes truth only after every pass clears (or is consciously overridden).
- After fold, canonical specs describe current behavior with no dangling deltas.
- Obey the constitution: flag quality-vs-speed trade-offs; gloss jargon on first use.
