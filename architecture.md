<!-- Purpose: Describes the repository's information architecture and future service boundary. -->
---
title: Repository architecture
status: active
owners: [maintainers]
last_reviewed: 2026-07-27
tags: [architecture, knowledge-model, mcp]
---

# Repository architecture

## Purpose and boundary

Project Context is a file-backed knowledge system. Git supplies identity, history, review, and distribution. Markdown supplies portability. Folders express scope. Links express relationships. Optional front matter supplies machine-readable metadata.

The repository contains descriptive knowledge, not application source code, runtime state, secrets, or telemetry.

## Layers

1. `shared/` contains organization- or ecosystem-wide defaults.
2. `projects/<project-id>/` contains a project's current truth and explicit exceptions.
3. `decisions/` contains append-oriented reasoning and consequences.
4. `patterns/` contains reusable, non-mandatory solutions.
5. `history/` contains non-authoritative historical context.
6. `templates/` and `agents/` define how knowledge is written and consumed.

## Resolution order

For a question about a project, resolve knowledge in this order:

1. Accepted ADR explicitly governing the topic.
2. Project-specific fact, rule, or documented exception.
3. Applicable shared standard.
4. Reusable pattern.
5. Historical material, used only to explain prior state.

Conflicts at the same level require clarification. Recency alone does not override an accepted decision.

## Document identity

Paths are stable identifiers. Rename files only when the concept itself changes, and update inbound links in the same change. ADR filenames are permanent. Project IDs and metadata use lowercase kebab case.

Recommended front matter fields are `title`, `status`, `owners`, `last_reviewed`, `applies_to`, and `tags`. The document body remains complete without metadata-aware tooling.

## Retrieval design

Documents use predictable filenames and headings so retrieval can combine path filters, lexical search, links, and embeddings. Each section should make sense when retrieved independently. Avoid pronouns whose referent exists only several sections earlier, and keep key terminology consistent with the glossary.

An indexer may treat each second- or third-level heading as a chunk while retaining path, title, status, project ID, and heading ancestry as metadata.

## MCP projection

A future Model Context Protocol server can remain a thin adapter:

- Resources expose raw Markdown and directory indexes.
- Read tools assemble a project overview with applicable shared documents and decisions.
- Search returns excerpts plus stable repository paths and headings.
- Write tools validate templates, create reviewable files, and never silently mutate accepted ADRs.

Tool results should include commit identity or revision, source paths, and status so consumers can cite evidence and detect stale context.

## Portability constraints

- Plain Markdown must remain sufficient to read and edit all canonical content.
- No vendor-specific database is authoritative.
- Generated indexes may supplement, but never replace, source documents.
- Machine metadata must be optional, text-based, and Git-diffable.
