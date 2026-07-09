# SDD without a framework — just prompts

Kay automates spec-driven development. But you don't *need* Kay (or any framework) to
practice it — SDD is a **discipline**, and you can run it with nothing but well-shaped
prompts to any AI coding assistant (Copilot, Claude, whatever).

This file shows how. The prompts are in **code blocks** — paste each one straight into
your assistant, swap in your own idea, and you're doing SDD by hand. Once you feel the
rhythm, Kay's `/k-*` skills are just this loop with the bookkeeping, gates, and file
layout handled for you.

> **The whole idea in one line:** write down *what* and *how-you'll-know* **before** you
> write code, then hold the code to it.

We'll build one tiny feature end to end: **a command-line word counter that can ignore
blank lines**. Keep a folder open and let the assistant create files as we go.

> **One filename rule:** the feature's spec always lives in a file called **`SPEC.md`**.
> Every prompt below creates or reads that same file — same name every time — so the
> spec never goes missing between steps.

---

## Move 0 — set the ground rules (do this once, first)

A framework like Kay starts every project with `/k-init`, which writes the files the
assistant reads on **every** later step: a **constitution** (the principles and stack it
must obey) and a **spec-format** reference (how requirements and scenarios are written).
By hand you create these once yourself and **keep them in context** so the assistant
actually follows them.

### 0a. The constitution — your project's house rules

```text
Write me a short constitution and save it as a file named constitution.md, for a
small Python CLI project. Include:
(1) two non-negotiable principles — "quality over speed" (flag anything that trades
    correctness or maintainability for speed, and recommend the sounder path) and
    "plain language" (gloss jargon on first use with a quick example);
(2) a gate policy of "warn + explicit override" — surface issues and wait, never
    silently pass; only the human overrides;
(3) a Stack section naming the language (Python 3), the test runner (pytest), and the
    base branch (main).
Keep it under a page.
```

**What to do with it:**

- Keep `constitution.md` in your project root.
- **Reread it into context at the start of every SDD prompt** — the assistant only obeys
  rules it can see. Either paste the file, or open your prompts with *"Following the
  rules in `constitution.md`, …"*. (This is exactly what Kay automates: every `/k-*`
  skill loads the constitution first.)
- It's **yours** — edit it by hand as your principles or stack change; the assistant
  should never rewrite it without you asking.

### 0b. The spec conventions — so every spec looks the same

You want every requirement written the same testable way, session after session.

```text
Give me a one-page cheat sheet and save it as a file named spec-format.md. Cover the
five EARS requirement forms — Ubiquitous (THE SYSTEM SHALL …), Event (WHEN … THE
SYSTEM SHALL …), State (WHILE … THE SYSTEM SHALL …), Conditional (IF … THEN THE SYSTEM
SHALL …), and Optional (WHERE … THE SYSTEM SHALL …) — with one example each, plus the
GIVEN / WHEN / THEN scenario shape. Note that every requirement must be testable: a
reader can tell pass from fail.
```

**What to do with it:**

