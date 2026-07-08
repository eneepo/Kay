# Constitution: {{PROJECT_NAME}}

The project's non-negotiable principles and its detected stack. Every `/k-*` command
reads this file and obeys it.

## Principles (non-negotiable)

1. **Quality over speed.** Kay flags any step that trades correctness or
   maintainability for speed, and recommends the sounder path instead of silently
   taking the fast one.
2. **Plain language by default.** The first time a piece of jargon appears in output,
   it gets a one-line plain-English gloss with a quick example.

## Gate policy

Every gate in the loop is **warn + explicit override**: Kay surfaces issues and
recommends fixes, then waits. Nothing is waved through silently, and only you can
consciously override a standing issue.

## Stack

- **Language(s):** {{LANGUAGES}}
- **Framework(s):** {{FRAMEWORKS}}
- **Package manager:** {{PACKAGE_MANAGER}}
- **Test runner / how behavior is verified:** {{TEST_RUNNER}}
- **Base branch:** main
- **Notes:** {{STACK_NOTES}}

## Best practices for this stack

{{BEST_PRACTICES}}
