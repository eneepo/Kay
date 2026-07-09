# Kay

Kay is a small **spec-driven development (SDD)** framework you drive through `/k-*`
skills in **GitHub Copilot** — the Copilot CLI and Copilot in VS Code.

> **Spec-driven development, in plain words:** instead of typing a prompt and hoping
> for the best, you write a short structured spec first — *what* you want, *how* it
> should behave, and the *steps* to get there. Kay builds to that spec, checks the
> result against it, and only then folds the spec into the project's source of truth.
> The spec stays true to the code over time, so it never rots into fiction.

Kay is a teaching-sized port of [Zeeg](../Zeeg): the same core loop, stripped to the
essentials for a presentation and a hands-on lab.

> **Looking for how to use it?** [`GUIDE.md`](GUIDE.md) walks you through the loop
> step by step. New to SDD? [`PROMPTS.md`](PROMPTS.md) shows how to do spec-driven
> development *by hand*, with no framework at all — the idea Kay automates.

## The loop

| Skill | What it does |
|---|---|
| `/k-init` | Set Kay up in a project: detect the stack, create the `.kay/` folder, seed the constitution and references |
| `/k-spec` | Turn an idea into a change — a proposal, EARS requirements, a design, and an ordered task list |
| `/k-analyze` | Consistency gate: check the proposal, specs, design, and tasks all agree, before any code is written |
| `/k-build` | Implement it to spec on the change branch — test-first where a test runner exists |
| `/k-verify` | Run the spec's own GIVEN/WHEN/THEN scenarios against the real build and record pass/fail |
| `/k-review` | Quality gate, then fold the spec into the source of truth, archive the change, and merge |

A change flows `spec → analyze → build → verify → review`. Specs are **living**: when
the build forces a divergence, the spec is updated to match reality, never left to
drift.

**Companion skill:**

| Skill | What it does |
|---|---|
| `/k-retro` | End-of-session retrospective — a private note (what happened, what went sideways, what to change), then approval-gated routing of the durable signals |

## A note on the `k:` names

In Claude Code, Zeeg's skills are namespaced as `/z:spec`, `/z:build`, and so on.
GitHub Copilot skill names **can't contain colons**, so the `k:` family is invoked
with a hyphen: `/k-spec`, `/k-build`, `/k-verify`, etc. Same idea, Copilot-native
spelling.

## Principles (built into every skill)

- **Quality over speed.** Kay flags any step that trades correctness or
  maintainability for speed, and recommends the sounder path.
- **Plain language by default.** The first time a piece of jargon appears in output,
  it gets a one-line plain-English gloss with a quick example.

## Where things live

- **The tool** — skills in `.github/skills/k-*/SKILL.md`. Copilot discovers them
  automatically; run `/skills list` in the Copilot CLI to confirm.
- **The artifacts** — when you run `/k-init`, Kay creates a `.kay/` folder **in your
  project repo** (committed alongside the code, so specs travel with the branch they
  describe):

  ```
  .kay/
    constitution.md        # principles + detected stack
    reference/             # spec-format.md, glossary.md
    specs/<capability>/     # canonical living specs
    changes/<id>/           # one in-flight change's artifacts
    changes/archive/<id>/   # completed changes (full audit trail)
  ```

## Install (local development)

Kay's skills are **project skills** — they live in this repo under `.github/skills/`,
so Copilot picks them up automatically when you work here. To use Kay in another
project, copy the `.github/skills/k-*` folders into that repo (or into
`~/.copilot/skills/` to make them personal skills available everywhere), then:

```
# in the project you want to manage
/k-init
```

## Try it — the hands-on lab

Three starter projects in [`examples/`](examples) let you run the whole loop on
something real, each exercising a different aspect of SDD:

- [`examples/quote-cli`](examples/quote-cli) — a Python CLI **with a test runner**
  (pytest), so you see the test-first build path.
- [`examples/tasklist-web`](examples/tasklist-web) — a plain HTML/JS page with **no
  test runner**, so you see behavioral verification.
- [`examples/task-service`](examples/task-service) — a **multi-capability** task
  manager (CLI + REST API over a shared core) that ships **already initialized** with
  living specs, so you see multi-capability changes, **MODIFIED** deltas, and both
  verification styles at once.

Each has a README with suggested features to spec. See [`GUIDE.md`](GUIDE.md) for the
walkthrough.

## License

MIT.
