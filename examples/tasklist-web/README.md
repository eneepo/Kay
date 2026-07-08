# Lab: tasklist-web (plain HTML + JS)

A tiny task list with **no build step and no dependencies**. Use it to run the **Kay
loop** on a project that has **no test runner** — so you experience **behavioral
verification**: `/k-verify` drives the page and observes what actually happens.

## Run it

Open `examples/tasklist-web/index.html` in a browser (double-click it, or serve the
folder with `python -m http.server` and visit the printed URL). You can add tasks and
tick them complete.

## Your lab exercise

Set Kay up here, then spec and ship **one** new feature through the full loop:

```
/k-init
/k-spec "<your feature>"
/k-analyze <change-id>
/k-build   <change-id>
/k-verify  <change-id>
/k-review  <change-id>
```

Because there's no test runner, `/k-build` implements directly and `/k-verify`
verifies **behaviorally** — it sets up each GIVEN, performs the WHEN in the page, and
checks the THEN against what really renders. Write your scenarios so they're checkable
by looking at the page.

### Suggested features (pick one)

- **Clear completed** — a button that removes all ticked tasks at once.
- **Task count** — show "N tasks, M done" and keep it updated.
- **Persist** — remember tasks across reloads with `localStorage`.
- **Delete a task** — an × button on each row.

Each is small enough to spec in a few EARS requirements with concrete
GIVEN/WHEN/THEN scenarios.

> Tip: a good web scenario names what you'd *see* — e.g. "GIVEN two tasks, one ticked,
> WHEN I click Clear completed, THEN only the un-ticked task remains and the count
> reads '1 task, 0 done'."
