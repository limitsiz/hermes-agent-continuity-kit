# Review Workflow

This document defines a generic metadata-only review workflow for a HermesAgent
Continuity Kit. It complements the archive workflow by describing how safe
summaries and audit notes can be produced without exposing private content.

## Purpose

The review workflow exists to answer:

- Which placeholder cursor range has been reviewed?
- Were any gaps, overlaps, or anomalies detected?
- Are the archive manifest and monthly index internally consistent?
- Is it safe to advance the review cursor after explicit approval?

It must not expose raw content, decrypted content, secrets, or private metadata.

## Review cursor

The review cursor is independent from the archive cursor.

- Archive cursor: highest placeholder source cursor covered by encrypted archive
  artifacts.
- Review cursor: highest placeholder source cursor covered by metadata-only
  review.

The review cursor may lag behind the archive cursor. It should advance only when
safe summaries and validation notes exist for the relevant placeholder range and
an explicit approval gate has been satisfied.

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

## High-signal review checks

The review should focus on signals that are useful without private content:

- Coverage: does the placeholder range appear covered by a manifest and index?
- Continuity: are gaps or overlaps reported?
- Integrity: are placeholder hash fields present and marked verified?
- Safety: do safety booleans remain false for raw/private/decrypted content?
- Approval: are scope, archive, review, and cursor gates recorded?
- Drift: do archive cursor, review cursor, and checkpoint relationships make
  sense?
- Boundary: are sibling repositories represented only as generic read-only
  boundaries?

## Safe-summary outputs

A safe review output may include:

- `<REVIEW_SCOPE_ID>`
- `<START_CURSOR>` and `<END_CURSOR>` placeholders.
- Generic status labels.
- Counts of manifests or index entries.
- Gap/overlap booleans.
- A short anomaly list with no private values.
- A recommendation such as `<ADVANCE_REVIEW_CURSOR>` or
  `<DO_NOT_ADVANCE_REVIEW_CURSOR>`.

A safe review output must not include excerpts, raw message text, decrypted
archive text, secret values, private paths, or real identifiers.

## Review gates

Use explicit gates:

1. **Scope gate:** approve the metadata-only review range.
2. **Input gate:** confirm only allowed inputs are available.
3. **Output gate:** confirm safe-summary output contains no forbidden content.
4. **Validation gate:** run structural and redaction checks.
5. **Cursor gate:** approve review cursor advancement separately from review
   generation.
6. **Commit gate:** approve any file staging, commit, or push separately.

## Cursor advancement rule

Advance the review cursor only if all are true:

- The review scope was explicitly approved.
- Review output is metadata-only.
- Validation checks are clean.
- No forbidden input or output was used.
- Archive coverage is compatible with the target review cursor.
- The user explicitly approves review cursor movement.

If any condition fails, keep the cursor unchanged and report the anomaly using
safe metadata only.

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
and cron changes each require separate explicit approval.
