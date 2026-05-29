# Cursor Model

The Continuity Kit uses separate cursors for separate guarantees. Cursor values
in public docs must be placeholders, never real private message IDs or ranges.

## Cursor types

- **Archive cursor:** encrypted backup coverage.
- **Review/audit cursor:** high-signal review and safe-summary coverage.
- **Recovery checkpoint:** aligned recoverable baseline after the required archive
  and review/audit state is complete.

## Archive cursor

The archive cursor tracks encrypted backup coverage only.

It may advance only after:

1. The candidate range is locked.
2. Encrypted archive artifacts are produced under approval.
3. Metadata-only manifests and index entries are produced.
4. Artifact size/checksum and linkage validation pass.
5. The archive artifacts and metadata are committed and pushed under approval.
6. A separate archive cursor advancement gate is approved.

Template fields:

```yaml
archive_cursor:
  last_archive_message_id: <ARCHIVE_CURSOR_ID>
  previous_archive_message_id: <PREVIOUS_ARCHIVE_CURSOR_ID>
  latest_committed_range: "<START_CURSOR>-<END_CURSOR>"
  latest_committed_message_count: <MESSAGE_COUNT>
```

## Review/audit cursor

The review/audit cursor tracks high-signal safe-summary coverage only.

It may advance only after:

1. Metadata-only high-signal review is complete.
2. Approved safe-summary, policy, memory, or runbook updates are complete.
3. The target timestamp or cursor metadata is verified by allowed metadata-only
   fields.
4. A separate review/audit cursor advancement gate is approved.

Template fields:

```yaml
sessions:
  last_seen_message_id: <REVIEW_CURSOR_ID>
  last_seen_message_timestamp: <REVIEW_CURSOR_TIMESTAMP>
updated_at: "<REVIEW_CURSOR_TIMESTAMP_UTC>"
```

## Recovery checkpoint

The recovery checkpoint represents a recoverable baseline. It may advance only
when the intended archive and review/audit coverage are aligned and supporting
metadata has been validated and approved.

Template fields:

```yaml
checkpoint:
  checkpoint_id: <RECOVERY_CHECKPOINT_ID>
  archive_cursor_id: <ARCHIVE_CURSOR_ID>
  review_cursor_id: <REVIEW_CURSOR_ID>
```

## Separation rule

Advancing the archive cursor never implies advancing the review/audit cursor.
Advancing the review/audit cursor never implies encrypted archive coverage.
Refreshing a recovery checkpoint never authorizes future automatic cursor
movement.

## Reconciliation rule

When archive and review/audit cursors are reconciled at the same checkpoint, do
not plan another review cursor advancement for that checkpoint. Treat remaining
work as documentation/state reconciliation or recovery checkpoint refresh, each
under its own explicit gate.

## Candidate range rule

Archive candidate ranges are computed from the archive cursor only:

```text
<CANDIDATE_START_CURSOR> = <ARCHIVE_CURSOR_ID> + 1
<CANDIDATE_END_CURSOR> = <CURRENT_MAX_SOURCE_CURSOR_ID>
```

The review/audit cursor may be reported as a reference, but it must not affect
archive candidate range computation.

## Common mistakes

Avoid these mistakes:

- Treating archive coverage as review coverage.
- Treating review coverage as encrypted backup coverage.
- Treating recovery checkpoint refresh as cursor advancement.
- Publishing real cursor IDs, message IDs, ranges, paths, or commit hashes in
  public docs.
- Moving any cursor from a report-only cron dry-run.
