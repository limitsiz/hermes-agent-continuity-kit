# Public / Private Boundary

This kit is a shareable continuity blueprint. It documents safe workflows,
templates, and validation rules without carrying private operational state.

## Public Kit

The Public Kit may contain:

- Generic docs and workflow descriptions.
- Placeholder-only templates.
- Validation checklists and public-readiness rules.
- Synthetic examples explicitly labeled as synthetic.
- Safe status vocabularies such as `<NO_OP>`, `<CANDIDATE_READY>`, and
  `<BLOCKED_ANOMALY>`.

The Public Kit must remain safe to publish or share. Placeholder values such as
`<ARCHIVE_CURSOR_ID>`, `<REVIEW_CURSOR_ID>`, `<RECOVERY_CHECKPOINT_ID>`,
`<PRIVATE_STATE_PATH>`, `<ARCHIVE_ARTIFACT_PATH>`, and `<SAFE_SUMMARY_FILE>`
stand in for private instance data.

## Private State

Private State is the instantiated state for a specific installation. It may
include real cursor values, manifest/index metadata, checkpoint records, cron
reports, archive artifact references, and local operational summaries.

Private State does not belong in the Public Kit. If a workflow needs to mention
private state in public docs, use placeholders and describe the class of data,
not the actual value.

## Private Ops

Private Ops are executable or operator-driven procedures that read, write, or
mutate an installation. Examples include:

- Memory audit scanners that inspect real local sources.
- Memory writers that persist approved findings.
- Archive producers that package and encrypt source content.
- Recovery/decrypt runners that use private identities.
- Handoff builders that compile private project state.
- Cursor advancement, cron changes, staging, commit, or push automation.

Private Ops must be approval-gated and must not be copied into the Public Kit
unless rewritten as placeholder-only documentation or synthetic sample logic.

## Forbidden in public docs

Never include the following in public/shareable files:

- Raw transcript or message body content.
- Messaging-platform plaintext exports.
- Session database plaintext.
- Decrypted archive content.
- Secrets, tokens, passwords, cookies, `.env` values, auth material, or private
  key material.
- Real private repository paths, artifact paths, database paths, cron job IDs,
  commit hashes, cursor IDs, message IDs, ranges, delivery targets, or user- or
  operator-specific identity details.

## Boundary test

A file is public-safe only if it can be published without revealing the
installation that produced it. If a value identifies a real machine, user,
repository, session, artifact, key, cursor, or project, replace it with a
placeholder or move it to Private State.

## Public product boundary

Public kit material must not include private operator identity material,
private team operating structures, peer-agent project details, real runtime
paths, real cursor/message identifiers, or private archive metadata.


## Runtime boundary

The public runtime skeleton is safe scaffolding. Private state belongs only in a local target directory created by the installer and must not be copied back into the public repository.
