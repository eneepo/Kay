# Capability: storage

Load and save the task list as JSON. A missing file is an empty store; a corrupt
file is a loud error, never a silent wipe.

## Requirement: Missing file is an empty store
WHEN `load` is called on a path that does not exist THE SYSTEM SHALL return an empty
list.

### Scenario: no file yet
GIVEN a path with no file at it
WHEN I call `storage.load(path)`
THEN it returns `[]` and creates nothing

## Requirement: Persist and reload
THE SYSTEM SHALL save a task list so that a later `load` returns the same list.

### Scenario: round trip
GIVEN a task list `[{"id": 1, "title": "buy milk", "done": false}]`
WHEN I `storage.save(path, tasks)` then `storage.load(path)`
THEN the loaded list equals the saved list

## Requirement: Corrupt file is a clear error
IF the file exists but is not a JSON list THEN THE SYSTEM SHALL raise `StorageError`
rather than crashing or discarding data.

### Scenario: malformed JSON
GIVEN a file whose contents are `{not json`
WHEN I call `storage.load(path)`
THEN it raises `StorageError`
