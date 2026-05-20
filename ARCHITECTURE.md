# Continuity Kit Architecture

This document describes a generic, shareable architecture for a HermesAgent
Continuity Kit. It intentionally uses placeholders and policy language only. It
must not contain private paths, real identifiers, raw message content, decrypted
content, secrets, or environment-specific metadata.

## Goals

- Preserve operational continuity across restarts, migrations, and recovery
  events.
- Keep archive, review, and recovery state aligned without exposing private
  content.
- Separate durable metadata from raw/private data.
- Make all cursor movement explicit, gated, and reviewable.
- Provide templates that can be adopted by another installation without copying
  private repository details.

## Non-goals

- This kit does not define a raw transcript storage format.
- This kit does not include decrypted archive content.
- This kit does not include private keys, tokens, cookies, or local database
  paths.
- This kit does not prescribe a specific hosting provider, repository name, or
  messaging platform identifier.

## Component model

A continuity setup can be modeled as these components:

- **Archive cursor:** the highest source cursor safely covered by encrypted
  archive artifacts.
- **Review cursor:** the highest source cursor safely reviewed into metadata-only
  summaries or audit notes.
- **Recovery checkpoint:** the highest source cursor that a fresh agent can treat
  as operationally summarized and restorable.
- **Archive manifest:** a metadata-only record describing an encrypted archive
  batch, its placeholder references, integrity status, and approval gates.
- **Monthly index:** a metadata-only index that groups archive manifests by a
  generic month key and tracks coverage, gaps, overlaps, and review state.
- **Report-only cron dry-run:** a scheduled metadata check that reports status
  without writing files, moving cursors, creating archives, or changing jobs.
- **Safety boundary:** the rule set that prevents private content from entering
  shareable documentation or templates.

## Relationship overview

The components should form a one-way control flow:

1. A metadata-only scope is selected.
2. Archive production is separately approved.
3. Encrypted artifacts are produced outside shareable docs.
4. A manifest records only safe metadata and placeholders.
5. Validation checks confirm integrity and redaction boundaries.
6. The archive cursor advances only after explicit approval.
7. Review produces safe summaries only.
8. The review cursor advances only after explicit approval.
9. A recovery checkpoint is refreshed only after the relevant archive and review
   state are aligned.
10. Cron dry-runs report drift or missing work but do not mutate state.

## Cursor model overview

Cursors are monotonic metadata markers. They should be treated as separate
state surfaces:

- Archive cursor answers: "What source range is safely archived?"
- Review cursor answers: "What source range has safe metadata-only review?"
- Recovery checkpoint answers: "What source range is safe to rely on for
  recovery?"

A recovery checkpoint should not imply raw content is present in the kit. It only
means the shareable metadata surfaces are internally consistent up to a
placeholder cursor.

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

- It may inspect safe summaries, counts, date ranges, and manifest status.
- It must not print or persist raw transcript content.
- It must not print or persist decrypted archive content.
- It must produce safe summaries, anomaly notes, and cursor recommendations.
- It advances the review cursor only through an explicit gate.

## Recovery checkpoint alignment

A checkpoint is aligned when:

- Archive coverage is present through `<CHECKPOINT_CURSOR>`.
- Review coverage is present through `<CHECKPOINT_CURSOR>`.
- Manifest and monthly index validation are clean.
- Protected files and private data boundaries remain unchanged.
- The checkpoint is updated only after explicit approval.

## Cron dry-run role

Cron dry-runs are observers, not mutators. A dry-run job may report:

- Latest placeholder cursor status.
- Missing manifest/index coverage.
- Gap or overlap indicators.
- Whether manual approval is required.

A dry-run job must not:

- Create archives.
- Decrypt archives.
- Move cursors.
- Commit or push.
- Change cron definitions.
- Print raw/private content.

## Data classification boundaries

Use three broad classes:

- **Public/shareable metadata:** generic documentation, placeholder schemas,
  safety booleans, and redaction rules.
- **Private metadata:** local paths, real identifiers, real cursor values, real
  repository names, real commit hashes, real job IDs, and real artifact names.
- **Private content:** raw messages, transcripts, decrypted archives, secrets,
  private keys, cookies, and database plaintext.

Only public/shareable metadata belongs in this kit.

## Sibling repository boundary

Sibling repositories must be treated as generic read-only boundaries in shareable
material. A kit may state that an adjacent or sibling repository is read-only,
but must not include its private paths, identifiers, internal files, secrets, or
content. Any cross-repository recommendation should be represented as generic
policy, not as environment-specific instructions.

## Safe adoption pattern

A safe adopter should:

1. Copy the generic docs and templates.
2. Replace placeholders only in a private repository or local secure location.
3. Keep raw/private data outside the shareable kit.
4. Validate Markdown and YAML structure.
5. Run private metadata and secret scans before commit.
6. Use explicit approval gates for staging, commit, push, archive creation,
   cursor movement, and cron changes.
