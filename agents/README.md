<!-- Purpose: Defines vendor-neutral operating rules for any AI assistant using this knowledge. -->
# AI assistant guidelines

These instructions apply to ChatGPT, Codex, Claude Code, Cursor, VS Code assistants, Gemini, and other tools. Tool-specific adapter files may point here, but must not replace or contradict this authority.

## Required reading order

1. Read `projects/<project-id>/overview.md`.
2. Follow its links to applicable shared standards.
3. Read project architecture, business rules, workflows, integrations, conventions, and glossary relevant to the task.
4. Read governing accepted ADRs.
5. Use patterns and history only as supporting context.

## Behavior contract

- Prefer documented facts and accepted decisions over assumptions.
- Never invent a business rule, integration contract, owner, deadline, or security requirement.
- Distinguish `Documented fact`, `Inference`, `Recommendation`, and `Open question` in answers when ambiguity matters.
- Cite repository paths and headings for project-specific claims.
- Surface conflicts, missing context, and stale review dates.
- Treat `draft` and `proposed` content as non-authoritative.
- Respect scope: shared standards are defaults; project exceptions and accepted ADRs can govern more narrowly.
- Keep proposed documentation concise, evergreen, and free of chat-specific framing.
- Do not copy secrets, personal data, source code, or confidential transient context into this repository.

## Updating knowledge

When durable knowledge emerges, propose the smallest canonical update. Use an ADR for consequential choices. Do not silently rewrite accepted decisions, erase contradictions, or turn a recommendation into a fact. Human review remains required for business, security, legal, and architectural authority.

See [context protocol](context-protocol.md) for retrieval and response mechanics.
