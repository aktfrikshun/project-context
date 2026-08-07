# Data and Memory

Canon, artifact status, public visibility, and generation eligibility are separate dimensions. Provenance must survive imports and normalization. Creator OS currently upserts archive Markdown by source path and excludes unresolved mystery entries from generation by default.

Retrieval should prefer:

1. accepted canon and decisions relevant to the task;
2. active visual canon for production imagery;
3. current product/architecture documentation;
4. project-specific implementation context;
5. drafts and historical material only when their status is explicit.

Conversation history is not canon. Generated descriptions must state only what is visible or supplied and may not invent external facts. Long-term conversational memory, semantic search, and cross-session continuity are proposed capabilities unless a project document identifies them as implemented.

## Cross-application submission promotion

FrikFan is authoritative for an audience member's original fragment submission, consent choices, contact information, private attachments, moderation history, and export state. Creator OS is authoritative for its staging inbox and every later creative or publication record derived from an accepted submission.

Promotion uses an asynchronous, idempotent envelope sent to a Creator-owned authenticated ingestion web service after the FrikFan transaction commits. The envelope contains only the information approved and required for creative review. Creator validates the envelope and performs its own staging write. Failure to reach Creator OS leaves the accepted FrikFan record intact and retryable; FrikFan has no Creator database credentials and the systems do not attempt a distributed database transaction.

The Creator staging inbox must remain separate from canonical status, public visibility, and generation eligibility. Those dimensions change only through explicit review actions.

Source: `creator_frikshun/README.md`, `frikshun_creator/services/generation_context.py`; marketing archive canon discipline; `frikfan/AI_AGENTS_README.md`
