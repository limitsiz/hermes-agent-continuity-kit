# Shareable HermesAgent Continuity Kit

A generic, shareable operating model for preserving assistant continuity without exposing private transcripts, credentials, or environment-specific metadata.

## What this kit provides

- A two-cursor model for encrypted archive coverage and high-signal review coverage.
- A recovery checkpoint model that advances only after archive and review coverage align.
- A report-only cron dry-run pattern for safe automation preflight.
- A manual gated archive workflow for encrypted backups.
- Validation checklists and safety boundaries for pre-commit and post-flight checks.

## What this kit does not contain

This shareable kit must not include private repo paths, real commit hashes, real message identifiers, real message ranges, real cron job identifiers, real database paths, platform exports, raw transcript text, decrypted archive content, or secrets.

Use placeholders such as `<CONFIG_REPO>`, `<ARCHIVE_CURSOR_ID>`, `<REVIEW_CURSOR_ID>`, `<ARCHIVE_COMMIT_SHA>`, `<CRON_JOB_ID>`, and `<HERMES_STATE_DB>`.

## Suggested adoption paths

For step-by-step adoption into another repository or installation, see
`ADOPTION_GUIDE.md`. Keep this directory shareable-only: replace placeholders
only inside private/local instantiated copies, never in public templates.

### Fresh install

Start with empty cursor templates, choose an archive recipient, and begin from a declared checkpoint such as `<START_FROM_NOW_CURSOR_ID>`.

### Existing adoption

Perform a metadata-only inventory first. Do not import raw transcripts into shareable documentation. Lock a starting cursor, document the boundary, and proceed through the manual gated workflow.

### Legacy recovery

If historical archives already exist, verify them by metadata only: encrypted artifact presence, size, checksum, manifest/index linkage, and cursor consistency. Do not decrypt during shareable-kit validation.

## File map

- `ADOPTION_GUIDE.md`: safe copy, private instantiation, and adoption validation guide.
- `ARCHITECTURE.md`: component model and data classification boundaries.
- `CURSOR_MODEL.md`: archive cursor vs review/audit cursor semantics.
- `ARCHIVE_WORKFLOW.md`: manual gated encrypted archive workflow.
- `REVIEW_WORKFLOW.md`: metadata-only review and safe-summary workflow.
- `CRON_DRY_RUNS.md`: report-only metadata-only cron pattern.
- `RECOVERY_CHECKPOINTS.md`: recovery checkpoint model.
- `SAFETY_BOUNDARIES.md`: private/shareable split and forbidden content.
- `VALIDATION_CHECKLIST.md`: validation checklist.
- `templates/last_archive_cursor.yaml`: archive cursor state template.
- `templates/last_scan_cursor.yaml`: review/audit cursor state template.
- `templates/recovery-current-state.yaml`: recovery checkpoint state template.
- `templates/archive-manifest.yaml`: archive batch manifest template.
- `templates/monthly-index.yaml`: monthly archive index template.
