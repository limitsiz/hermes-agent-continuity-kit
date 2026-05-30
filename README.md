# Hermes Agent Continuity Kit

A generic, shareable operating model for preserving assistant continuity without
exposing private transcripts, credentials, or environment-specific metadata.

## What this kit is

This kit is a continuity, memory audit, encrypted archive, and recovery blueprint.
It provides generic documentation, templates, workflows, and validation rules for
installations that need to preserve context across daily use, migration, restore,
or disaster recovery.

The kit helps an installation:

- Track encrypted archive coverage separately from high-signal review coverage.
- Detect durable memory candidates through metadata-aware audit workflows.
- Route approved findings to safe memory or summary surfaces.
- Keep raw history out of plaintext public repositories.
- Treat encrypted archives as last-resort recovery/context sources.
- Validate that public/shareable materials contain placeholders only.

## What this kit is not

This kit is not:

- An role-specific operator identity-definition system.
- A private state bundle.
- A raw transcript synchronization system.
- A decrypted archive repository.
- A memory auto-write engine.
- A replacement for explicit operator approval gates.

Public kit files must not contain private repo paths, real commit hashes, real
message identifiers, real message ranges, real cron job identifiers, real
database paths, platform exports, raw transcript text, decrypted archive content,
private keys, credentials, or operator-specific identity details.

## Public vs private boundary

Use three layers:

- **Public Kit:** generic docs, templates, workflows, validation checklists, and
  placeholder-only examples.
- **Private State:** real cursor values, manifests, indexes, checkpoints,
  reports, summaries, and local metadata for one installation.
- **Private Ops:** scanners, writers, archive producers, recovery/decrypt
  runners, handoff builders, cron changes, cursor movement, staging, commit, and
  push workflows.

Use placeholders such as `<PRIVATE_STATE_PATH>`, `<ARCHIVE_CURSOR_ID>`,
`<REVIEW_CURSOR_ID>`, `<RECOVERY_CHECKPOINT_ID>`, `<ARCHIVE_ARTIFACT_PATH>`, and
`<SAFE_SUMMARY_FILE>` in public/shareable material.

## Core workflows

- **Memory audit:** report-only candidate detection followed by explicit approval
  before any write.
- **Memory write routing:** approved candidates go to persistent memory,
  safe-summary files, active project state, decision logs, or no-op.
- **Encrypted archive:** raw history is backed up only as encrypted artifacts;
  manifests and indexes stay metadata-only.
- **Cursor reconciliation:** archive cursor, review/audit cursor, cron baseline,
  and recovery checkpoint are compared using metadata-only checks.
- **Recovery:** recovery checkpoint refresh and decrypt/restore actions remain
  separate private gates.

## File map

- `PUBLIC_PRIVATE_BOUNDARY.md`: public/private/private-ops split.
- `ARCHITECTURE.md`: component model and data classification boundaries.
- `CURSOR_MODEL.md`: archive cursor vs review/audit cursor semantics.
- `CURSOR_RECONCILIATION.md`: metadata-only reconciliation patterns.
- `MEMORY_AUDIT_WORKFLOW.md`: candidate report + approval audit model.
- `MEMORY_WRITE_POLICY.md`: target-surface policy for approved findings.
- `SAFE_SUMMARY_SURFACES.md`: roles of summary, project, decision, audit, archive,
  and recovery surfaces.
- `ARCHIVE_WORKFLOW.md`: manual gated encrypted archive workflow.
- `REVIEW_WORKFLOW.md`: metadata-only review and safe-summary workflow.
- `CRON_DRY_RUNS.md`: report-only metadata-only cron pattern.
- `RECOVERY_CHECKPOINTS.md`: recovery checkpoint model.
- `SAFETY_BOUNDARIES.md`: private/shareable split and forbidden content.
- `VALIDATION_CHECKLIST.md`: validation checklist.
- `ADOPTION_GUIDE.md`: safe copy, private instantiation, and adoption validation.
- `PACKAGING.md`: source-layout and publish-layout guidance.
- `templates/last_archive_cursor.yaml`: archive cursor state template.
- `templates/last_scan_cursor.yaml`: review/audit cursor state template.
- `templates/recovery-current-state.yaml`: recovery checkpoint state template.
- `templates/archive-manifest.yaml`: archive batch manifest template.
- `templates/monthly-index.yaml`: monthly archive index template.

## Suggested adoption paths

For step-by-step adoption into another repository or installation, see
`ADOPTION_GUIDE.md`. Keep this directory shareable-only: replace placeholders
only inside private/local instantiated copies, never in public templates.

## Public release quickstart

Clone the public release repository with unauthenticated HTTPS and validate the
root-layout public package before adapting it:

```bash
git clone https://github.com/limitsiz/hermes-agent-continuity-kit.git
cd hermes-agent-continuity-kit

scripts/validate-public-readiness.sh --repo-root . --strict-release
scripts/validate-public-readiness.sh --repo-root . --strict-release --format json
```

The current public release commit passed public HTTPS clean clone RC1 validation.
Version tags and GitHub Releases may be added later as optional future versioning
work; their absence is not a blocker for the current public RC1 release-ready
state.

### Fresh install

Start with empty cursor templates, choose a private archive recipient in a
private location, and begin from a declared placeholder checkpoint such as
`<START_FROM_NOW_CURSOR_ID>`.

### Existing adoption

Perform a metadata-only inventory first. Do not import raw transcripts into
shareable documentation. Lock a starting cursor, document the boundary with
placeholders, and proceed through the manual gated workflow.

### Legacy recovery

If historical archives already exist, verify them by metadata only: encrypted
artifact presence, size, checksum, manifest/index linkage, and cursor
consistency. Do not decrypt during shareable-kit validation.

## Public vocabulary

Use these names consistently in public docs and templates:

- Continuity Engine
- Memory Router
- Audit Ledger
- Encrypted Archive Pipeline
- Recovery Workbench
- Knowledge Workspace Adapter
- Approval Kernel
- Release Test Harness

## Automation-ready MVP surfaces

The automation-ready MVP is composed of public docs, placeholder-only templates,
and validation guidance. It does not include instantiated runtime state, raw
conversation content, decrypted archive content, secrets, private operator
identity material, peer-agent operations, or deployment-specific paths.

Recommended MVP docs:

- `AUTOMATION_POLICY.md`: automation profiles, allowlists, hard stops, and receipts.
- `APPROVAL_MODEL.md`: Approval Kernel and canonical approval profiles.
- `INSTALL_PROFILES.md`: safe adoption profiles.
- `SERVER_REQUIREMENTS.md`: clean-server assumptions.
- `BOOTSTRAP_RUNBOOK.md`: safe first-run sequence.
- `MEMORY_ROUTING_POLICY.md`: Memory Router policy.
- `CONVERSATION_SOURCE_POLICY.md`: safe source inventory policy.
- `KNOWLEDGE_WORKSPACE_ADAPTER.md`: product-agnostic workspace adapter.
- `OPTIONAL_CURATED_WIKI.md`: optional curated knowledge workspace model.
