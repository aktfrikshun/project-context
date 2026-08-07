# FrikFan

Role: Rails 8 fan/entertainer platform and current home of conversational agents that share a Chloe persona layer.

Chloe operates as a resident virtual entertainer and guide across customer, entertainer, and owner support roles. Universal voice/disclosure/safety rules live in `app/services/ai_agents/chloe_persona.rb`; role-specific facts remain in each agent. Tests verify virtual disclosure, safety language, discovery links, and progressive disclosure.

## Public Chloe namespace

`https://fans.frikshun.com/chloe` is the canonical public application boundary for Chloe experiences hosted by FrikFan. It should use a Chloe-specific layout and navigation while remaining part of the FrikFan application, allowing interested visitors to move into broader FrikFan content without making that context compulsory at entry.

Planned routes beneath the namespace:

- `GET /chloe` — Chloe landing and orientation page
- `GET /chloe/archive` — public approved archive index
- `GET /chloe/archive/search` — archive query results
- `GET /chloe/archive/fragments/:public_id` — public fragment record
- `GET /chloe/fragments/new` — public fragment-submission form
- `POST /chloe/fragments` — fragment intake
- `GET /chloe/fragments/received/:public_token` — private submission acknowledgement without exposing a sequential database ID

Public archive queries must operate only on an approved, public projection of archive material. Private submissions, contact information, moderation notes, unpublished testimony, and operational metadata must never enter public search results.

FrikFan owns the original submission, submitter permissions, private attachments, and moderation history in its primary application database. Acceptance does not establish canon. A separate explicit promotion step may later send a sanitized accepted contribution to Creator OS for transformation and to the archive for curated publication.

The intake accepts text, source links, images, and video under the public policy in `product/fan-fragment-submission-policy.md`. Originals remain private and quarantined through safety, rights, and editorial review. Public derivatives may be created only after approval.

Notification is optional and submission-specific. The form presents an unchecked outcome-notification choice and requires email only when selected. FrikFan may send an editorial outcome notice after review and, for accepted material, a separate publication notice containing the permanent archive URL once it is live. Email and notification state remain private FrikFan data and are never exported to Creator OS.

Current implementation note: FrikFan presently uses SQLite for its primary Rails databases, while Creator OS uses the local `frikshun_content_development` PostgreSQL database. FrikFan must not connect to or write that database directly.

Creator OS should expose a narrow authenticated ingestion web service for versioned, sanitized, idempotent accepted-submission envelopes. FrikFan retains the original submission and moderation record, calls the service only after acceptance commits, and records export attempts, the Creator ingestion ID, acknowledgement state, and retry state locally. Creator OS validates the contract and owns every write to its staging and operational tables.

Promotion runs through a retryable background job using a stable source submission ID and idempotency key. Creator unavailability must not invalidate or roll back the accepted FrikFan submission.

Owner/admin review routes should remain authenticated and outside the public namespace, for example `admin/chloe/fragment_submissions`. Exact Rails route names and controller organization remain implementation details.

## Optional vanity hostname

`chloefans.frikshun.com` is a deferred deployment option, not a separate Chloe product or canonical content origin. If adopted, prefer redirecting it to `https://fans.frikshun.com/chloe` and retain that destination as the canonical URL. This avoids duplicate search indexing, split analytics, cookie ambiguity, and two competing public addresses while preserving easy access to the wider FrikFan experience.

Important sources: `AGENTS.md`, `AI_AGENTS_README.md`, `AI_AGENTS_DEVELOPER_GUIDE.md`, `app/services/ai_agents/chloe_persona.rb`, and its spec.

Promote universal identity and safety boundaries. Keep Rails stack, role endpoints, current model selection, and platform-specific support facts local.
