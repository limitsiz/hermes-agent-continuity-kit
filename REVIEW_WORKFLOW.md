# Review Workflow

This document defines a generic metadata-only review workflow for a Hermes Agent
Continuity Kit. It complements memory audit and archive workflows by describing
how safe summaries and audit notes can be produced without exposing private
content.

## Purpose

The review workflow exists to answer:

- Which placeholder cursor range has been reviewed?
- Were any gaps, overlaps, or anomalies detected?
- Are the archive manifest and monthly index internally consistent?
- Are there high-signal memory or safe-summary candidates?
- Is it safe to recommend a later review/audit cursor gate?

It must not expose raw content, decrypted content, secrets, or private metadata.

## Review/audit cursor

The review/audit cursor is independent from the archive cursor.

- Archive cursor: highest placeholder source cursor covered by encrypted archive
  artifacts.
- Review/audit cursor: highest placeholder source cursor covered by metadata-only
  review and safe-summary handling.

The review/audit cursor may lag behind, match, or be ahead of the archive cursor.
Each case has different meaning and must be reconciled without assuming one
cursor implies the other.

## Metadata-only scope lock

Before review begins, lock the scope with placeholders:

- `<REVIEW_SCOPE_ID>`
- `<START_CURSOR>`
- `<END_CURSOR>`
- `<ARCHIVE_BATCH_ID>`
- `<MONTH_KEY>`
- `<EXPECTED_MANIFEST_REF>`

The scope lock should describe what will be reviewed without listing real
message identifiers, private paths, or raw content.

## Allowed inputs

Allowed inputs are metadata-only and redacted:

- Placeholder cursor ranges.
- Manifest schema fields and safety booleans.
- Monthly index coverage fields.
- Counts of batches, gaps, overlaps, or validation failures.
- Generic status values such as `<VERIFICATION_STATUS>` or `<REVIEW_STATUS>`.
- Safe summaries that contain no raw/private content.
- Candidate memory classes with no raw excerpts.

## Forbidden inputs

The review workflow must not ingest, print, summarize, or persist:

- Raw transcript or message body content.
- Telegram or messaging-platform plaintext.
- Hermes database or session plaintext.
- Decrypted archive content.
- Private keys or private key markers.
- Secrets, tokens, passwords, cookies, `.env` contents, or auth material.
- Real private repository paths.
- Real artifact paths or filenames.
- Real commit hashes.
- Real cron job identifiers.
- Real messaging platform identifiers.
- Real database paths.

## High-signal candidate classes

Review should identify candidate classes, not auto-write them:

- Durable user preference.
- Stable environment or repo convention.
- Active project state.
- Durable decision.
- Reusable workflow lesson.
- Safety/boundary correction.
- No-op / do-not-save item.

## Candidate report

A safe candidate report may include:

- `<REVIEW_SCOPE_ID>`
- `<START_CURSOR>` and `<END_CURSOR>` placeholders.
- Candidate class.
- Short safe summary.
- Proposed target surface.
- Approval status.
- Safety flags.

A safe candidate report must not include excerpts, raw message text, decrypted
archive text, secret values, private paths, or real identifiers.

## Approval gate

Review and memory audit start as candidate report + explicit approval. No
persistent memory write, safe-summary update, decision-log update, cursor
movement, staging, commit, or push should happen until the user approves the
exact target and scope.

## Approved write routing

After approval, candidates may route to:

- Hermes persistent memory for compact durable facts.
- Safe-summary surfaces for human-readable state.
- Active project state for current work and gates.
- Decision log for durable decisions.
- No-op when the candidate is temporary, sensitive, stale, or unsafe.

## Cursor advancement rule

Advance the review/audit cursor only if all are true:

- The review scope was explicitly approved.
- Review output is metadata-only.
- Approved writes or no-op decisions are complete.
- Validation checks are clean.
- No forbidden input or output was used.
- The user explicitly approves review/audit cursor movement.

If archive and review/audit cursors are already reconciled at a checkpoint, do
not plan another review cursor advancement for that checkpoint.

## Failure and anomaly handling

If a review detects a problem:

- Do not move cursors.
- Do not create or decrypt archives.
- Do not commit or push unless separately approved.
- Report only generic anomaly types and placeholder references.
- Ask for the next approval gate if corrective action is required.

Example safe anomaly labels:

- `<GAP_DETECTED>`
- `<OVERLAP_DETECTED>`
- `<MISSING_MANIFEST>`
- `<INTEGRITY_NOT_VERIFIED>`
- `<FORBIDDEN_CONTENT_MARKER_DETECTED>`
- `<CURSOR_ALIGNMENT_MISMATCH>`

## Validation before commit

Before committing review workflow artifacts, run:

- Markdown heading and fenced code block checks.
- YAML parse checks for templates.
- Placeholder consistency checks.
- Private metadata scans.
- Raw/secret/private-key/decrypted marker scans.
- `git diff --check` for the intended files.
- `git add --dry-run` scoped to the intended files.

Staging, commit, push, cursor movement, archive production, archive decryption,
recovery refresh, and cron changes each require separate explicit approval.

## Candidate report model

Review starts with a metadata-only candidate report. Raw/high-signal review,
memory writes, safe-summary updates, and Audit Ledger cursor advancement each
require explicit approval under the relevant canonical profile.
