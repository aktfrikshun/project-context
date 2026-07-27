<!-- Purpose: Defines shared expectations for maintainable source repositories. -->
# Coding standards

These standards describe outcomes that project repositories should enforce with their native tooling.

## Baseline

- Optimize for clarity, correctness, and reversibility.
- Use names from the domain glossary and avoid unexplained abbreviations.
- Keep modules cohesive and dependencies explicit.
- Validate inputs at trust boundaries and handle failures deliberately.
- Do not commit secrets or sensitive production data.
- Prefer automated formatting, linting, type checking, and tests.
- Document public contracts and non-obvious constraints, not line-by-line mechanics.
- Make observability useful without exposing protected data.
- Treat dependency additions as architecture and supply-chain decisions.

Projects must document language-specific rules, commands, generated-code policy, and justified exceptions in `projects/<project-id>/conventions.md`.

Copy [the coding standards template](../../templates/coding-standards-template.md) when defining a more specific standard.
