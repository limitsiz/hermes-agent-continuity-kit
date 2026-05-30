# Adoption Guide

This guide explains how to copy and apply the Shareable Hermes Agent Continuity
Kit in another repository or installation without exposing private metadata,
raw transcripts, decrypted archives, or secrets.

## Purpose

Use this guide when adopting the kit into a new or existing environment. The
shareable kit should remain generic: documentation and templates use placeholders
only, while installation-specific values belong in a private copy or secure local
state.

## Safe copy model

Adoption has three stages:

1. **Copy shareable files as-is.** Copy the kit documentation and templates while
   preserving placeholder values.
2. **Instantiate templates privately.** Create private/local copies for actual
   operational state. Replace placeholders only in those private copies.
3. **Validate before commit.** Run structural, placeholder, redaction, and scoped
   git checks before staging or publishing any adoption changes.

Do not copy raw transcript content, decrypted archive content, local database
plaintext, credentials, or private identifiers into the shareable kit.

## Files to copy as-is

Copy these files as shareable documentation:

- `README.md`
- `ARCHITECTURE.md`
- `CURSOR_MODEL.md`
- `ARCHIVE_WORKFLOW.md`
- `REVIEW_WORKFLOW.md`
- `CRON_DRY_RUNS.md`
- `RECOVERY_CHECKPOINTS.md`
- `SAFETY_BOUNDARIES.md`
- `VALIDATION_CHECKLIST.md`

Copy these files as shareable templates and keep their placeholders intact:

- `templates/last_archive_cursor.yaml`
- `templates/last_scan_cursor.yaml`
- `templates/recovery-current-state.yaml`
- `templates/archive-manifest.yaml`
- `templates/monthly-index.yaml`

## Templates to instantiate privately

Instantiate templates only in a private repository, secure local state directory,
or another non-shareable location. Recommended private instantiation order:

1. `templates/last_archive_cursor.yaml`
2. `templates/last_scan_cursor.yaml`
3. `templates/recovery-current-state.yaml`
4. `templates/archive-manifest.yaml`
5. `templates/monthly-index.yaml`

The shareable template files should remain examples. Do not replace their
placeholder values with environment-specific values.

## Placeholder replacement rules

Use angle-bracket placeholders in shareable files:

- `<START_CURSOR>`
- `<END_CURSOR>`
- `<ARCHIVE_BATCH_ID>`
- `<MANIFEST_PLACEHOLDER_REF>`
- `<VERIFICATION_STATUS>`
- `<REVIEW_STATUS>`

Avoid mixed placeholder styles such as double-curly placeholders, uppercase
change-or-replace sentinel words, or fake-looking real values.

Replace placeholders only after copying a template into a private adoption
location. If a value would reveal a private path, real identifier, secret, raw
content, or decrypted content, it does not belong in shareable documentation.

## Private metadata boundaries

Never include these in the shareable kit:

- Private repository paths or local absolute paths.
- Real commit hashes.
- Real message identifiers or message ranges.
- Real cron job identifiers.
- Real database paths.
- Real artifact, manifest, export, index, or identity paths.
- Messaging platform plaintext or platform export details.
- Raw transcript or message body content.
- Hermes database or session plaintext.
- Decrypted archive content.
- Secret, token, password, auth, cookie, `.env`, or private-key values.

Safe shareable content includes generic workflow descriptions, placeholder
schemas, safety booleans, validation checklists, and synthetic examples that do
not resemble real private values.

## First-time setup checklist

Use this checklist for a new installation:

- [ ] Copy the shareable kit files as-is.
- [ ] Keep all shareable templates placeholder-only.
- [ ] Decide where private instantiated templates will live.
- [ ] Create private copies of cursor, recovery, manifest, and index templates.
- [ ] Replace placeholders only in private copies.
- [ ] Define archive, review, and recovery checkpoint gates.
- [ ] Keep cron jobs report-only until separately approved.
- [ ] Run Markdown, YAML, placeholder, redaction, and scoped git checks.
- [ ] Require explicit approval before staging, commit, push, cursor movement,
      archive production, archive decryption, or cron changes.

## Existing installation checklist

Use this checklist when adopting the kit into an existing environment:

- [ ] Perform a metadata-only inventory first.
- [ ] Do not import raw transcripts into shareable documentation.
- [ ] Map existing archive cursor, review cursor, and recovery checkpoint state
      into private template copies.
- [ ] Check for gaps, overlaps, and cursor alignment using metadata only.
- [ ] Keep existing archive artifacts outside the shareable kit.
- [ ] Record only placeholder references in shareable templates.
- [ ] Run redaction validation before any commit.
- [ ] Treat any cursor advancement as a separate approval gate.

## Validation before commit

Before staging or publishing adoption changes:

```bash
git diff --check -- <EXPECTED_FILES>
git add --dry-run -- <EXPECTED_FILES>
```

Then verify:

- Markdown headings exist and fenced code blocks are balanced.
- YAML templates parse successfully.
- Placeholder style is consistent.
- No private metadata or private paths are present.
- No raw transcript, platform plaintext, database plaintext, decrypted archive
  content, secrets, auth material, cookies, or private keys are present.
- `git status --short` contains only approved files.
- Protected cursor, archive, recovery, and cron surfaces are unchanged unless
  explicitly approved.

## Common mistakes

- Replacing placeholders directly inside the shareable kit.
- Using fake-looking hashes, IDs, or paths that resemble real private metadata.
- Treating archive cursor and review cursor as the same state.
- Advancing recovery checkpoint before archive and review coverage align.
- Allowing report-only cron dry-runs to write files or move cursors.
- Adding raw transcript snippets to explain examples.
- Committing private instantiated templates to a public or shareable location.

## Do-not-proceed conditions

Stop and request a new approval if any of these occur:

- A file contains raw/private/decrypted/secret content.
- A template contains real environment-specific identifiers.
- `git add --dry-run` includes unexpected files.
- Markdown or YAML structural checks fail.
- Cursor, archive, recovery, or cron files changed outside the approved scope.
- A sibling repository boundary requires environment-specific details.
- Archive production, archive decryption, cron changes, commit, push, or cursor
  movement is needed.

## Generic sibling repository boundary

Sibling repositories should be described only as generic read-only boundaries in
shareable material. Do not include their private paths, identifiers, internal
configuration, secrets, raw content, or operational state. If an adoption needs a
cross-repository recommendation, write it as generic policy and keep any
installation-specific details in private state.

## Canonical adoption profiles

Use only the canonical approval profiles in public docs:

- `report-only`
- `docs-batch`
- `safe-local-setup`
- `archive-batch-local`
- `maintainer-guarded`

Stop immediately if adoption requires raw source content, decrypted archive
content, private keys, real cursor/message identifiers, real archive paths, or
private runtime state.


## Runtime adoption path

Use `installer/install.sh` for a local runtime skeleton, validate it with `bin/hck-validate-runtime`, then keep memory audit report-only and archive actions dry-run until a separate approval changes the operating mode.
