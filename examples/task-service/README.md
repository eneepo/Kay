# Lab: task-service (Python, multi-capability, brownfield)

The **most complex** of the three lab starters. A small task manager with a shared
core (`storage` → `task-domain`) exposed by **two front-ends** — a **CLI** and a
**REST API** — over one JSON store. Standard library only; no dependencies to run it.

Use it to exercise the SDD aspects the two simple examples can't:

- **Multiple interdependent capabilities** — a change often spans `task-domain` +
  `cli` + `api`, so `/k-analyze`'s coverage matrix earns its keep.
- **Brownfield / living specs** — this project **already has canonical specs** under
  [`.kay/specs/`](.kay/specs). Your change can **MODIFY** an existing requirement, not
  just add one — exercising `/k-analyze`'s canonical-mismatch check and `/k-review`'s
  fold-into-existing-spec path.
- **Two verification styles in one repo** — test-first for the domain/API (pytest),
  and behavioral (drive the running server) for the API.

## Layout

```
taskservice/
  storage.py     load/save JSON            (capability: storage)
  domain.py      task operations           (capability: task-domain)
  cli.py         argparse front-end        (capability: cli)
  api.py         stdlib HTTP front-end     (capability: api)
tests/           pytest tests for storage, domain, api
.kay/            Kay already initialized — constitution + canonical specs
```

## Run it

```bash
cd examples/task-service

# CLI
python -m taskservice.cli add "buy milk"
python -m taskservice.cli list
python -m taskservice.cli done 1
python -m taskservice.cli rm 1

# REST API (in one terminal)
python -m taskservice.api --port 8000
# then in another:
curl -s localhost:8000/tasks
curl -s -X POST localhost:8000/tasks -d '{"title":"buy milk"}'
curl -s -X DELETE localhost:8000/tasks/1

# tests
python -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m pytest
```

## Your lab exercise

`.kay/` is **already initialized** here, so skip `/k-init` — go straight to `/k-spec`:

```
/k-spec "<your feature>"
/k-analyze <change-id>
/k-build   <change-id>
/k-verify  <change-id>
/k-review  <change-id>
```

### Suggested features (pick one)

- **Due dates** — `add --due YYYY-MM-DD`, store it, show it in `list`, and return it
  from the API. *Spans `task-domain` + `cli` + `api` — a real multi-capability change,
  and a good workout for the coverage matrix.*
- **Rename a task** — a `PATCH /tasks/{id}` endpoint (and a `rename` CLI command).
  *This **MODIFIES** the `api` capability's canonical spec — watch `/k-review` fold a
  change into an existing spec.*
- **Filter the API by status** is already there — instead, add **`GET
  /tasks/{id}`** to fetch one task (404 if unknown).
- **Guard against a huge title** — reject titles over N characters. *A focused
  `task-domain` change with clear pass/fail scenarios.*

> Tip: because the domain is pure and the API routing lives in `dispatch()`, most of
> your scenarios can be verified with fast pytest tests. Save the browser/`curl`
> behavioral check for the live-server behavior.
