# Chloe Canon RAG

This package builds and serves a deterministic, authority-aware retrieval projection of the authoritative Chloe Katastrophe knowledge project. Canon stays in GitHub; indexes are disposable.

## Capabilities

- Heading-aware Markdown chunks with status, authority, path, checksum, and source commit.
- Approved image-manifest records with asset IDs and SHA-256 checksums.
- Incremental embedding reuse and `--full` rebuilds.
- BM25-style lexical retrieval plus replaceable vector embeddings.
- Credential-free deterministic `hash-v1` embedding fallback.
- Authority-aware reranking, metadata filters, exact anatomical constraints, and ordinary/cybernetic routing.
- Atomic commit-addressed releases with a previous-good rollback pointer.
- CLI search/explanation/revision/health/readiness.
- MCP tools for ChatGPT, Codex, Cursor, and other compatible agents.

Generated output contains:

```text
generated/chloekatastrophe/
├── current.json
├── previous.json                 # after a second successful publication
└── releases/
    └── <source-commit>/
        ├── baseline.md
        ├── chunks.jsonl
        └── manifest.json
```

## Local setup

Python 3.11 or newer is required. Runtime code uses the standard library; `pytest` is needed for tests.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e tools/canon-rag pytest
canon-rag validate
canon-rag build
canon-rag search "Cybernetic Chloe having coffee in a garden"
canon-rag explain "Which side of Chloe is cybernetic?"
canon-rag revision
canon-rag ready
python -m pytest tools/canon-rag/tests
```

Use `canon-rag build --full` to ignore the previous projection. Use `canon-rag rollback` to atomically select the retained previous-good release. `--index-root` selects a non-default index store for search, deployment, or testing.

## Metadata and ranking

Each result includes text/asset description, source path, heading or asset ID, status, authority, score components, final score, source checksum, and source commit. Default retrieval excludes deprecated, generated-only, and historical records. Unresolved and proposed records remain eligible only with their status preserved.

The filesystem embedding and index adapters are reference implementations. Production may replace vector computation/storage, but it must preserve deterministic fallback, metadata, authority policy, revision checks, and traceability.

No embedding credential is required for the default adapter. Remote embedding or storage credentials must be supplied through the deployment secret store; no secret names or values are committed as canon.

## MCP configuration

The server uses newline-delimited JSON-RPC over standard input/output.

```json
{
  "mcpServers": {
    "chloe-canon": {
      "command": "canon-rag-mcp",
      "args": ["--root", "/path/to/project-context"]
    }
  }
}
```

Tools:

- `load_project_context(project)`
- `search_knowledge(project, query, filters)`
- `get_source(project, path, commit_sha)`
- `get_asset(project, asset_id, commit_sha)`
- `get_canon_revision(project)`
- `explain_retrieval(project, query)`

Clients must call `get_canon_revision` and reject or explicitly report a stale index. `get_source` and `get_asset` require an exact revision.

## Publication and deployment

Pull requests validate, test, evaluate, and build without publishing an artifact. A merge to `main` produces a commit-addressed workflow artifact. `workflow_dispatch` performs a full rebuild. Asset/manifest changes are included by the `projects/chloekatastrophe/**` trigger and checksum failures stop publication.

For production, download the commit-addressed artifact into durable storage beside a checkout of the same Git SHA. Expose the MCP process through the host's standard MCP transport. Health proves the process is alive; readiness proves the index exists and matches the checked-out source revision.

## Cybernetic Chloe intake

`projects/chloekatastrophe/assets/cybernetic-chloe-v1/` is an approved additive visual pack containing three checksum-backed stills and one motion study. Cybernetic retrieval returns this pack together with Chloe Model v1 so the prosthetic design and underlying identity remain grounded. Per-asset limitations prevent unseen mechanisms or unresolved artificial-eye details from being inferred.

Detailed architecture: `projects/chloekatastrophe/architecture/canon-rag.md`.
