---
name: k-retro
description: Run an end-of-session retrospective for Kay — while the conversation is still in context, write a private per-session retro note (summary, timeline, sideways & loops, communication, Kay improvements, wins), then triage the durable signals and, only after you approve, route them (communication preferences to memory, quick fixes to ROADMAP.md, bigger ideas to a queued /k-spec prompt). Invoke with /k-retro.
allowed-tools: shell
---

# /k-retro — look back at the session before you clean up

Run this at the **end of a working session, before cleanup**, while the conversation
is still in context — that live conversation is the retro's richest evidence, and a
fresh run later wouldn't have it.

> **Retro (retrospective)** — a short look-back at a piece of work asking "what
> happened, what went sideways, what should we change" — like a sports team reviewing
> game tape. Here it looks back at a whole Kay *session*.

This command takes **no argument**: it reflects on the session you're in, not on one
change-id. It writes a private note freely, but **never** writes to shared or durable
places (your memory, `ROADMAP.md`, the spec queue) until you approve a triage.

## Step 0 — Guard and load

- If `.kay/` does not exist → tell the user to run `/k-init` first and **stop**,
  writing no files.
- Read `.kay/constitution.md` — its plain-language and quality duties bind this
  command too.

## Step 1 — Gather evidence

The **primary source is the live conversation** you're holding: what the user asked
for, where the work went, where it stalled or looped, what felt like friction. Use it
directly.

Then **anchor it to durable artifacts** where a change was active this session, so
observations are checkable rather than pure recollection: the current branch, today's
commits (`git log --oneline`), and any `.kay/changes/<id>/decisions.md`. **Anchor at
least one observation to a real artifact** (a commit hash or change-id) when a change
was active.

**When no change was active** — the session was only discussion or planning — that's
fine: summarize honestly and **do not invent artifact citations**. A no-change retro
is still a valid retro.

## Step 2 — Write the retro note (private, no approval needed)

Write the note at **`.kay/.local/retros/<date>.md`** (create `retros/` if absent; get
`<date>` as `YYYY-MM-DD` from `date +%F`, never guessed). This lives under the
gitignored `.kay/.local/`, so it's private scratch and leaves no committed footprint —
writing it needs **no** approval.

**Same-day re-run:** if `<date>.md` exists, **append** a `## Retro @ <HH:MM>` block
rather than overwriting, so a day's reflections stay in one file.

The note MUST contain these **six sections, in order**:

```markdown
# Retro — <date> · <session label>

## Summary
What the session set out to do and what actually happened, in a few plain sentences.

## Timeline
The arc of the session as bullets — changes/commands touched, key decisions,
outcomes. Anchor to real artifacts (commit hash, change-id) where a change was active.

## Sideways & loops
Where work went off-track, backtracked, or repeated. For each: the trigger, the tell,
and roughly what it cost. An honest "nothing notable" is valid — don't fabricate.

## Communication
Two-sided, concrete suggestions — at least one for the **user** (what to say
earlier/differently) and one for the **agent** (what to ask or do differently).

## Kay improvements
Friction that's a **framework gap**, not a one-off — candidate changes to Kay itself,
each a crisp, actionable item. This is the section Step 3 triages.

## Wins
What worked and is worth keeping, so it's reinforced rather than lost.
```

## Step 3 — Triage the improvement ideas

> **Triage** — sorting items by what each one needs, the way an ER sorts patients.

For **each** idea in the note's *Kay improvements* section, classify it into **exactly
one** of three routes, and collect any **communication preferences** worth remembering
across sessions (from the *Communication* section):

- **quick-fix** — a small change worth capturing in `ROADMAP.md`;
- **bigger** — worth its own change; becomes a ready-to-run `/k-spec` prompt;
- **one-off** — session-specific, not worth persisting; dropped.

Present the triage as a table plus the proposed memory entries:

| Idea | Route | Destination |
|---|---|---|
| … small wording fix … | quick-fix | ROADMAP.md |
| … new capability … | bigger | queued /k-spec prompt |
| … one-time gripe … | one-off | dropped |

## Step 3b — Approval gate (before ANY durable write)

**Stop and ask for explicit approval of the triage.** The private note may already
exist — that's fine — but **nothing durable is written yet**:

- **Explicit approval** → proceed to Step 4.
- **Decline, edits, or a non-committal reply** → write **nothing** durable; leave your
  memory, `ROADMAP.md`, and the queue untouched. Fold in edits and re-present.

## Step 4 — Route the durable signals (on approval only)

- **Communication preferences → your memory.** Save each as a durable preference.
  **Degrade by policy:** where no memory mechanism is available, do **not** probe or
  error — keep the preferences in the retro note and tell the user they weren't
  persisted.
- **Quick-fix ideas → `ROADMAP.md`.** Append each as a concise bullet, editing the
  file in place. If the project has no `ROADMAP.md`, leave the quick-fix in the retro
  note and say so rather than creating one in a project that doesn't want it.
- **Bigger ideas → `.kay/.local/retro-queue.md`.** Append each as a ready-to-run
  prompt, one per line, newest last, in the exact form
  `/k-spec "<the idea, phrased as a change to build>"`, so a later session runs it
  directly. Create the file if absent (it's under the gitignored `.kay/.local/`).
- **One-off ideas** → not persisted.

## Step 5 — Report

Tell the user, in plain language: where the note was written, what was routed where
(and what was dropped), and — if anything was queued — that
`.kay/.local/retro-queue.md` now holds ready-to-run `/k-spec` prompts for next time.

## Rules

- Obey the constitution: flag quality-vs-speed trade-offs; gloss jargon on first use.
- The private note is free; every durable/shared write waits behind the Step 3b
  approval gate.
- Never auto-run `/k-spec` — bigger ideas are *queued* as prompts, never executed.
- Never fabricate friction, wins, or artifact citations — an honest thin retro beats
  an invented rich one.
