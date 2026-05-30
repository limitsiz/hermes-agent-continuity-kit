# Automation Policy

The Hermes Agent Continuity Kit uses automation only through explicit approval
profiles, path allowlists, hard stops, validations, and approval receipts.

## Canonical approval profiles

- `report-only`: inspect and report only; no writes.
- `docs-batch`: update allowlisted public docs/templates only; no stage/commit/push.
- `safe-local-setup`: instantiate placeholder templates in a private/local setup.
- `archive-batch-local`: create encrypted local archive artifacts and safe metadata.
- `maintainer-guarded`: maintainer-reviewed actions such as release, push, cursor movement, or visibility change.

Do not add new canonical profile names in public docs without a release decision.
Implementation-specific sub-modes may exist internally, but they are not public
profile names.

## Allowlist model

Every automation run declares allowed paths, forbidden paths, allowed operations,
required validations, and a receipt. If an operation needs a path outside the
allowlist, stop and request a new approval.

## Hard stops

Stop on raw source exposure, decrypted archive exposure, secret or private-key
material, unexpected file changes, protected path changes, dirty tree when clean
is required, stage/commit/push without approval, cursor movement, archive
creation, recovery refresh, service/cron changes, or remote visibility changes.

## Receipt requirement

Each run produces an approval receipt listing the active profile, scope, changed
files, validation status, safety booleans, and next required approval.


## Runtime automation defaults

The installable runtime MVP may create local placeholder directories and command wrappers. It must not enable cron or systemd production timers during default installation.
