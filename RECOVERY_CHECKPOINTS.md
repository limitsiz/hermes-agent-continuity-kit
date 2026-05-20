# Recovery Checkpoints

A recovery checkpoint is a recoverable metadata baseline, not a raw transcript backup.

## Advancement rule

Advance a recovery checkpoint only after:

1. Encrypted archive coverage reaches the target archive cursor.
2. High-signal review coverage reaches the target review/audit cursor.
3. Supporting metadata and safe-summary changes are committed.
4. Recovery metadata is refreshed without raw or decrypted content.

## Generic checkpoint model

```yaml
checkpoint:
  checkpoint_id: <RECOVERY_CHECKPOINT_ID>
  archive_cursor_id: <ARCHIVE_CURSOR_ID>
  review_audit_cursor_id: <REVIEW_CURSOR_ID>
  latest_completed_range: "<START_ID>-<END_ID>"
  supporting_commits:
    archive: "<ARCHIVE_COMMIT_SHA>"
    archive_cursor: "<ARCHIVE_CURSOR_COMMIT_SHA>"
    safe_summary_policy: "<SAFE_SUMMARY_POLICY_COMMIT_SHA>"
    review_cursor: "<REVIEW_CURSOR_COMMIT_SHA>"
    recovery: "<RECOVERY_COMMIT_SHA>"
```

## Meaning

A checkpoint means the operator can reconstruct safe state from committed metadata, encrypted archive artifacts, and safe summaries.

## Non-meaning

A checkpoint does not mean:

- Raw transcripts are stored in shareable docs.
- Decrypted archive content exists in the repo.
- Private keys are readable by the agent.
- Archive and review cursors are the same concept.
- Future cursor advancement can be automatic without gates.
