# Kay usage guide

This guide walks you through Kay's loop with GitHub Copilot. For what Kay *is*, start
with [`README.md`](README.md); to see the same discipline done by hand with no
framework, read [`PROMPTS.md`](PROMPTS.md).

> **Spec-driven development (SDD)** — instead of typing a prompt and hoping, you write
> a short structured spec first (what you want, how it should behave, the steps). Kay
> builds to that spec, checks the result against it, and keeps the spec true to the
> code afterwards.

## How to invoke a skill

In the **Copilot CLI** or **Copilot in VS Code**, type the skill name with a slash
and pass your input after it:

```
/k-spec "add a clear-completed button to the task list"
```

Copilot also loads a skill automatically when your request matches its description, so
"set up Kay here" will pull in `/k-init`. Run `/skills list` in the CLI to see the
skills Copilot found, and `/skills reload` after editing one.

## The core loop, step by step

You have one concrete thing to do — a feature, a fix, a refactor — and you want it
specced, built, checked, and merged without drift.

### 0. `/k-init` — once per project

Run it in the project root. Kay detects your stack (language, framework, test
runner), creates the `.kay/` folder, and seeds the **constitution** — the project's
non-negotiable principles that every later skill reads and obeys — plus the
spec-format and glossary references. Everything lands in your repo, so specs travel
with the code. Re-running is safe: it refreshes references and never clobbers your
decisions.

### 1. `/k-spec "<your idea>"`

Kay asks clarifying questions **one at a time**, recaps what it heard, and — only
after your **explicit go-ahead** — writes the change's artifacts on a branch
`kay/<change-id>`:

- a **proposal** (why, what, scope, non-goals, success criteria),
- **EARS requirements** — fill-in-the-blank testable requirements like "WHEN a user
  submits an empty task THE SYSTEM SHALL reject it",
- **scenarios** — GIVEN/WHEN/THEN examples of each requirement in action,
- a **design**, and an ordered **task list** where every task cites the requirement it
  satisfies.

Answering the questions is not the same as approving — Kay waits for a clear "go
ahead" before it creates anything.

### 2. `/k-analyze <change-id>`

A read-only **consistency gate**: it builds a coverage matrix mapping each requirement
to the tasks that implement it, and flags gaps — a requirement with no task, a task
that traces to nothing (possible scope creep), a vague requirement, a mismatch with
the canonical specs. It writes only its `analysis.md` report. Fix what it flags before
building.

### 3. `/k-build <change-id>`

Implements the tasks on the change branch. Where a **test runner** exists, Kay works
test-first — write the test, watch it fail (red), implement, watch it pass (green) —
before checking each task off. Where there's no test runner, it implements directly
and leans on `/k-verify`. If reality forces the spec to change, the spec is updated to
match — specs never rot into fiction.

### 4. `/k-verify <change-id>`

Runs each **scenario** from the spec against the real build — actually performing the
WHEN and observing the result, not just reading code — and records PASS/FAIL with
evidence. A failing scenario enters a bounded fix-and-re-run loop (default 3 attempts)
before it reaches the gate.

### 5. `/k-review <change-id>`

The last **quality gate**. Kay reviews the diff in ordered passes (security → core →
QA), gating after each. On a pass it **folds** the change's delta into `.kay/specs/` —
the canonical, current description of how your system behaves — archives the change
with its full audit trail, and merges the branch into `main`.

Every gate follows the same policy: **warn + explicit override** — Kay surfaces issues
and recommends fixes, and only you consciously wave one through.

**You end up with:** the change merged, its spec folded into `.kay/specs/` as living
truth, and the change folder archived with its analysis, verification, and review
reports.

## A worked example

```
/k-init
/k-spec "let users clear all completed tasks at once"
# answer the clarifying questions, then approve the recap
/k-analyze clear-completed
/k-build clear-completed
/k-verify clear-completed
/k-review clear-completed
```

Try it for real against one of the starters in [`examples/`](examples).

## Hands-off — autopilot

Once a change is **specced** (you've run `/k-spec` and approved it), you don't have to
drive the remaining four steps by hand. **`/k-autopilot <change-id>`** flies the change
through `analyze → build → verify → review` unattended, in the current session.

At each gate it reads the verdict instead of asking you: a **clean** gate (and
nit-level findings) proceeds automatically; anything that needs a human — an analysis
issue, a scenario still failing after its retry budget, a review blocker — **halts the
run** with a plain-language report of what stopped it and how to resume. Fix the cause
(or resolve that one gate by running its command directly), then re-run
`/k-autopilot <change-id>` and it picks up from the halted phase.

Invoking it is your **standing consent** for the whole run — no mid-run prompts. It
ends at a change that's **reviewed, folded into `.kay/specs/`, and archived, ready to
merge** — autopilot **never merges**; that last step stays yours (via `/k-review`'s
merge step or your PR flow). If you'd rather approve each gate, just run the five
commands individually instead.

## After a session — the retrospective

Run **`/k-retro`** at the end of a working session, *before* you close the terminal —
while the conversation is still in context, which is its richest evidence. It writes a
private note under `.kay/.local/retros/<date>.md` (gitignored, so no committed
footprint) with six sections: summary, timeline, sideways & loops, communication, Kay
improvements, and wins.

Then it **triages** the improvement ideas and shows you a table before writing
anything durable. Only after you approve does it route them: communication
preferences to memory, quick fixes to `ROADMAP.md`, and bigger ideas to
`.kay/.local/retro-queue.md` as ready-to-run `/k-spec` prompts for next time. Nothing
shared is touched without your go-ahead, and it never auto-runs `/k-spec`.

## Tips

- **One change at a time.** Keep changes small — one feature or fix per `kay/<id>`
  branch. Small changes are easier to spec, verify, and review.
- **Trust the gates.** If `/k-analyze` flags an uncovered requirement, it's usually
  right — add the task rather than override.
- **Read the artifacts.** Everything Kay writes is plain Markdown under `.kay/`. Open
  the files; the spec is meant to be read by humans, not just tools.
