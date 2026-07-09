# Kay glossary

Plain-language definitions for the terms Kay uses. (Kay glosses each term the first
time it appears in output too — this file is the reference.)

- **Spec-driven development (SDD)** — write a short structured spec first (what to
  build, how it behaves, the steps), build to it, then check the result against it.
  The spec is the source of truth, not the prompt.
- **Capability** — one coherent area of behavior (e.g. `auth`, `todo-list`). Canonical
  specs live one folder per capability under `.kay/specs/`.
- **Change** — one unit of work flowing through the loop, on its own `kay/<id>`
  branch, with its artifacts under `.kay/changes/<id>/`.
- **Canonical spec** — the living, current description of how the system behaves,
  in `.kay/specs/`. Updated only at `/k-review` fold time.
- **Delta spec** — one change's proposed edits to the canonical specs (ADDED /
  MODIFIED / REMOVED), written during `/k-spec`.
- **EARS** — *Easy Approach to Requirements Syntax*: five fill-in-the-blank forms for
  testable requirements (see `spec-format.md`).
- **Scenario** — a GIVEN/WHEN/THEN example of a requirement in action; `/k-verify`
  runs these against the real build.
- **Living spec** — a spec kept true to the code: when the build forces a change, the
  spec is updated to match reality, never left to drift.
- **Gate** — a checkpoint that flags problems and waits for your decision, rather than
  passing silently. Kay's gates are **warn + explicit override**.
- **Constitution** — the project's non-negotiable principles and detected stack, in
  `.kay/constitution.md`; every command reads and obeys it.
