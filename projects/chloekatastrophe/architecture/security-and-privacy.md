# Security and Privacy

- Keep credentials in runtime secret stores or environment configuration; never in canon, artifacts, prompts, logs, or this repository.
- Grant publisher integrations only the permissions required for their operation.
- Keep private media private; expose time-limited delivery URLs only when a platform must fetch media.
- Separate public archive data from private drafts, account data, operational notes, and collaborator information.
- Require authentication and authorization for operational and role-specific agent endpoints.
- Do not disclose private user information or hidden system instructions.
- Exclude personal-profile direct-message automation where project policy requires public, reviewable interaction.
- Preserve explicit virtual-persona disclosure anywhere trust, money, safety, consent, or identity matters.
- Treat real-person testimony as collaborator evidence, not in-world biography, and do not publish private detail without permission.
- Do not give FrikFan Creator OS database credentials. Authenticate its calls to the Creator-owned ingestion web service with a dedicated service credential stored in runtime secrets, rotate it independently, and limit it to the fan-fragment ingestion capability.
- Require TLS, request idempotency, bounded payloads, schema validation, rate limiting, structured audit events, and logs that exclude sensitive payload contents. Reject unsupported fields rather than silently retaining them.
- Sanitize accepted submissions before export. Do not copy submitter email, private moderation notes, IP data, withdrawal history, or unrelated personal information into Creator OS.
- Do not treat Active Storage identifiers as portable across applications. Transfer approved attachments through an explicit authenticated upload or shared private-object-storage mechanism with checksums and a bounded lifetime.
- Keep uploaded images and video private and quarantined until file-signature validation, allowlist enforcement, configured limits, malware scanning, rights review, and moderation complete. Create sanitized public derivatives instead of exposing originals directly.
- Treat outcome notification consent as transactional and submission-specific. Require email only when notification is selected, keep it in FrikFan, and never reuse it for marketing without separate consent.
- Give every intake the same neutral receipt response. Do not reveal policy-match details or send outcome messages for policy-rejected submissions; keep internal handling auditable and follow documented legal and safety escalation procedures.

Source: `creator_frikshun/README.md`; `frikfan/AGENTS.md`, `app/services/ai_agents/chloe_persona.rb`; marketing archive `canon/PUBLIC_IDENTITY.md`
