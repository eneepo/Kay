# Spec format (Kay)

Kay specs are plain Markdown. There are two shapes: **canonical specs** (the living
truth in `.kay/specs/`) and **delta specs** (one change's proposed edits, in
`.kay/changes/<id>/specs/`).

## Capabilities

A **capability** is one coherent area of behavior (e.g. `auth`, `search`,
`todo-list`). Canonical specs live one folder per capability:
`.kay/specs/<capability>/spec.md`.

## EARS requirements

Every requirement is written in **EARS** — *Easy Approach to Requirements Syntax*,
fill-in-the-blank forms that are hard to write vaguely. Use one of these five:

| Form | Template | Example |
|---|---|---|
| Ubiquitous | `THE SYSTEM SHALL …` | THE SYSTEM SHALL store tasks in a local file. |
| Event | `WHEN … THE SYSTEM SHALL …` | WHEN the user adds a task THE SYSTEM SHALL append it to the list. |
| State | `WHILE … THE SYSTEM SHALL …` | WHILE the list is empty THE SYSTEM SHALL show a placeholder. |
| Conditional | `IF … THEN THE SYSTEM SHALL …` | IF the task text is empty THEN THE SYSTEM SHALL reject it. |
| Optional | `WHERE … THE SYSTEM SHALL …` | WHERE a due date is given THE SYSTEM SHALL sort by it. |

A requirement must be **testable**: a reader can tell pass from fail. "THE SYSTEM
SHALL be fast" is not testable; "THE SYSTEM SHALL respond within 200ms" is.

## Scenarios (GIVEN / WHEN / THEN)

Every requirement carries **at least one scenario** — a concrete example that
`/k-verify` will actually run:

```
GIVEN an empty task list
WHEN the user adds "buy milk"
THEN the list shows one task, "buy milk"
```

## Canonical spec layout

```
# Capability: <name>

## Requirement: <short title>
<the EARS statement>

### Scenario: <name>
GIVEN <starting state>
WHEN <action>
THEN <observable result>
```

## Delta spec layout

A change never edits canonical specs directly — it writes a **delta** that
`/k-review` folds in later. Group edits under three headings:

```
# Delta: <capability>

## ADDED
### Requirement: <title>
<EARS statement>
### Scenario: <name>
GIVEN … / WHEN … / THEN …

## MODIFIED
### Requirement: <title matching an existing canonical requirement>
<the new EARS statement + scenario>

## REMOVED
### Requirement: <title of the canonical requirement to delete>
```

Only include the headings you use. A brand-new capability has only an `## ADDED`
section.
