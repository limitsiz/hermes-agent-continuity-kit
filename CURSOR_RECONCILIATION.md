# Cursor Reconciliation

Cursor reconciliation compares archive coverage, review/audit coverage, cron
baselines, and recovery checkpoints using metadata-only checks. It resolves
state ambiguity without reading or printing raw content.

## Purpose

Use reconciliation when docs, reports, or operators disagree about the current
checkpoint. The goal is to identify which cursor value each state surface
actually represents and what gate, if any, remains.

## Inputs

Allowed inputs are metadata-only:

- Archive cursor template or private instance fields.
- Review/audit cursor template or private instance fields.
- Report-only cron baseline fields.
- Manifest/index coverage summaries.
- Recovery checkpoint metadata.
- Current maximum source cursor from an allowed metadata-only query.

Forbidden inputs include raw messages, session plaintext, decrypted archives,
secrets, private key material, and platform plaintext exports.

## Metadata-only checks

A reconciliation check may read scalar fields such as:

- `<ARCHIVE_CURSOR_ID>`
- `<REVIEW_CURSOR_ID>`
- `<RECOVERY_CHECKPOINT_ID>`
- `<LATEST_ARCHIVE_RANGE>`
- `<CRON_BASELINE_CURSOR_ID>`
- `<CURRENT_MAX_SOURCE_CURSOR_ID>`

It must not select, print, or persist content fields.

## Archive cursor checks

The archive cursor answers: what source range has encrypted backup coverage?

Check that:

- The archive cursor points to the latest committed archive coverage.
- The latest manifest/index placeholders agree with that cursor.
- Candidate archive ranges start after the archive cursor.
- Archive cursor movement is separate from review/audit cursor movement.

## Review/audit cursor checks

The review/audit cursor answers: what source range has high-signal safe-summary
coverage?

Check that:

- The review/audit cursor field is read from its own state surface.
- Report-only audit jobs use it as the baseline for future candidate review.
- Archive dry-runs treat it as reference-only and not as the archive range
  source.
- Review cursor movement is separately approved when needed.

## Cron baseline checks

Cron outputs may be used only as reports. They do not become the source of truth
unless their values are reconciled with the relevant cursor files or private
state surfaces.

A report-only cron must not create archives, decrypt archives, move cursors,
commit, push, or change its own schedule.

## Candidate range checks

Archive candidate ranges are computed from the archive cursor only:

```text
<CANDIDATE_START_CURSOR> = <ARCHIVE_CURSOR_ID> + 1
<CANDIDATE_END_CURSOR> = <CURRENT_MAX_SOURCE_CURSOR_ID>
```

Review/audit cursor references may be reported for visibility, but they must not
change archive candidate range computation.

## Resolution patterns

- If archive and review/audit cursors match, do not plan another review cursor
  advancement for that checkpoint.
- If archive cursor is ahead of review/audit cursor, plan safe-summary review and
  review cursor advancement as separate gates.
- If review/audit cursor is ahead of archive cursor, do not infer encrypted
  backup coverage; plan archive coverage separately.
- If recovery checkpoint lags both cursors, refresh recovery metadata only under
  a separate approval gate.

## Forbidden checks

Do not reconcile by printing raw transcripts, platform plaintext, decrypted
archive content, secrets, private paths, or real identifiers in public docs. In
shareable material, all values must remain placeholders.
