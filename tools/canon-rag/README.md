# Chloe Canon Retrieval Artifacts

This tool creates a deterministic, inspectable retrieval projection of the
authoritative Chloe Katastrophe Markdown. It does not create or modify canon.

## Outputs

- `baseline.md`: `overview.md` and the curated `AI_CONTEXT.md`, with source paths
  and the source revision.
- `chunks.jsonl`: one record per Markdown section, including its path, heading
  hierarchy, authority classification, retrieval eligibility, and revision.
- `manifest.json`: artifact schema, counts, and provenance.

The committed Markdown remains authoritative. Generated artifacts are disposable
and should be rebuilt from the Git revision they identify. Embeddings and a
vector database are intentionally outside phase one.

Prompt-audit Markdown in the approved visual reference pack is preserved as
provenance but excluded from chunk discovery so repeated provider prompts cannot
overwhelm narrative and visual canon. The pack model card and README remain
indexed.

## Run locally

Requires Python 3.11 or newer and has no runtime dependencies.

```bash
python -m pip install -e tools/canon-rag
canon-rag validate
canon-rag build
python -m pytest tools/canon-rag/tests
```

Set `CANON_SOURCE_REVISION` when building an artifact for a specific source
commit. Otherwise the tool uses the current Git `HEAD`.

## Authority behavior

The classifier retains all material but marks deprecated, generated, and
historical chunks as ineligible for default retrieval. Drafts, proposals, and
unresolved items are retained with `requires_status_label: true`. Consumers
should rank by `authority_score`, then lexical or semantic relevance, and must
preserve the source path and status in results.

Classification is deliberately conservative and deterministic. Add explicit
YAML `status` metadata as the repository vocabulary matures; do not use the
classifier to promote source material into canon.
