---
name: k-autopilot
description: Drive a specced Kay change through analyze → build → verify → review unattended, in the current session. Each gate resolves automatically — clean proceeds, anything needing a human halts with a report — and the run ends at a reviewed, folded, archived change ready to merge (it never merges). Invoke with /k-autopilot <change-id>.
argument-hint: "<change-id>"
allowed-tools: shell
---

# /k-autopilot — fly one change through the loop, hands-off

The `change-id` is in the prompt arguments. If empty, list `.kay/changes/` (ignoring
`archive/`) and ask which one.

> **Autopilot** — Kay drives a specced change through its own pipeline unattended,
> handing control back when something needs judgment: like a plane's autopilot flying
> the route while the pilot takes over on anything tricky. It runs
> `/k-analyze → /k-build → /k-verify → /k-review` per each skill, and at every gate it
> reads the verdict instead of prompting — a clean gate proceeds, a gate that needs a
> human halts.

**Standing consent:** invoking this command consents to the whole run proceeding with
**no mid-run prompts**, up to a **reviewed, folded, and archived change ready to
merge**. Autopilot **never merges** — merging stays a human act. If you'd rather
approve each gate yourself, run the commands individually.

## The three gate outcomes

At each gate, autopilot replaces the interactive "warn + override" with an automatic
reading of the **same** findings, in three classes:

- **clean** — no issues → proceed.
- **auto-overridable** — only nit-level findings, or a fork Kay resolved itself with a
  clear recommendation → proceed, recording it as the driven command normally would.
- **must-stop** — something needs a human → halt (Step 4). Concretely:
  - `/k-analyze` found a real issue (uncovered requirement, orphan task, a failed
    EARS/testability check, a canonical mismatch);
  - `/k-build` hit a flagged quality-vs-speed trade-off or a skipped test-first step
    with no clear call;
  - `/k-verify` has a scenario still failing after its retry budget;
  - `/k-review` has a standing **blocker** or **should-fix** in any pass.

## Step 0 — Guard

- If `.kay/` does not exist → tell the user to run `/k-init` first and **stop**.
- If `.kay/changes/<id>/` does not exist, or branch `kay/<id>` has no committed spec
  artifacts (proposal, delta specs, design, tasks) → report what's missing, name
  `/k-spec` as the fix, and **stop without driving anything**. Autopilot starts where
  `/k-spec` ended; it never specs.

## Step 1 — Detect the phase (first runs and resumes)

Check `kay/<id>` for completed-phase artifacts and drive **only what remains**, in
order:

| Artifact | Phase it completes |
|---|---|
| `analysis.md` with a clean verdict | analyze |
| build commit with `tasks.md` fully ticked (`- [x]`) | build |
| `verification.md` with every scenario PASS | verify |
| folder moved to `.kay/changes/archive/<id>/` | review |

A **must-stop** artifact (a halted gate) is *not* a finished phase — it's the resume
point: re-run that phase. Never re-run a completed phase. This is also the resume
path: after a halt, fix the cause and re-run `/k-autopilot <id>` to pick up at the
halted phase. If nothing remains, say the change is already reviewed and stop.

## Step 2 — Announce

Tell the user the flight plan in one line (which phases will run) and remind them of
the standing consent — the run ends at a reviewed, archived change **ready to merge**,
never merged.

## Step 3 — Drive the remaining phases

For each remaining phase in order — analyze, build, verify, review — **run that
command exactly per its own `.github/skills/k-<phase>/SKILL.md`**, with one
difference: at the gate, don't prompt — read the outcome (above):

- **clean / auto-overridable** → proceed to the next phase. Everything the command
  records (its report, its notes) is still written; only the resolution changes.
- **must-stop** → go to Step 4. Do not start the next phase.

**Review-phase carve-out.** Run `/k-review`'s passes, then its **fold + archive +
commit** — but **stop before the merge**. Autopilot never merges; it leaves the change
reviewed, folded into `.kay/specs/`, and archived on `kay/<id>`, ready for you to
merge. (Where the project uses pull requests — `gh` plus a remote — the standing
consent covers pushing the branch and opening a PR, but still never merging.)

## Step 4 — Halt (on any must-stop)

Stop **before** the next phase. Then:

1. **Optionally notify** — if a desktop notifier is available, tap the user on the
   shoulder (macOS: `osascript -e 'display notification "<id>: halted at <gate>" with
   title "Kay autopilot"'`; Linux: `notify-send "Kay autopilot" "<id>: halted at
   <gate>"`). Use only the change-id and gate name — never interpolate free text into
   the shell command. If no notifier exists or it fails, skip it silently.
2. **Report** in plain language: **which gate halted**, its **findings** (the failing
   scenario, the flagged issue, the standing should-fix), and the **resume path** —
   fix the cause (or override it interactively by running that one command), then
   re-run `/k-autopilot <id>` to continue from this phase.
3. **End the run.** A halt is not an override — the issue stands, and nothing
   downstream has run.

## Step 5 — Complete

When the review phase finishes (change folded and archived), report: what shipped,
that the specs are folded into `.kay/specs/` and the change is archived with its audit
trail, and the **one remaining human step** — merge `kay/<id>` (via `/k-review`'s
merge step or your PR flow). Point at the next change.

## Rules

- Drive the four commands per their own skills — autopilot adds gate *resolution*, not
  new mechanics. Never re-implement or shortcut a driven command's steps.
- `must-stop` always waits for a human; auto-proceeding on clean / auto-overridable is
  the user-invoked carve-out this command exists for.
- Never merge the change; never delete the change branch; never drive `/k-spec`.
- Obey the constitution: flag quality-vs-speed trade-offs; gloss jargon on first use.
