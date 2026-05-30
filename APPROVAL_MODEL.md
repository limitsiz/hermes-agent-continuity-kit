# Approval Model

The Approval Kernel is the safety boundary for the Hermes Agent Continuity Kit.
It converts a user approval into a bounded operation with an explicit profile,
allowlist, hard stops, validations, and receipt.

## Canonical profiles

- `report-only`
- `docs-batch`
- `safe-local-setup`
- `archive-batch-local`
- `maintainer-guarded`

## Approval receipt fields

Receipts should include profile, scope, allowed paths, forbidden paths, files
changed, protected-file status, raw/decrypted/secret safety booleans, staging,
commit, push, cursor movement, archive creation, validation results, and the
next required approval.

## Human approval boundaries

A docs update does not authorize staging. A staging approval does not authorize a
commit. A commit approval does not authorize a push. A push approval does not
authorize public visibility changes, cursor movement, archive decrypt/restore,
cron changes, or recovery refresh.


## Runtime approval boundary

Runtime commands inherit the Approval Kernel boundary: archive production, cursor advancement, decrypt operations, and scheduler enablement are not default install actions and require separate approval.
