# Constitution: task-service

The project's non-negotiable principles and its detected stack. Every `/k-*` command
reads this file and obeys it.

## Principles (non-negotiable)

1. **Quality over speed.** Kay flags any step that trades correctness or
   maintainability for speed, and recommends the sounder path instead of silently
   taking the fast one.
2. **Plain language by default.** The first time a piece of jargon appears in output,
   it gets a one-line plain-English gloss with a quick example.

## Gate policy

Every gate in the loop is **warn + explicit override**: Kay surfaces issues and
recommends fixes, then waits. Nothing is waved through silently, and only you can
consciously override a standing issue.

## Stack

- **Language(s):** Python 3
- **Framework(s):** none — standard library only (`argparse`, `http.server`)
- **Package manager:** none for the app; `pytest` for tests (install into a venv)
- **Test runner / how behavior is verified:** pytest
- **Base branch:** main
- **Notes:** A layered task manager. A shared core (`storage` → `task-domain`) is
  exposed by two front-ends (`cli`, `api`). Keep the domain independent of storage
  and transport so it stays trivially testable; front-ends should be thin adapters.

## Best practices for this stack

- Keep the layers separate: `storage` knows files, `task-domain` knows tasks, and the
  `cli`/`api` front-ends only translate input/output — never put domain rules in a
  front-end.
- Make domain functions operate on plain data (a list of task dicts) so tests need no
  files or servers.
- Write a pytest test for every requirement's scenario before implementing it
  (test-first). Use `tmp_path` for anything that touches the filesystem.
- Surface errors as clear messages: the CLI exits non-zero, the API returns the right
  HTTP status (400 bad input, 404 unknown id) — never a raw traceback.
- Never let a bad or corrupt store silently wipe data; fail loudly instead.
