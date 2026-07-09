# Capability: api

A standard-library HTTP JSON front-end over the task domain. Routing lives in the
pure `dispatch(method, path, body, file)` function; the HTTP handler is a thin
adapter. Run as `python -m taskservice.api`.

## Requirement: List tasks
WHEN a `GET /tasks` request arrives THE SYSTEM SHALL respond 200 with the task list
as JSON, filtered by an optional `?status=todo|done` query.

### Scenario: empty list
GIVEN an empty store
WHEN a client sends `GET /tasks`
THEN the response is 200 with body `[]`

## Requirement: Create a task
WHEN a `POST /tasks` request arrives with a non-empty `title` THE SYSTEM SHALL create
the task, persist it, and respond 201 with the created task.

### Scenario: create
GIVEN an empty store
WHEN a client POSTs `{"title": "buy milk"}` to `/tasks`
THEN the response is 201 with the task `{"id": 1, "title": "buy milk", "done": false}`

## Requirement: Reject an invalid create
IF a `POST /tasks` body has an empty or missing title THEN THE SYSTEM SHALL respond
400 with an error message and create nothing.

### Scenario: empty title
GIVEN an empty store
WHEN a client POSTs `{"title": ""}` to `/tasks`
THEN the response is 400 with an `error` field

## Requirement: Delete a task
WHEN a `DELETE /tasks/{id}` request names an existing task THE SYSTEM SHALL remove it
and respond 200; IF the id is unknown THEN it responds 404.

### Scenario: delete unknown
GIVEN an empty store
WHEN a client sends `DELETE /tasks/99`
THEN the response is 404
