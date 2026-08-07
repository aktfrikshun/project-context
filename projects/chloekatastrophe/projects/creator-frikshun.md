# FrikShun Creator OS

Role: private local-first content transformation, publishing, metrics, and interaction-review cockpit.

It imports marketing-archive Markdown by source path, assigns generation eligibility, transforms artifacts into platform-specific drafts, publishes to supported channels, and records results. Current implementation is Flask with a shared PostgreSQL data boundary and provider adapters. Ordinary daily posts avoid compulsory promotional footers; dedicated participation messages carry broader invitations. Daily social drafts should express the artifact as a concise, emotionally complete signal rather than reproducing the full archive entry. The linked or source marketing-archive record may retain the longer reconstruction narrative and provenance.

Creator OS should support daily archive parity: before a socially active day closes, associate its publications with an artifact record, field note, daily signal log, or collaboration record in the marketing archive. Multiple platform variants and lightweight interactions may roll up to one daily record. Creator OS retains the complete private activity ledger; the public archive receives the curated durable layer.

For recovered-memory and recovered-artifact families, Creator OS assigns a stable public `CK-######` catalog entry ID and includes it in related social copy. The ID follows the record across platforms and does not imply confirmed canon. Automatic generation stores the chosen editorial family as metadata and randomly selects from families absent from the recent daily history, preventing accidental consecutive runs of `Questions from the Echo` or another single family.

Creator OS also stores and rotates a visual composition mode independently from editorial family: full-body action, environmental story, fine art, or editorial portrait. Recent modes are excluded from automatic selection. Prompt generation should treat mirrors, reflections, duplicate/alternate Chloes, translucent echoes, and static close-ups as overused rather than default Chloe imagery, while preserving Chloe Model v1 identity in every medium.

`Questions from the Echo` is the accepted recurring subseries within the `philosophy` editorial family. Project context owns its meaning, question eligibility, and claim boundaries in `experience/questions-from-the-echo.md`; Creator OS owns topic rotation, recent-topic avoidance, platform rendering, coordinated imagery, and generated-artifact validation.

## Fan-submission staging inbox

Creator OS should own a narrow staging inbox for sanitized, accepted fragment submissions exported from FrikFan. The inbox is an integration contract, not automatic artifact creation. Each envelope should carry a schema version, stable FrikFan submission public ID, unique idempotency key, classification, approved attribution, sanitized public candidate text, source/provenance summary, attachment manifest when supported, and export timestamps.

Creator OS imports a staged envelope through review-first processing, preserves its FrikFan provenance, and decides whether to create a proposed artifact or collaboration record. Receipt in the staging inbox does not make the contribution public, generation-eligible, or canon.

Creator OS owns the staging-table schema, migration changes, validation, and database writes. FrikFan receives no Creator database credentials. Creator exposes a versioned authenticated ingestion web service, initially equivalent to `POST /api/v1/intake/fan-fragments`, which accepts sanitized JSON envelopes and returns `202 Accepted` with a stable ingestion ID and acknowledgement state.

The service contract should require an authorization credential, schema version, stable FrikFan source submission ID, and idempotency key. It should validate payload size and fields, reject private or unsupported data, rate-limit the service identity, produce structured errors and request IDs, and log an audit event without logging sensitive payload contents. A status endpoint may be added if asynchronous processing requires FrikFan to reconcile acknowledgement state.

The ingestion contract supports accepted image and video manifests as well as text and links. Media uses an authenticated two-phase transfer or private object-storage handoff: Creator first creates the staging envelope and returns bounded upload authorization, FrikFan transfers approved files with checksums, and Creator marks the ingestion complete after validating the manifest. Media must not be represented by FrikFan Active Storage database identifiers.

Creator never receives submitter email, notification preferences, private moderation notes, policy-rejected material, or unrelated personal information. Its staging record contains only sanitized material that passed FrikFan safety, rights, and editorial review.

Important sources: `README.md`, `AGENTS.md`, `docs/fan-engagement-cadence.md`, `docs/chloe_tiktok_series/series-bible.md`, and `frikshun_creator/services/`.

Promote durable workflow/status rules; keep credentials, adapter configuration, exact models, endpoints, and operational commands project-specific.
