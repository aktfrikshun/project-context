# Fan Fragment Submission Policy

## Product promise

The fragment submission system should invite broad fan creativity while preserving consent, privacy, safety, provenance, and canon discipline. Fans may submit text, source links, images, or video. Submission, receipt, editorial acceptance, public publication, generation eligibility, and canon promotion are separate events.

The public form and policy must explain these distinctions in plain language. The archive may decline, remove, or retain privately any submission and does not promise publication, response, or canon status.

## Contact and notification choice

The intake form includes an unchecked `Notify me about the outcome of this submission` choice.

- Email is required only when notification is selected; it may otherwise be omitted.
- The form must validate the conditional requirement on both client and server.
- Notification consent applies to transactional messages about that submission only. It does not enroll the submitter in marketing or a newsletter.
- FrikFan retains the email privately. It must not be included in the Creator staging envelope or public archive record.
- A submitter who opts in may receive an editorial outcome notice after review.
- An accepted submission receives a separate publication notice when a permanent public archive URL exists. The notice includes that URL and the approved attribution.
- An accepted submission is not described as published until the archive URL is live.
- Policy-rejected submissions receive no outcome or publication message, even when notification was requested. The public policy discloses this possibility without exposing moderation signals for a specific submission.

Every intake receives the same neutral on-screen acknowledgement and non-sequential public receipt token. It confirms receipt only, not safety review, acceptance, publication, or authenticity.

## Media submissions

The public form may accept multiple images and videos in addition to text and links. Operational file-count, size, duration, and format limits must be visible before upload and generous enough to support creative work, but they remain necessary for security and reliable processing.

Original media remains private and quarantined in FrikFan. Before staff preview or export, the system should:

- verify actual file signatures rather than trusting browser MIME declarations;
- enforce allowlisted image and video formats;
- enforce configured count, size, and duration limits;
- scan for malware and malformed files;
- prevent active content from being served inline;
- calculate and retain checksums for deduplication and provenance;
- preserve the original privately while generating safe review derivatives where appropriate;
- remove location and other unnecessary embedded metadata from public derivatives;
- transcode accepted public video to controlled delivery formats when required.

The submitter must confirm that they created the material or have permission to share it and identify whether it contains or depicts real people. Public display requires explicit publication permission. The archive may request additional releases or decline material involving real people.

FrikFan Active Storage identifiers are private implementation details and are never exported as portable attachment references. After editorial acceptance, FrikFan and Creator OS use an authenticated two-phase media transfer: create the sanitized staging envelope, receive an ingestion ID and bounded upload authorization, transfer each approved attachment with its checksum and manifest, then mark the envelope complete. Creator stores its own staging copy.

## Publicly forbidden content

The submission page must link to or display a concise public policy stating that the following content is forbidden:

- sexual exploitation or sexual content involving minors, or anyone presented as a minor;
- non-consensual intimate imagery, sexual coercion, or content shared without the depicted person's permission;
- doxxing, private contact or location information, credentials, financial data, medical records, or other sensitive personal information submitted without authority;
- credible threats, targeted harassment, stalking, hateful abuse, or encouragement of violence against a person or protected group;
- instructions or encouragement for suicide, self-harm, abuse, exploitation, or serious criminal activity;
- malware, executable payloads, phishing, credential theft, spam, or attempts to compromise the service;
- stolen work, unauthorized copyrighted media, impersonation, or material the submitter does not have the right to share;
- fabricated accusations about identifiable real people, deceptive real-world emergency reports, or content intended to cause real-world panic or harm;
- graphic cruelty, torture, gore, or sexual violence submitted for shock or gratification rather than legitimate documentary review;
- explicit pornography or fetish content unrelated to a legitimate archive or artistic review purpose;
- content whose principal purpose is advertising, solicitation, manipulation of archive status, or evasion of a prior moderation decision;
- any content illegal to possess, transmit, or publish in the applicable jurisdiction.

The public policy should also state:

> Forbidden submissions may be rejected, removed, preserved only as required for safety or legal handling, or referred to appropriate services without individual notice. A submission receipt does not mean the material passed review.

Policy language and handling procedures should receive appropriate legal review before public launch, especially for unlawful sexual content, mandatory reporting, copyright complaints, privacy requests, evidence retention, and law-enforcement requests.

## Silent policy rejection

`policy_rejected` is an internal moderation result, not a public status. The system must:

- show the same neutral receipt response at intake;
- avoid confirming which automated or human rule matched;
- send no acceptance, decline, or publication notification;
- prevent export to Creator OS and public search;
- retain only the minimum record required by the documented safety, abuse, and legal-retention procedure;
- preserve auditable internal handling without copying prohibited content into ordinary application logs.

Normal editorial declines that do not involve forbidden content may receive a respectful generic outcome notice when the submitter opted in. This distinction prevents silence from being used as a moderation oracle while still treating good-faith contributors humanely.

## Status separation

Recommended internal dimensions:

- **Safety:** pending, cleared, quarantined, policy_rejected, escalated.
- **Editorial:** received, under_review, needs_clarification, accepted, declined, withdrawn.
- **Export:** not_eligible, pending, staged, media_transferring, complete, failed.
- **Publication:** private, preparing, published, removed.
- **Canon:** unreviewed, contribution, proposed_artifact, canon_review_requested, promoted.
- **Notification:** not_requested, pending_outcome, outcome_sent, pending_publication, publication_sent, suppressed.

No single enum should collapse these independent facts.

Source: Allen Taylor decisions recorded 2026-08-03; `architecture/security-and-privacy.md`; `product/workflows.md`; `projects/frikfan.md`; `projects/creator-frikshun.md`
