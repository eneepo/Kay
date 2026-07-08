---
name: k-verify
description: Verify a built Kay change behaves the way its spec says — run each requirement's GIVEN/WHEN/THEN scenario against the real build and record pass/fail with evidence. Invoke with /k-verify <change-id>.
argument-hint: "<change-id>"
allowed-tools: shell
---

# /k-verify — check the build against the spec's scenarios

The `change-id` is in the prompt arguments. If empty, list `.kay/changes/` and ask
which one.

> Verification here is **behavioral**: instead of only reading the code, you run the
> thing on a concrete example and check what actually happens against what the spec's
> scenario said should happen. A scenario that says "WHEN init runs THEN
> `.kay/constitution.md` exists" means you actually run it and check the file is
> there.

## Step 0 — Locate

Be on the change branch (`git checkout kay/<id>`). Read every delta spec under
`.kay/changes/<id>/specs/` and collect **every scenario** (GIVEN/WHEN/THEN). Read
`tasks.md` and `design.md` for context.

## Step 1 — Plan a real check per scenario

For each scenario, decide how to exercise it for real:

- If the stack has automated tests that cover it, run them.
- Otherwise build a concrete fixture: set up the GIVEN, perform the WHEN (run the
  command / call the code / drive the behavior), and observe the result.

For a web page, "perform the WHEN" means loading the page and driving the interaction
(a headless browser if one is available, otherwise open it and check the observable
result).

## Step 2 — Run them, and loop on failure

Execute each check and capture **real evidence**: command output, files created or
changed, exit codes, messages observed. Don't assert from reading alone — make the
behavior actually happen.

If a scenario **passes**, record PASS and move on. If it **fails**, enter a bounded
**fix-and-re-run loop**:

1. **Diagnose** — record the failure and a short diagnosis.
2. **Fix** — hand the failing scenario + diagnosis back to the build step and apply
   the smallest code fix. (Verify verifies; the fix is a build edit.)
3. **Re-run** the scenario and record the result.
4. **Repeat** until it passes or the **retry budget** (default 3 attempts) is reached.

> After a fix lands, **re-run the other scenarios too** — a fix can regress a
> previously-green scenario.

A scenario that passes within budget is a PASS; one still failing when the budget is
exhausted falls to the gate (Step 4).

## Step 3 — Record (every scenario, every attempt)

Write `.kay/changes/<id>/verification.md`: every scenario → **PASS / FAIL**, each with
the evidence you captured, and for failures, expected vs actual. For a scenario that
looped, record each attempt — its diagnosis, the fix, and the re-run result — so the
path to green (or to the gate) is visible. Commit it on the branch:

```
git add .kay/changes/<id>/verification.md
git commit -m "verify(<id>): scenario results"
```

## Step 4 — Gate after the budget (warn + override)

If every scenario passes (including those fixed within budget), say so and hand off.
If a scenario is **still failing after its retry budget is exhausted**, per the gate
policy: report the failure clearly and require the user to fix or consciously override
before proceeding. Never paper over a failing scenario — but give the loop its
budgeted attempts first.

Then tell the user the next step is `/k-review <id>`.

## Rules

- Behavioral evidence beats inspection — a scenario isn't verified until you've seen
  it happen.
- Obey the constitution: flag quality-vs-speed trade-offs; gloss jargon on first use.
