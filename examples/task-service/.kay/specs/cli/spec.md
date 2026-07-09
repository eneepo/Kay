# Capability: cli

An argparse front-end over the task domain. Subcommands map to domain operations and
persist through `storage`. Invoked as `python -m taskservice.cli`.

## Requirement: Subcommands drive the domain and persist
WHEN the user runs `add`, `list`, `done`, or `rm` THE SYSTEM SHALL apply the matching
domain operation against the `--file` store (default `tasks.json`) and save the
result.

### Scenario: add then list
GIVEN an empty store
WHEN I run `add "buy milk"` then `list`
THEN the output shows one task, `[ ] #1 buy milk`

### Scenario: done marks a task complete
GIVEN a store with task #1
WHEN I run `done 1` then `list`
THEN task #1 is shown as `[x] #1 …`

## Requirement: Errors exit non-zero
IF a domain or storage error occurs THEN THE SYSTEM SHALL print a clear `error:`
message to standard error and exit with a non-zero status — never a traceback.

### Scenario: empty title
GIVEN an empty store
WHEN I run `add "   "`
THEN it prints an error to stderr and exits with status 2
