---
name: k-init
description: Set up Kay in this project. Detects the stack, creates the .kay/ folder, and seeds the constitution, spec format, and glossary. Run once per project, or re-run to refresh reference files. Use when asked to set up Kay or start spec-driven development. Invoke with /k-init.
allowed-tools: shell
---

# /k-init — set Kay up in this project

Your job: make this repo ready for spec-driven development with Kay by creating the
`.kay/` folder and its seed files. Be **idempotent** — never overwrite a file the
user may have edited.

> First time you mention it: **spec-driven development (SDD)** means writing a short
> structured spec (what to build, how it should behave, the steps) *before* coding,
> then building to that spec. The spec is the source of truth, not the prompt.

## Step 1 — Detect the stack

Inspect the repo root and infer:

- **Language / framework** — check for `package.json` (Node/JS/TS),
  `pyproject.toml` / `requirements.txt` (Python), `go.mod` (Go), `Cargo.toml` (Rust),
  etc.
- **Package manager** (npm / pnpm / yarn / poetry / uv / cargo / …).
- **Test runner** (jest / vitest / pytest / `go test` / …). If there is no
  conventional runner — for example a static site or a docs project — record that
  behavior is verified by `/k-verify` running each spec scenario.

Summarize what you found in one short paragraph before writing anything.

## Step 2 — Create the `.kay/` skeleton (idempotent)

Create these directories if they don't already exist (never delete existing content):

```
.kay/ .kay/specs/ .kay/changes/ .kay/changes/archive/ .kay/reference/
```

## Step 3 — Seed the files from the bundled templates

This skill ships templates in its own `templates/` directory (next to this
`SKILL.md`). For each one: read the template, fill the `{{PLACEHOLDERS}}`, and write
the result — but **do not overwrite a file that already exists**; if it exists, leave
it and note that you skipped it.

- `templates/constitution.md` → `.kay/constitution.md`
  Fill `PROJECT_NAME`, `LANGUAGES`, `FRAMEWORKS`, `PACKAGE_MANAGER`, `TEST_RUNNER`,
  `STACK_NOTES`, and `BEST_PRACTICES` (3–6 concrete bullets fitting the stack).
  **Keep the two Principles and the gate policy exactly as written — they are
  non-negotiable.**
- `templates/spec-format.md` → `.kay/reference/spec-format.md` (no placeholders; safe
  to refresh if it exists).
- `templates/glossary.md` → `.kay/reference/glossary.md` (safe to refresh).

## Step 4 — Report

Print a short summary: the stack you detected, which files you created vs skipped,
and the next step — run `/k-spec "<your idea>"` to start your first change. Gloss any
jargon in plain language (per the constitution).

## Rules

- **Idempotent.** Re-running must be safe. Never overwrite `.kay/constitution.md` or
  anything under `specs/` or `changes/` — those hold human decisions. Reference files
  (`spec-format.md`, `glossary.md`) may be refreshed to the latest template.
- **Obey the constitution you just wrote:** flag any quality-vs-speed trade-off, and
  gloss jargon on first use.
