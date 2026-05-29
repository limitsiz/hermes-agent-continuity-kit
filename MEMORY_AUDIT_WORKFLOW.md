# Memory Audit Workflow

Memory audit is the process of finding durable high-signal information that may
need to be written to persistent memory or safe-summary surfaces. The default
mode is report-only: produce candidates first, then ask for explicit approval.

## Purpose

The audit protects continuity by detecting facts, decisions, project-state
changes, and workflow lessons that should survive context loss, migration, or
restore.

## Inputs

Allowed inputs depend on the private installation, but the shareable workflow
only describes safe classes:

- Cursor/baseline metadata.
- Safe summaries and decision logs.
- Manifest/index status.
- Prior approved memory summaries.
- Metadata-only counts or status labels.

Forbidden inputs for public output include raw transcript text, platform
plaintext, session database plaintext, decrypted archive content, secrets, and
private key material.

## Metadata-aware scanning

A memory audit should scan incrementally from `<REVIEW_CURSOR_ID>` or another
approved baseline. It should record what range was considered using placeholders
in public material and private safe metadata in private instances.

## High-signal candidate classes

Candidate classes include:

- Durable user preference.
- Stable environment or repository convention.
- Active project state.
- Durable decision.
- Reusable workflow lesson.
- Safety or boundary correction.
- No-op / do-not-save item.

## Candidate report format

A candidate report should include:

- `<AUDIT_SCOPE_ID>`
- `<BASELINE_CURSOR_ID>`
- `<CURRENT_CURSOR_ID>`
- Candidate summary.
- Proposed target surface.
- Approval status.
- Safety flags.

The report must not include raw message excerpts or private identifiers in
public/shareable files.

## Approval gate

Memory audit starts as candidate report + explicit approval. No persistent
memory, safe-summary, project-state, decision-log, or cursor write should occur
until the user approves the exact candidates and target surfaces.

## No auto-write default

The initial and safest default is no auto-write. Auto-write may be considered
only after a private installation defines narrow, low-risk classes and explicit
approval rules. The Public Kit does not prescribe auto-write.

## Approved write routing

Approved candidates may be routed to:

- Hermes persistent memory for durable future-useful facts.
- Safe-summary files for human-readable state.
- Active project state for current work and pending gates.
- Decision log for durable decisions and rationale.
- No-op when the candidate is temporary, sensitive, stale, or unsafe.

## Safety flags

Every report should state whether raw content, secrets, decrypted content,
private key material, cursor movement, file writes, cron changes, archive
creation, commit, or push occurred. A report-only audit should mark all mutation
flags false.

## Validation

Before applying approved writes, validate expected files, run a secret/raw marker
scan, check that protected files remain unchanged, and use scoped dry-run staging
where applicable. Staging, commit, push, cursor movement, archive production,
and recovery refresh each require separate gates.
