<!-- Purpose: Records the foundational format and portability decision for this repository. -->
---
title: Use Markdown and Git as the canonical knowledge layer
status: accepted
date: 2026-07-27
decision_id: ADR-0001
owners: [maintainers]
tags: [architecture, portability]
---

# ADR-0001: Use Markdown and Git as the canonical knowledge layer

## Context

Persistent project knowledge must be readable and maintainable across organizations, editors, AI assistants, and future retrieval systems without depending on a single vendor.

## Decision

Store canonical knowledge as Markdown in Git. Use stable directory conventions, relative links, and optional YAML front matter. Treat vendor indexes, embeddings, and MCP services as replaceable projections of these files.

## Alternatives considered

- **Vendor-hosted assistant memory:** convenient, but difficult to review, export, and share across tools.
- **Wiki as sole authority:** approachable, but portability, offline use, and change review vary by vendor.
- **Structured database:** queryable, but raises operating cost and makes direct human contribution harder.

## Consequences

- Knowledge is portable, diffable, reviewable, and useful without specialized software.
- Maintainers must curate structure, links, metadata, and stale content.
- Rich queries may require a derived index later.
- Plain Markdown remains the fallback whenever derived systems are unavailable.

## Follow-up

Define compatibility tests before introducing an MCP server or generated semantic index.
