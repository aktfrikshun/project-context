# Source Inventory

Authority reflects content and explicit status, not file modification time. “Current” means current within the available repository evidence.

| Repository | Source path | Category | Authority | Status / freshness | Destination | Notes |
|---|---|---|---|---|---|---|
| frikshun_marketing | `archives/chloe-katastrophe/canon/CHLOE_CANON_MASTER.md` | Identity, family, philosophy | Canon master | Current through July decisions | identity, overview | Primary normalized narrative source |
| frikshun_marketing | `archives/chloe-katastrophe/canon/CANON_DECISIONS.md` | Decisions | Accepted decisions | Current through 2026-07-24 | decisions, domain, history | Highest-value change authority |
| frikshun_marketing | `archives/chloe-katastrophe/canon/CANON_CHANGE_LOG.md` | History | Canon log | Current through 2026-07-24 | history, provenance | Freshness and supersession evidence |
| frikshun_marketing | `archives/chloe-katastrophe/canon/DAUGHTER_OF_ECHOES_ORIGIN_RECORD.md` | Future origin | Draft canon | Draft approved for development | character, concepts | Do not present every detail as settled |
| frikshun_marketing | `archives/chloe-katastrophe/canon/GREGOR_CANON_RECONCILIATION_2026-07-14.md` | Family | Confirmed plus labeled drafts | Current | relationships, conflicts | Separates testimony and lyric candidates |
| frikshun_marketing | `archives/chloe-katastrophe/canon/PUBLIC_IDENTITY.md` | Public identity | Canon | Contains open launch items | character, conflicts | Platform status may lag implementations |
| frikshun_marketing | `archives/chloe-katastrophe/canon/UNRESOLVED_QUESTIONS.md` | Open questions | Canon-managed unresolved | Current | conflicts | Must not be guessed |
| frikshun_marketing | `archives/chloe-katastrophe/stories/TIMELINE.md` | History | Current narrative doc | Current family refinements | timeline | Future dates mostly unspecified |
| frikshun_marketing | `archives/chloe-katastrophe/brand/BRAND_GUIDE.md` | Brand | Current guide | Current | UI, glossary | Public promise and motifs |
| frikshun_marketing | `archives/chloe-katastrophe/brand/FRIKFAN_PERSONA.md` | Fan persona | Project guide | Current | audiences, interaction | Also duplicated in standalone repo |
| frikshun_marketing | `archives/chloe-katastrophe/workflows/chlokat_evil_plan_packet/chlokat_evil_plan/` | Product/architecture | Final plans plus roadmap | July 2026; some scope superseded by code | product, architecture, ADR-001 | Public/private split explicitly decided |
| chloe-katastrophe | `canon/CANON_FACTS.md` | Identity/visual | Explicit canon in that repo | June 8; partly superseded | deprecated, conflicts | Preserve historical authority context |
| chloe-katastrophe | `canon/CHLOE_CANON_MASTER.md` | Identity/family | Canon master | Older than marketing archive | history, conflicts | Significant duplication/divergence |
| chloe-katastrophe | `canon/CANON_DECISIONS.md` | Decisions | Accepted in repo | June 2026 | deprecated | Establishes older visual reference |
| chloe-katastrophe | `AGENTS.md`, `workflows/IDE_AGENT_WORKFLOW.md` | Governance | Repository instructions | Current local discipline | README, ADR-003 | Additive change rules |
| frikshun_image_studio | `studio/chloe-model/appearance.md` | Visual identity | Canon | Active | UI, identity | Highest-priority appearance text |
| frikshun_image_studio | `studio/reference-packs/chloe_model_v1/MODEL_CARD.md` | Visual production | Approved model card | Approved 2026-06-26 | UI, ADR-002 | Production foundation |
| frikshun_image_studio | `studio/milestones/chloe_model_v1.json` | Visual milestone | Approved machine record | Complete, not superseded | ADR-002 | Locked traits and status |
| frikshun_image_studio | `studio/reference-packs/chloe_model_v1/` | Canon image references | Approved versioned pack | Approved 2026-06-26; not superseded | `assets/chloe-model-v1/` | Copied intact, including images, manifests, model cards, and prompt audits |
| frikshun_image_studio | `AGENTS.md` | Voice/visual governance | Repository instructions | Current | identity, boundaries | Adds glamour and pronunciation rules |
| Allen Taylor / FoxyAI / ChatGPT image generation | `projects/chloekatastrophe/assets/cybernetic-chloe-v1/` | Cybernetic visual canon | Approved | 4 stills + 1 motion study supplied and approved 2026-07-27 | cybernetic-body, ADR-005, ADR-006 | Manifest checksums and per-asset limitations are authoritative |
| Allen Taylor | `projects/chloekatastrophe/decisions/adr-006-cybernetic-left-eye.md` | Cybernetic eye canon | Accepted decision | Explicitly approved and visually grounded 2026-07-27 | cybernetic-body, Cybernetic Chloe model card | Dedicated headshot governs visible eye treatment; hidden mechanism remains unresolved |
| Allen Taylor | Direct confirmation recorded 2026-08-03 | Public social and fan profiles | Confirmed public identity canon | Current as of confirmation | `identity/public-presence.md` | Exact Facebook, Instagram, TikTok, YouTube, X, and FanVue URLs; clean FanVue profile distinguished from referral URL |
| creator_frikshun | `README.md` | Creator implementation | Current implementation doc | Current; later than evil-plan MVP | capabilities, architecture | Secrets/config values excluded |
| creator_frikshun | `docs/fan-engagement-cadence.md` | Engagement | Current operating policy | Current | workflows, rules | No compulsory ordinary-post footer |
| creator_frikshun | `docs/chloe_tiktok_series/series-bible.md` | Video production | Canon-derived guidance | v0.1, voice provisional | voice, UI | Visual rules match Model v1 |
| creator_frikshun | `frikshun_creator/services/` | Implementation | Code evidence | Current | project context | Summarized, not copied |
| chlokat_frikshun | `README.md` | Public archive architecture | Current project README | Early implementation | architecture, project | Defines schema ownership |
| frikfan | `AGENTS.md` | Persona/product boundaries | Repository instructions | Current | boundaries, project | Trust and adult-adjacent constraints |
| frikfan | `app/services/ai_agents/chloe_persona.rb` | Conversational behavior | Current implementation | Tested | voice, interaction | Role-neutral persona module |
| frikfan | `AI_AGENTS_README.md` | Agent architecture | Current documentation | Current | capabilities, architecture | Model/endpoints stay project-specific |

Repositories `wayfinder`, `signal-journal`, and `frikshun_dev_stack` were searched; no substantive Chloe knowledge was found beyond shared infrastructure references. `frikshun_marketing` outside the Chloe archive was searched through the archive scope where the maintained material resides.
