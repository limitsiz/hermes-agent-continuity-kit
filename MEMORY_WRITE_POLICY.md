# Memory Write Policy

This policy defines where approved memory-audit findings should go. It keeps
persistent memory, safe-summary files, project state, decision logs, Knowledge Workspace Adapter surfaces, or
other note systems, and encrypted archives from being treated as the same layer.

## What belongs in Hermes persistent memory

Write only compact durable facts that will remain useful across future sessions,
such as:

- Stable user preferences.
- Stable environment facts.
- Reusable workflow lessons.
- Durable corrections to assistant behavior.

Do not write temporary task progress, raw transcripts, secrets, private keys,
credential material, cache contents, large logs, or stale operational artifacts.

## What belongs in safe-summary files

Safe-summary files hold human-readable state and policy summaries, such as:

- Current continuity status.
- Active gates.
- Cursor semantics.
- Durable decisions.
- Archive/review/recovery workflow notes.

They may contain safe private metadata in a private instance, but public kit
files must use placeholders.

## What belongs in active project state

Active project state should track current work, next gates, blockers, risks, and
pending approvals. It should avoid raw/private content and should not duplicate
archive manifests or indexes.

## What belongs in the decision log

The decision log should record durable decisions and rationale. It should not log
every operational step, raw evidence, or private transcript content.

## What belongs in notes systems

A Knowledge Workspace Adapter can provide an optional long-form knowledge surface. Obsidian-compatible workspaces are only optional adapter examples and are not part of the product identity.
It is not the canonical Hermes persistent memory layer, not the archive, and not
the cursor source of truth unless a private installation explicitly defines that
role.

## What belongs in encrypted archive

Encrypted archive is a raw backup and last-resort recovery/context source. It is
not primary memory and must not be represented as plaintext in public docs.
Archive validation should rely on encrypted artifact metadata unless a separate
private decrypt gate is approved.

## What must never be written

Never write the following to public/shareable docs or unencrypted summaries:

- Raw transcript or message body content.
- Platform plaintext exports.
- Session database plaintext.
- Decrypted archive content.
- Secrets, tokens, passwords, cookies, `.env` values, auth material, or private
  key material.
- Real private paths, commit hashes, cursor IDs, message IDs, ranges, artifact
  paths, cron job IDs, or operator-specific identity details.

## Approval model

Memory writes should follow candidate report + explicit approval:

1. Produce candidate findings.
2. Propose target surfaces.
3. Ask for approval.
4. Apply only approved writes.
5. Validate changed files and protected boundaries.
6. Use separate approvals for staging, commit, push, cursor movement, archive
   production, or recovery refresh.

## Validation after writes

After approved writes, check exact changed files, run `git diff --check`, scan
for strong secret/raw/decrypted markers, verify protected files remain unchanged,
and use scoped `git add --dry-run` before any staging request.

## Memory Router

The Memory Router classifies candidate updates as durable memory, stale-memory
correction, Audit Ledger entry, Knowledge Workspace Adapter note, or no-action.
It must not write public or private state unless the active approval profile
explicitly allows the target path and the required validation passes.
