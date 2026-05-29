# Continuity Kit Architecture

This document describes a generic, shareable architecture for a Hermes Agent
Continuity Kit. It intentionally uses placeholders and policy language only. It
must not contain private paths, real identifiers, raw message content, decrypted
content, secrets, or environment-specific metadata.

## Goals

- Preserve operational continuity across restarts, migrations, and recovery
  events.
- Detect durable memory candidates without exposing private content.
- Keep archive, review, and recovery state aligned without merging their
  meanings.
- Separate public docs/templates from private state and private operations.
- Make all writes, cursor movement, archive production, decrypt, staging, commit,
  push, and cron changes explicit, gated, and reviewable.

## Non-goals

- This kit does not define an role-specific operator identity system.
- This kit does not store raw transcripts or decrypted archive content.
- This kit does not include private keys, tokens, cookies, auth files, or local
  database paths.
- This kit does not prescribe a specific hosting provider, repository name,
  messaging platform identifier, or user-specific assistant identity.
- This kit does not provide auto-write memory behavior by default.

## Layer model

Use three layers:

1. **Public Kit:** shareable docs, templates, workflows, placeholder examples,
   and validation rules.
2. **Private State:** instantiated cursor files, manifests, indexes, checkpoint
   metadata, audit reports, and safe-summary surfaces for a private installation.
3. **Private Ops:** executable workflows that scan, write, archive, decrypt,
   refresh recovery metadata, build handoffs, change cron, move cursors, or
   perform git operations.

Only the Public Kit layer belongs in shareable materials.

## Component model

A continuity setup can be modeled as these components:

- **Memory audit:** metadata-aware candidate detection for durable facts,
  decisions, project state, and workflow lessons.
- **Persistent memory:** compact approved durable facts used by the assistant in
  future sessions.
- **Safe-summary surfaces:** human-readable summaries, active project state,
  decision logs, audit notes, and policy/runbook summaries.
- **Archive cursor:** the highest source cursor safely covered by encrypted
  archive artifacts.
- **Review/audit cursor:** the highest source cursor safely reviewed into
  metadata-only summaries or audit notes.
- **Recovery checkpoint:** the highest source cursor that a fresh agent can treat
  as operationally summarized and restorable.
- **Archive manifest:** a metadata-only record describing an encrypted archive
  batch, placeholder references, integrity status, and approval gates.
- **Monthly index:** a metadata-only index that groups archive manifests and
  tracks coverage, gaps, overlaps, and review state.
- **Report-only cron dry-run:** a scheduled metadata check that reports status
  without writing files, moving cursors, creating archives, or changing jobs.
- **Safety boundary:** rules that prevent private content from entering
  shareable documentation or templates.

## Relationship overview

The components should form a gated control flow:

1. A metadata-only scope is selected.
2. Memory audit produces candidates, not writes.
3. The user approves any write target explicitly.
4. Archive production is separately approved.
5. Encrypted artifacts are produced outside shareable docs.
6. Manifests and indexes record only safe metadata and placeholders.
7. Validation checks confirm integrity and redaction boundaries.
8. Archive cursor advancement is separately approved.
9. Review/audit cursor advancement is separately approved when needed.
10. Recovery checkpoint refresh occurs only after relevant archive and review
    state align and a separate recovery gate is approved.
11. Cron dry-runs report drift or missing work but do not mutate state.

## Cursor model overview

Cursors are monotonic metadata markers. They should be treated as separate state
surfaces:

- Archive cursor answers: "What source range is safely archived?"
- Review/audit cursor answers: "What source range has safe metadata-only review?"
- Recovery checkpoint answers: "What source range is safe to rely on for
  recovery?"

When archive and review/audit cursors are reconciled at the same placeholder
checkpoint, do not plan another review cursor advancement for that checkpoint.
Treat remaining work as documentation/state reconciliation or recovery checkpoint
refresh, each under its own gate.

## Memory audit flow overview

Memory audit is report-only by default:

- Scan from an approved placeholder baseline.
- Produce candidate findings and proposed target surfaces.
- Ask for explicit approval.
- Apply only approved writes in private state or assistant memory.
- Validate changed surfaces and protected boundaries.

## Archive flow overview

Archive flow is gated:

- Scope lock: define a metadata-only range using placeholders.
- Build approval: receive explicit approval before archive production.
- Artifact creation: produce encrypted artifacts outside the shareable kit.
- Manifest update: record only placeholder paths, placeholder hashes, and safety
  booleans.
- Validation: verify the manifest has no raw/private content.
- Commit approval: commit only after validation and explicit approval.
- Cursor approval: advance cursor only after archive commit/push approval.

## Review/audit flow overview

Review flow is metadata-only:

- It may inspect safe summaries, counts, placeholder ranges, and manifest status.
- It must not print or persist raw transcript content.
- It must not print or persist decrypted archive content.
- It must produce candidate summaries, anomaly notes, and cursor recommendations.
- It advances the review/audit cursor only through an explicit gate when needed.

## Recovery checkpoint alignment

A checkpoint is aligned when:

- Archive coverage is present through `<RECOVERY_CHECKPOINT_ID>`.
- Review/audit coverage is present through `<RECOVERY_CHECKPOINT_ID>`.
- Manifest and monthly index validation are clean.
- Protected files and private data boundaries remain unchanged.
- The checkpoint is updated only after explicit approval.

## Data classification boundaries

Use three broad classes:

- **Public/shareable metadata:** generic documentation, placeholder schemas,
  safety booleans, and redaction rules.
- **Private metadata:** local paths, real identifiers, real cursor values, real
  repository names, real commit hashes, real job IDs, and real artifact names.
- **Private content:** raw messages, transcripts, decrypted archives, secrets,
  private keys, cookies, and database plaintext.

Only public/shareable metadata belongs in this kit.

## Safe adoption pattern

A safe adopter should:

1. Copy the generic docs and templates.
2. Replace placeholders only in a private repository or local secure location.
3. Keep raw/private data outside the shareable kit.
4. Validate Markdown and YAML structure.
5. Run private metadata and secret scans before commit.
6. Use explicit approval gates for staging, commit, push, archive creation,
   cursor movement, decrypt/recovery, and cron changes.

## Public component vocabulary

The public architecture uses these role-agnostic components:

- **Continuity Engine:** coordinates safe continuity state across sessions.
- **Memory Router:** classifies candidate updates before any write.
- **Audit Ledger:** records reviewed metadata, approvals, and cursor decisions.
- **Encrypted Archive Pipeline:** preserves raw source material only as encrypted artifacts.
- **Recovery Workbench:** restores from safe metadata and approved private material.
- **Knowledge Workspace Adapter:** connects approved summaries to a user-selected workspace.
- **Approval Kernel:** enforces profiles, allowlists, hard stops, and receipts.
- **Release Test Harness:** validates public-readiness and clean-server behavior.

The architecture is not tied to any external method, person, private operating
role, peer-agent system, or specific note-taking product.
