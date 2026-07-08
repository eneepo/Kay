# Lab: quote-cli (Python + pytest)

A tiny Python CLI that prints a random quote. Use it to run the **Kay loop** on a
project that **has a test runner** — so you experience the **test-first build** path.

## Run it

```bash
cd examples/quote-cli
python quote.py            # prints a random quote
pytest                     # runs the starter tests
```

(Only the Python standard library and `pytest` are needed.)

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

Because there's a test runner, watch `/k-build` write a failing test first, then make
it pass — and watch `/k-verify` run your scenarios for real.

### Suggested features (pick one)

- **`--count N`** — print N random quotes instead of one.
- **`--author "<name>"`** — only print quotes by a given author (and a friendly
  message if none match).
- **`--list`** — print every quote, numbered, and exit.
- **`--seed N`** — make the choice reproducible for a given seed.

Each is small enough to spec in a few EARS requirements, and each has clear
GIVEN/WHEN/THEN scenarios to verify.

> Tip: keep scope tight. One flag, two or three requirements, one or two scenarios
> each. The point is to feel the loop, not to build a big CLI.
