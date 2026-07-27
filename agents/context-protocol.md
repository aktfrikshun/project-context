<!-- Purpose: Specifies a predictable retrieval and evidence protocol for assistants and future MCP clients. -->
---
title: AI context protocol
status: active
owners: [maintainers]
last_reviewed: 2026-07-27
tags: [ai, retrieval, protocol, mcp]
---

# AI context protocol

## Inputs

An assistant should establish the project ID, task, affected domain, and requested action. If the project is unknown, search `projects/README.md`; do not select one from name similarity without disclosing the inference.

## Retrieval

1. Load the project overview.
2. Expand only relevant project documents and linked shared standards.
3. Retrieve accepted ADRs by scope, tags, links, and keywords.
4. Retrieve glossary definitions for ambiguous domain language.
5. Use `history/` only to explain evolution, never as current authority.

Prefer direct path and heading matches before semantic similarity. Preserve status, scope, date, and source path with every retrieved chunk.

## Synthesis

Resolve scope using [repository architecture](../architecture.md). Quote sparingly; summarize faithfully. If sources conflict, report both and request or propose resolution. If no source supports a claim, label it as an inference or recommendation.

## Mutation

AI-generated changes should be reviewable Git diffs. New decisions start as `proposed`. Assistants may draft rules, but an accountable human must verify the source and activate them. Accepted ADRs are superseded, not substantively edited.

## Suggested MCP behavior

- Read tools return Markdown plus path, heading, revision, status, and scope.
- Search ranks authoritative and project-scoped sources above patterns and history.
- `load_project_context` follows explicit links and reports omissions rather than loading the entire repository blindly.
- `record_decision` validates the next ADR ID, creates a proposed record, and updates the index in one atomic change.
- Write tools never bypass normal review or store conversation history as authority.

## Response evidence

For material project claims, return the source path and heading. State which required documents were unavailable or stale. Recommendations should explain which constraints informed them and which decision would need an ADR.
