# Cursor Model

The Continuity Kit uses separate cursors for separate guarantees.

## Archive cursor

The archive cursor tracks encrypted backup coverage only.

It may advance only after:

1. The candidate range is locked.
2. Encrypted archive artifacts are produced.
3. Metadata-only manifests and index entries are produced.
4. Artifact size/checksum and linkage validation pass.
5. The archive artifacts and metadata are committed and pushed.

Template fields:

```yaml
archive_cursor:
  last_archive_message_id: <ARCHIVE_CURSOR_ID>
  previous_archive_message_id: <PREVIOUS_ARCHIVE_CURSOR_ID>
  latest_committed_range: "<START_ID>-<END_ID>"
  latest_committed_message_count: <MESSAGE_COUNT>
```

## Review/audit cursor

The review/audit cursor tracks high-signal safe-summary coverage only.

It may advance only after:

1. Metadata-only high-signal review is complete.
2. Safe summary, policy, or runbook updates are committed and pushed.
3. The target timestamp is verified by allowed metadata-only fields.

Template fields:

```yaml
sessions:
  last_seen_message_id: <REVIEW_CURSOR_ID>
  last_seen_message_timestamp: <REVIEW_CURSOR_TIMESTAMP>
updated_at: "<REVIEW_CURSOR_TIMESTAMP_UTC>"
```

## Separation rule

Advancing the archive cursor never implies advancing the review/audit cursor. Advancing the review/audit cursor never implies encrypted archive coverage.

## Recovery checkpoint alignment

A recovery checkpoint may advance only when both cursors intentionally align at a declared checkpoint and supporting metadata has been committed.
