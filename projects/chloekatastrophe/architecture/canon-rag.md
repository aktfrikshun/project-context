---
title: Chloe Canon RAG Architecture
status: active
authority: implementation_detail
---

# Chloe Canon RAG Architecture

## Source-of-truth boundary

GitHub Markdown, JSON manifests, and approved Git LFS assets under `projects/chloekatastrophe/` are authoritative. Chunks, lexical statistics, embeddings, indexes, workflow artifacts, and service caches are rebuildable projections. They never become canon by being retrieved or published.

## Ingestion lifecycle

1. Validate required baseline files, relative links, status vocabulary, asset fields, file existence, and SHA-256 checksums.
2. Split Markdown by heading while preserving heading hierarchy, path, metadata, status, authority, and source commit.
3. Normalize image manifests into asset records with stable IDs, checksum, description, provenance, view, demonstrated features, limitations, and permitted uses.
4. Reuse embeddings only when record ID and source checksum match the previous good projection; `--full` disables reuse.
5. Build in a staging directory, rename it to `releases/<commit-sha>/`, then atomically update `current.json`.
6. Retain `previous.json` for rollback.

## Retrieval

Retrieval combines BM25-style lexical scores, replaceable vector similarity, authority score, exact anatomical-constraint bonuses, and continuity routing. The credential-free default is deterministic `hash-v1`; a production semantic provider can implement the same embedding adapter without changing storage or ranking contracts.

Default ranking/exclusion policy:

- accepted canon outranks accepted decisions;
- accepted decisions outrank current/implementation guidance;
- proposals and unresolved records retain visible status;
- generated, deprecated, and historical records are excluded unless explicitly requested;
- ordinary Chloe queries exclude the Cybernetic Chloe intake/specification;
- cybernetic queries retrieve both Chloe Model v1 identity and the cybernetic layer or its explicit gap.

## Runtime and MCP

The CLI supplies `build`, `validate`, `search`, `explain`, `revision`, `health`, `ready`, and `rollback`. `canon-rag-mcp` exposes:

- `load_project_context(project)`
- `search_knowledge(project, query, filters)`
- `get_source(project, path, commit_sha)`
- `get_asset(project, asset_id, commit_sha)`
- `get_canon_revision(project)`
- `explain_retrieval(project, query)`

Every result includes source path, heading or asset ID, authority/status, score components, final score, checksum where applicable, and source commit. Revision responses mark indexes stale when the checked-out/published source differs.

## Deployment

Run the service beside a read-only checkout of the published canon revision and an index artifact produced for the same SHA. Health means the process responds; readiness additionally requires a current, complete index. Publish commit-addressed workflow artifacts atomically to durable storage in production, then change a single current-revision pointer. Keep the storage adapter replaceable; the filesystem adapter is the reference implementation.

ChatGPT, Codex, Cursor, and other IDE agents should connect to the same deployed MCP command/service and call `get_canon_revision` before relying on retrieved context. Credentials for remote embeddings or artifact storage belong in runtime secret stores, never this repository.

## Rebuild and rollback

```bash
canon-rag validate
canon-rag build
canon-rag build --full
canon-rag ready
canon-rag rollback
```

A failed validation, checksum, test, evaluation, or build must leave `current.json` unchanged. Rollback only changes the atomic pointer to the retained previous-good release.

Source: `tools/canon-rag/`, `.github/workflows/chloe-canon-index.yml`
