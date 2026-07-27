<!-- Purpose: Entry point for humans, AI assistants, and future knowledge services. -->
# Project Context

Project Context is a vendor-neutral, documentation-only knowledge repository that sits beside software repositories. It is the authoritative source for durable project knowledge: architecture, business rules, terminology, standards, workflows, integrations, patterns, and significant decisions.

Chats are useful working spaces, but poor systems of record. They are private to a tool, difficult to review, easy to lose, and rarely versioned with intent. Knowledge that should survive a session belongs here, where people can review it, AI assistants can retrieve it, and Git can preserve why it changed.

## Principles

- Markdown is the canonical format.
- Humans remain responsible for correctness and approval.
- Documents are concise, linked, searchable, and evergreen.
- Facts, decisions, constraints, proposals, and examples are labeled distinctly.
- Shared guidance applies broadly; project guidance captures justified differences.
- Stable paths and predictable headings are part of the public interface.
- The repository describes software and its operating context; it does not contain application source code, secrets, credentials, generated logs, or private customer data.

## Start here

1. Read [AI assistant guidance](agents/README.md).
2. Select a project under `projects/` and read its `overview.md`.
3. Load the relevant material under `shared/`.
4. Read the project's architecture, business rules, workflows, integrations, and conventions.
5. Check applicable records in `decisions/` before proposing a conflicting direction.

The `_template` project is a copyable scaffold, not a real project.

## Knowledge model

| Location | Scope | Examples |
| --- | --- | --- |
| `shared/` | Defaults reused by multiple projects | coding, security, testing, deployment, UI, technology guidance |
| `projects/<project-id>/` | Facts and exceptions for one project | purpose, boundaries, architecture, rules, workflows, integrations |
| `decisions/` | Immutable decision history | accepted, superseded, or rejected ADRs |
| `patterns/` | Reusable solutions with trade-offs | idempotency, event handling, API evolution |
| `templates/` | Authoring contracts | ADR, project, rule, glossary, workflow, integration templates |
| `agents/` | Tool-neutral consumption rules | reading order, evidence and update behavior |
| `history/` | Curated milestones and migrations | context that explains the present but is not current guidance |

Shared knowledge is the default. Project-specific knowledge narrows, extends, or explicitly overrides it. When guidance conflicts, a documented project exception or accepted ADR wins; otherwise raise the conflict instead of guessing.

## Updating the repository

Use a normal reviewable Git change:

1. Find the narrowest authoritative document; avoid duplicating the same fact.
2. State evidence, scope, owner, and review date where they matter.
3. Link related documents with relative links.
4. Use an ADR for a significant choice with alternatives and consequences.
5. Update indexes and mark superseded content; do not silently rewrite history.
6. Submit the change for review by the people responsible for the subject.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the authoring and review contract.

## Guidance for AI assistants

AI assistants should treat this repository as retrieved evidence, not as an infallible prompt. Always read the project overview first, load relevant shared standards, prefer accepted decisions over assumptions, and cite file paths when giving project-specific answers. Never invent missing business rules. Clearly label recommendations and unresolved questions, and propose documentation updates when durable knowledge emerges.

Detailed behavior is defined in [agents/README.md](agents/README.md) and [agents/context-protocol.md](agents/context-protocol.md).

## Future MCP compatibility

The layout intentionally maps to resource-oriented tools without requiring a database:

| Future tool | Natural source |
| --- | --- |
| `load_project_context(project)` | `projects/<project-id>/` plus referenced shared documents and ADRs |
| `search_knowledge(query)` | all Markdown content and front matter |
| `list_decisions()` | `decisions/adr-*.md` |
| `get_business_rules()` | `projects/<project-id>/business-rules.md` |
| `get_glossary()` | shared and project glossary documents |
| `get_architecture()` | `projects/<project-id>/architecture.md` |
| `record_decision()` | a new file created from `templates/adr-template.md` |

Stable identifiers, one topic per section, relative links, and lightweight YAML front matter make the same content usable through GitHub today and semantic retrieval later. See [architecture.md](architecture.md).

## Creating a project context

Copy `projects/_template/` to `projects/<project-id>/`, replace placeholders, and add the project to `projects/README.md`. Do not delete unused sections; mark them `Not applicable` with a reason so absence is unambiguous.

## Status

This repository defines a portable convention, not a dependency on any editor, model vendor, embedding provider, or MCP implementation. Changes should preserve plain-Markdown usefulness first.