- Reference `spec-format.md` in your Move 1 prompt (*"using the EARS forms in
  `spec-format.md`"*).
- This keeps specs consistent across features — the same reason Kay seeds it once at
  init. (Kay ships a ready-made version; you can copy
  [`.github/skills/k-init/templates/spec-format.md`](.github/skills/k-init/templates/spec-format.md)
  instead of generating your own.)

### Where things live (by hand)

No framework, no special folders — just three plain files:

```
constitution.md   # house rules             (Move 0a) — reused every session
spec-format.md    # requirement conventions (Move 0b) — reused every session
SPEC.md           # the current feature's spec (Move 1) — one per feature
```

Kay's `.kay/` folder is just a tidier, automated home for these same files.

---

## The five moves

With the ground rules from Move 0 in context, SDD is five moves. Each is one prompt. Do
them in order; don't skip ahead. Open each prompt with *"Following `constitution.md` and
`spec-format.md`, …"* so the assistant keeps obeying them.

### 1. Spec — say what you want, testably

Don't ask for code yet. Ask for a spec. The trick is to demand **EARS requirements**
(fill-in-the-blank forms that are hard to write vaguely) and **GIVEN/WHEN/THEN
scenarios** (concrete examples you can later check).

```text
I want a small CLI called wc-lite that counts words in a text file. Write me a short
spec first — NO code yet — and save it as a file named SPEC.md. Use the EARS forms
from spec-format.md and give at least one GIVEN/WHEN/THEN scenario per requirement.
Requirements must be testable — a reader can tell pass from fail. Include a
requirement for an optional --ignore-blank flag that skips blank lines. Keep it to
3–4 requirements.
```

You should get a `SPEC.md` like:

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

**Why first:** a spec is cheap to change and a code rewrite isn't. If the scenarios look
wrong, you caught it before writing a line.

### 2. Analyze — check the spec against itself, then fix it

Before building, make the assistant *critique its own spec*. This catches gaps a
framework would catch with a coverage matrix.

```text
Review SPEC.md for problems before I build it. Is every requirement testable? Is any
requirement vague (e.g. "be fast")? Are there missing edge cases — empty file, file
not found, a word with punctuation? List the issues with a recommended fix for each.
Don't write code and don't edit the file yet.
```

Then, once you've read the issues, have it **apply the fixes back to the spec** — a
separate prompt, so you approve the rewrite instead of letting the critique and the edit
blur together:

```text
Apply the fixes we agreed on directly to SPEC.md and show me the updated file. Only
change SPEC.md — no code yet. Keep every requirement in an EARS form with at least one
GIVEN/WHEN/THEN scenario.
```

Now `SPEC.md` is something you'd be happy to hold code to.

### 3. Build — implement to the spec, test-first

Now, and only now, ask for code — and pin it to the spec.

```text
Implement SPEC.md in Python. Work test-first: for each scenario, write a pytest test,
run it and show me it fails, then write the smallest code that makes it pass. Don't
add anything SPEC.md doesn't call for. If you find the spec is wrong or incomplete
while building, stop and tell me — we'll fix SPEC.md, not silently diverge.
```

That last sentence is the **living-spec** rule: the spec and the code must stay in sync,
so a surprise updates the spec rather than getting buried in code.

### 4. Verify — run the scenarios for real

Reading code proves nothing. Run the behavior.

```text
Go scenario by scenario through SPEC.md. For each one: set up the GIVEN (create the
fixture file), perform the WHEN (actually run wc-lite), and show me the real output
next to the THEN. Mark each PASS or FAIL with the evidence. If one fails, fix the
code, then re-run ALL the scenarios in case the fix broke another.
```

You now have proof, not vibes — a PASS/FAIL line and real output per scenario.

### 5. Review — quality gate, then make it truth

The last look before you call it done.

```text
Review the finished wc-lite against SPEC.md. Check: does the code do what each
requirement says? Any hardcoded paths, unhandled errors, or dead code? Any security
issue (bad file handling)? Was anything built that SPEC.md doesn't mention? List
findings by severity (blocker / should-fix / nit) with fixes. Then, once it's clean,
update SPEC.md so it describes the final behavior exactly — no stale bits.
```

When it's clean, `SPEC.md` *is* your living documentation of what `wc-lite` does.

---

## What you just did

You ran the exact loop Kay runs:

| By hand (this file) | With Kay |
|---|---|
| "Write me a constitution + spec conventions, then keep them in context" | `/k-init` |
| "Write me a spec, EARS + scenarios, no code" | `/k-spec` |
| "Critique the spec, then apply the fixes back to it" | `/k-analyze` |
| "Implement it, test-first, tell me if the spec is wrong" | `/k-build` |
| "Run every scenario for real, PASS/FAIL with evidence" | `/k-verify` |
| "Review by severity, then update the spec to match" | `/k-review` |

The discipline is the same. What Kay adds is the **plumbing**: a consistent file layout
under `.kay/`, a branch per change, a coverage matrix instead of a freeform critique,
gates that won't let a failing scenario slip through silently, and an archived audit
trail. You stop *remembering* to run the five moves — the tool makes them the path of
least resistance.

Next: we introduce Kay and run this same loop on a real starter in
[`examples/`](examples).
