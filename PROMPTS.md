# SDD without a framework — just prompts

Kay automates spec-driven development. But you don't *need* Kay (or any framework) to
practice it — SDD is a **discipline**, and you can run it with nothing but well-shaped
prompts to any AI coding assistant (Copilot, Claude, whatever).

This file shows how. Copy the prompts, swap in your own idea, and you're doing SDD by
hand. Once you feel the rhythm, Kay's `/k-*` skills are just this loop with the
bookkeeping, gates, and file layout handled for you.

> **The whole idea in one line:** write down *what* and *how-you'll-know* **before**
> you write code, then hold the code to it.

We'll build one tiny feature end to end: **a command-line word counter that can ignore
blank lines**. Keep a folder open and create files as we go.

---

## The five moves

SDD is five moves. Each is one prompt. Do them in order; don't skip ahead.

### 1. Spec — say what you want, testably

Don't ask for code yet. Ask for a spec. The trick is to demand **EARS requirements**
(fill-in-the-blank forms that are hard to write vaguely) and **GIVEN/WHEN/THEN
scenarios** (concrete examples you can later check).

> **Prompt:**
> "I want a small CLI called `wc-lite` that counts words in a text file. Write me a
> short spec first — no code yet. Use EARS requirements (WHEN… THE SYSTEM SHALL…, IF…
> THEN THE SYSTEM SHALL…, etc.) and give **at least one GIVEN/WHEN/THEN scenario per
> requirement**. Requirements must be testable — a reader can tell pass from fail.
> Include a requirement for an optional `--ignore-blank` flag that skips blank lines.
> Keep it to 3–4 requirements."

Save the result as `SPEC.md`. You should get something like:

```
## Requirement: Count words
WHEN wc-lite is run on a file THE SYSTEM SHALL print the number of
whitespace-separated words in that file.
### Scenario: two words
GIVEN a file containing "hello world"
WHEN I run `wc-lite file.txt`
THEN it prints "2"

## Requirement: Ignore blank lines
WHERE --ignore-blank is given THE SYSTEM SHALL not count words on blank lines.
### Scenario: blank line skipped
GIVEN a file with "hi\n\nthere"
WHEN I run `wc-lite --ignore-blank file.txt`
THEN it prints "2"
```

**Why first:** a spec is cheap to change and a code rewrite isn't. If the scenarios
look wrong, you caught it before writing a line.

### 2. Analyze — check the spec against itself

Before building, make the assistant *critique its own spec*. This catches gaps a
framework would catch with a coverage matrix.

> **Prompt:**
> "Review `SPEC.md` for problems before I build it. Is every requirement testable? Is
> any requirement vague (e.g. 'be fast')? Are there missing edge cases — empty file,
> file not found, a word with punctuation? List issues with recommended fixes. Don't
> write code."

Fold the fixes back into `SPEC.md`. Now the spec is something you'd be happy to hold
code to.

### 3. Build — implement to the spec, test-first

Now, and only now, ask for code — and pin it to the spec.

> **Prompt:**
> "Implement `SPEC.md` in Python. Work **test-first**: for each scenario, write a
> pytest test, run it and show me it fails, then write the smallest code that makes it
> pass. Don't add anything the spec doesn't call for. If you find the spec is wrong or
> incomplete while building, stop and tell me — we'll fix the spec, not silently
> diverge."

That last sentence is the **living-spec** rule: the spec and the code must stay in
sync, so a surprise updates the spec rather than getting buried in code.

### 4. Verify — run the scenarios for real

Reading code proves nothing. Run the behavior.

> **Prompt:**
> "Go scenario by scenario through `SPEC.md`. For each one: set up the GIVEN (create
> the fixture file), perform the WHEN (actually run `wc-lite`), and show me the real
> output next to the THEN. Mark each PASS or FAIL with the evidence. If one fails, fix
> the code, then re-run **all** the scenarios in case the fix broke another."

You now have proof, not vibes — a PASS/FAIL line and real output per scenario.

### 5. Review — quality gate, then make it truth

The last look before you call it done.

> **Prompt:**
> "Review the finished `wc-lite` against `SPEC.md`. Check: does the code do what each
> requirement says? Any hardcoded paths, unhandled errors, or dead code? Any security
> issue (bad file handling)? Was anything built that the spec doesn't mention? List
> findings by severity (blocker / should-fix / nit) with fixes. Then, once it's clean,
> update `SPEC.md` so it describes the final behavior exactly — no stale bits."

When it's clean, `SPEC.md` *is* your living documentation of what `wc-lite` does.

---

## What you just did

You ran the exact loop Kay runs:

| By hand (this file) | With Kay |
|---|---|
| "Write me a spec, EARS + scenarios, no code" | `/k-spec` |
| "Critique the spec, find gaps" | `/k-analyze` |
| "Implement it, test-first, tell me if the spec is wrong" | `/k-build` |
| "Run every scenario for real, PASS/FAIL with evidence" | `/k-verify` |
| "Review by severity, then update the spec to match" | `/k-review` |

The discipline is the same. What Kay adds is the **plumbing**: a consistent file
layout under `.kay/`, a branch per change, a coverage matrix instead of a freeform
critique, gates that won't let a failing scenario slip through silently, and an
archived audit trail. You stop *remembering* to run the five moves — the tool makes
them the path of least resistance.

Next: we introduce Kay and run this same loop on a real starter in
[`examples/`](examples).
