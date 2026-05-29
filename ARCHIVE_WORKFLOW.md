# Manual Gated Archive Workflow

This workflow creates encrypted archives without leaking raw content into docs, logs, commits, or chat reports.

## Gate 1: Metadata-only scope lock

Allowed actions:

- Read the archive cursor.
- Query only metadata fields such as id, timestamp, count, min, and max.
- Compute candidate range and chunk preview.
- Check gap, overlap, duplicate range, duplicate path, and dirty repo status.

Forbidden actions:

- Selecting raw content fields.
- Decrypting archives.
- Creating archive files.
- Advancing cursors.
- Committing or pushing.

## Gate 2: Archive production, local no-push

After approval, produce encrypted artifacts and metadata-only manifests/index entries.

Canonical artifact format:

```text
archive/encrypted/YYYY/MM/hermes-incremental-archive-<START_ID>-<END_ID>-<RUN_TIMESTAMP>.tar.zst.age
```

Canonical manifest format:

```text
archive/manifests/YYYY/MM/hermes-incremental-archive-<START_ID>-<END_ID>-<RUN_TIMESTAMP>.manifest.yaml
```

Canonical monthly index format:

```text
archive/indexes/YYYY/MM/YYYY-MM.index.yaml
```

Do not use `.age.zst`, ad-hoc `messages-<range>` names, or parallel monthly index names.

## Gate 3: Validation

Validate encrypted artifact size/checksum, manifest linkage, index linkage, gap/overlap safety, temporary plaintext cleanup, and unchanged cursor files.

## Gate 4: Archive commit and push

Stage only the approved encrypted artifacts, manifests, and index files. Use normal push only. No force push, rebase, or merge unless explicitly approved.

## Gate 5: Archive cursor advancement

Advance the archive cursor in a separate approval gate after archive commit/push succeeds.

## Gate 6: Review workflow

High-signal review and review cursor advancement remain separate gates.

## Encrypted Archive Pipeline

This workflow is the Encrypted Archive Pipeline. It tracks encrypted artifacts,
metadata-only manifests, indexes, and archive cursor state separately from the
Audit Ledger review cursor.
