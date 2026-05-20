# Report-only Cron Dry-runs

Cron dry-runs are observers, not writers.

## Required mode

Every dry-run cron must remain:

```yaml
mode:
  report_only: true
  metadata_only: true
  no_write: true
  no_archive: true
  no_decrypt: true
  no_cursor_advance: true
  no_commit_push: true
```

## Allowed metadata queries

Allowed query classes:

- Count records after the archive cursor.
- Read min/max id after the archive cursor.
- Read max timestamp after the archive cursor.
- Read ordered id/timestamp windows.

Forbidden query classes:

- `SELECT *`.
- Message content columns.
- Reasoning or tool payload columns.
- Session prompt or handoff text.
- Platform export plaintext.

## Status vocabulary

```yaml
no-op: "No records beyond the archive cursor."
candidate-ready: "A contiguous candidate range exists and checks pass."
blocked-anomaly: "A safety, integrity, repo, cursor, or metadata anomaly blocks automation."
```

## Required safety flags

Every cron report should include:

```yaml
raw_content_printed: false
files_modified: false
archive_created: false
archive_decrypted: false
archive_cursor_advanced: false
review_cursor_advanced: false
cron_changed: false
commit_push_performed: false
private_identity_read: false
```

## Scheduling guidance

Schedule dry-runs so they do not overlap other maintenance jobs. Keep the cron prompt self-contained and scoped to metadata-only operations.
