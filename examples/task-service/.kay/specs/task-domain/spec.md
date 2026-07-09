# Capability: task-domain

The task operations, independent of storage and transport. A task is
`{"id": int, "title": str, "done": bool}`.

## Requirement: Add a task
WHEN `add` is called with a non-empty title THE SYSTEM SHALL append a task with the
next unused id and `done` = false, and return it.

### Scenario: incrementing ids
GIVEN an empty list
WHEN I add "one" then "two"
THEN their ids are 1 and 2

## Requirement: Reject an empty title
IF the title is empty or only whitespace THEN THE SYSTEM SHALL raise `TaskError` and
add nothing.

### Scenario: whitespace title
GIVEN an empty list
WHEN I call `add(tasks, "   ")`
THEN it raises `TaskError` and the list stays empty

## Requirement: Complete a task
WHEN `complete` is called with an existing id THE SYSTEM SHALL set that task's `done`
to true.

### Scenario: mark done
GIVEN a list with task #1 not done
WHEN I call `complete(tasks, 1)`
THEN task #1 has `done` = true

## Requirement: Delete a task
WHEN `delete` is called with an existing id THE SYSTEM SHALL remove that task.

### Scenario: remove
GIVEN a list with task #1
WHEN I call `delete(tasks, 1)`
THEN the list no longer contains task #1

## Requirement: Unknown id is an error
IF an operation names an id that is not present THEN THE SYSTEM SHALL raise
`TaskError`.

### Scenario: complete a missing task
GIVEN an empty list
WHEN I call `complete(tasks, 99)`
THEN it raises `TaskError`

## Requirement: Filter the list by status
WHERE a status filter of "todo" or "done" is given THE SYSTEM SHALL return only the
tasks matching it; with no filter it returns all tasks.

### Scenario: todo filter
GIVEN tasks #1 (not done) and #2 (done)
WHEN I call `list_tasks(tasks, "todo")`
THEN it returns only task #1
