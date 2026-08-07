# Integrations

## Current or documented

- Social publication/metrics: Facebook Page, Instagram, Threads, X, YouTube, and FanVue in Creator OS; TikTok reel export is review-only. Canonical public endpoints are recorded in `identity/public-presence.md`.
- Music: DistroKid manages distribution; archive stores release metadata and streaming links.
- Media storage: local intake and private object storage with temporary public delivery where a platform requires it.
- AI: provider-backed text and image analysis/generation behind application services; absence or failure must degrade safely.
- Public/archive data: Rails and Creator OS share PostgreSQL; the public application owns coordinated durable schema changes.
- FrikFan: Rails interactive agents use a shared Chloe persona module with role-specific prompts.

## Integration rules

Use replaceable publisher/provider interfaces, least-privilege credentials, dry-run or review-first defaults where supported, explicit validation, error logging, and captured external URLs. Never copy credential values into knowledge documents.

Source: `creator_frikshun/README.md`; evil-plan architecture; `frikfan/AI_AGENTS_README.md`
