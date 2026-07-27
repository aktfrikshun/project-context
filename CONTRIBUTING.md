<!-- Purpose: Defines how knowledge changes are proposed, reviewed, and kept trustworthy. -->
# Contributing

Contributions improve the shared memory used by both people and AI systems.

## Before editing

- Confirm whether the knowledge is shared, project-specific, a reusable pattern, a historical note, or a decision.
- Search for an existing authority and update it instead of creating a duplicate.
- Verify facts with a subject-matter owner or durable source.
- Never add secrets, credentials, personal data, proprietary source code, chat transcripts, or unfiltered generated output.

## Authoring rules

- Use descriptive headings and short, complete sections.
- Put one durable concept under one canonical heading.
- Expand abbreviations on first use and add domain terms to the glossary.
- Use ISO 8601 dates (`YYYY-MM-DD`) and stable lowercase kebab-case identifiers.
- Use relative Markdown links within the repository.
- Label `Fact`, `Constraint`, `Decision`, `Recommendation`, `Example`, and `Open question` when the distinction could be unclear.
- Describe the current truth in project documents; preserve the reasoning and old state in ADRs or `history/`.
- Avoid tool-specific prompt tricks and time-sensitive prose such as “recently” or “currently” without a date.

## Metadata

New knowledge documents should use the fields described in [templates/document-template.md](templates/document-template.md). Keep metadata minimal and meaningful. `status`, `owners`, and `last_reviewed` support governance; `tags` and `applies_to` support retrieval.

## Decisions

Create an ADR when a choice changes system boundaries, data ownership, public contracts, security posture, operating model, or an expensive-to-reverse convention. Copy [templates/adr-template.md](templates/adr-template.md), assign the next four-digit number, and add it to [decisions/README.md](decisions/README.md).

Accepted ADRs are immutable records. Correct typos freely, but supersede a decision with a new ADR when its substance changes.

## Review checklist

- The document has one clear authority and scope.
- Claims are verified; unknowns are explicit.
- Shared defaults and project exceptions do not conflict silently.
- Links resolve and indexes are updated.
- Security and privacy boundaries are respected.
- A future reader can understand why the change matters.
- Stale or superseded guidance is marked and linked.

## Commit guidance

Prefer small commits with intent-focused messages such as `Document payment retry rules` or `Accept ADR 0007 for event ownership`. Reviews should include the relevant technical or business owner.
