# Safe Summary Surfaces

Safe-summary surfaces are human-readable state files that preserve continuity
without exposing raw/private content. They are distinct from persistent memory,
Knowledge Workspace Adapter implementations, and encrypted archives.

## Memory summary

A memory summary records compact durable state and policy context. It should
state the current safe checkpoint, boundaries, and important durable facts using
safe metadata only.

Public kit examples must use placeholders such as `<SAFE_SUMMARY_FILE>` and
`<RECOVERY_CHECKPOINT_ID>`.

## Active projects

Active project state records current work, phase, blockers, pending approvals,
and next gates. It should be concise and should not include raw transcripts,
secrets, decrypted archive content, or large logs.

## Decision log

A decision log records durable decisions and rationale. It should contain one
clear entry per durable decision, not a transcript of operational steps.

## Daily memory audit

A daily memory audit surface records report-only audit status, candidate finding
classes, approval requirements, and cursor/baseline semantics. It should default
to candidate report + explicit approval, not auto-write.

## Archive dry-run docs

Archive dry-run docs explain report-only metadata checks. They may describe
status vocabulary and range-computation rules, but they must not create archives,
decrypt archives, advance cursors, or commit/push.

## Archive policy

Archive policy defines normative requirements: encrypted artifacts only,
metadata-only manifests/indexes, no plaintext raw transcript in public docs, and
separate gates for production, commit/push, and cursor advancement.

## Recovery docs

Recovery docs describe checkpoint and restore semantics. Private recovery state
may contain safe metadata in a private installation, but public kit files must
use placeholders and must not include private paths, keys, raw content, or
decrypted content.

## Avoiding duplication

Do not duplicate artifact hash/size tables, manifest inventories, or index
records in safe-summary prose. Keep detailed archive metadata in manifests and
indexes; keep prose surfaces focused on meaning, gates, and current state.

## Public/private boundary

Public kit safe-summary examples must remain generic. Private installations may
instantiate these surfaces with safe private metadata, but raw/private content
and secrets remain forbidden in plaintext summaries.

## Product-agnostic workspace boundary

Safe-summary surfaces are not raw source stores and are not tied to a specific
notes product. A Knowledge Workspace Adapter may publish approved summaries to a
filesystem, docs repo, local wiki, or optional Obsidian-compatible workspace.
