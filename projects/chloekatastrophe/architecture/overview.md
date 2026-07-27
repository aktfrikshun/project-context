# Architecture Overview

The durable boundary is conceptual rather than vendor-specific:

- **Knowledge sources:** reviewed canon, decisions, project context, artifacts, and provenance.
- **Private operations:** ingestion, analysis, draft generation, approval, campaigns, publishing, and metrics.
- **Public experience:** approved searchable artifacts, releases, news, lore, links, and fan-safe interaction.
- **External systems:** AI/media providers, social publishers, storage, analytics, and music distributors.

The public experience must not expose an admin cockpit. Provider adapters should remain replaceable. Canon selection occurs before generation, and human approval remains a meaningful boundary.

Current implementations use a Flask Creator OS, a Rails 8 public archive prototype, a shared PostgreSQL database, and separate FrikFan Rails agents. These are current choices, not Chloe canon.

Source: evil-plan `architecture/core_architecture.md`, `docs/architecture_clarification_2026-07-09.md`; `creator_frikshun/README.md`; `chlokat_frikshun/README.md`
