# Release Test Harness

## Purpose

The Release Test Harness verifies that the Hermes Agent Continuity Kit is safe to package, clone, and review as a public-readiness release candidate.

It is designed to be read-only, dependency-free, and safe for disposable clean-server validation.

## Non-goals

The harness does not:

- Create archives or decrypt archives.
- Advance cursors.
- Read databases, sessions, raw transcripts, or message bodies.
- Read private runtime state.
- Install dependencies.
- Modify the git index, create commits, or push.
- Change remotes, visibility, deploy keys, services, gateway, or cron.

## Safety model

The validator inspects only the public documentation, template, and validation
surface. In the private/source repository this surface may live under
`docs/continuity-kit/`; in the public release repository it uses the root layout
(`README.md`, `scripts/`, `templates/`, and sibling public docs). It reports
sanitized findings with check names, file paths, and short summaries. It must not
print raw, secret, decrypted, or private runtime values.

Policy examples may mention forbidden classes such as environment files, cookies, passwords, raw transcripts, decrypted archives, or private keys. Those terms are allowed when used as safety rules. Actual assignments, key blocks, private paths, raw payloads, decrypted content, or runtime identifiers are failures.

## Checks

The harness checks:

- Repository state and optional clean/origin alignment.
- Public docs/templates inventory.
- Product name and naming debt.
- Public vocabulary: Continuity Engine, Memory Router, Audit Ledger, Encrypted Archive Pipeline, Recovery Workbench, Knowledge Workspace Adapter, Approval Kernel, Release Test Harness.
- Forbidden public identity markers.
- Public/private boundary markers.
- Secret/private marker patterns.
- Raw/decrypted content marker patterns.
- Template placeholder-only expectations.
- YAML structural validity with optional PyYAML and minimal fallback.
- Canonical approval profiles: report-only, docs-batch, safe-local-setup, archive-batch-local, maintainer-guarded.
- Knowledge Workspace Adapter product-agnostic wording.
- Clean-server readiness docs.
- Package/release boundary docs.

## Commands

For the public release repository root layout, run:

```bash
scripts/validate-public-readiness.sh --repo-root . --strict-release

scripts/validate-public-readiness.sh --repo-root . --strict-release --format json

python3 scripts/validate_public_readiness.py --repo-root . --strict-release
```

For a private/source repository that keeps the kit under `docs/continuity-kit/`,
use the same arguments with the source-layout script path, for example:

```bash
docs/continuity-kit/scripts/validate-public-readiness.sh --repo-root . --strict-release
```

## Output format

Text mode emits stable key/value lines:

```text
release_test_harness_result=pass
repo_state=pass
naming=pass
warnings=0
errors=0
```

JSON mode emits:

```json
{
  "result": "pass",
  "summary": {
    "warnings": 0,
    "errors": 0
  },
  "checks": {},
  "findings": []
}
```

Findings contain sanitized metadata only: severity, check, file, and summary.

## Exit codes

- `0`: pass
- `1`: validation fail
- `2`: usage/config error
- `3`: hard-stop/safety violation

## Clean-server RC1

RC1 confirms that a disposable node can clone the repository and run the validator without private state.

Acceptance criteria:

- Python 3 is available.
- No dependency install is required.
- The shell wrapper and Python validator run successfully.
- Required docs/templates are present.
- Naming, public vocabulary, boundary, marker, template, YAML, approval profile, adapter, clean-server readiness, and package boundary checks pass.
- Output is deterministic and sanitized.
- The validator writes no cache, log, or output files.

## Clean-server RC2

RC2 confirms reproducibility across another clean clone or environment.

Acceptance criteria:

- Same release candidate commit is checked out.
- Same validator command returns the same check matrix.
- JSON schema remains stable.
- No host-specific path or private state dependency appears.
- No repository files, generated caches, or git index entries are modified.

## Hard stops

Stop and fail if the validator detects actual private/runtime material, dangerous payloads, real instance identifiers, unexpected package files, or a non-read-only operation requirement. Stage, commit, push, cursor advancement, archive operations, DB/session reads, service changes, cron changes, and remote visibility/key changes are outside the harness.

## Approval receipt integration

Release validation reports should include whether files changed, whether protected files changed, whether raw/secret/decrypted content was printed, whether staging/commit/push occurred, whether cursor/archive work occurred, and the next required approval gate.
