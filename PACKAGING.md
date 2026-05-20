# Packaging and Release Boundary

## Purpose

This document defines the safe packaging and release boundary for the Shareable
HermesAgent Continuity Kit. It explains which generic documentation and template
files may be exported, which private-state surfaces must be excluded, and which
validation gates must pass before a package is copied to another repository,
server, or installation.

The packaging boundary is documentation-only unless a separate approval explicitly
authorizes an export artifact. Do not create archives, move cursors, update cron
jobs, or instantiate private templates as part of this packaging policy.

## Packaging decision

The shareable kit may be packaged only from an explicit include allowlist. The
allowlist is the source of truth. Exclude patterns are a safety net, not the
primary selection mechanism.

Default decision:

- Keep the kit as ordinary repository files under `docs/continuity-kit/`.
- Do not create a zip or tar artifact by default.
- Use dry-run package listing and validation before any future artifact creation.
- Require a separate approval for any real export artifact, checksum file, or
  release manifest.

## Shareable package scope

The package scope is limited to generic documentation and placeholder-only
templates. The package must describe workflows, data boundaries, cursor models,
archive policies, recovery checkpoint rules, validation gates, and adoption
steps without including installation-specific operational state.

Allowed content categories:

- Generic workflow documentation.
- Placeholder-only YAML templates.
- Synthetic examples that cannot be mistaken for real private values.
- Safety checklists and approval gates.
- Generic read-only boundary language for sibling repositories.

Disallowed content categories:

- Private state.
- Operational cursor state.
- Recovery checkpoint state from a real installation.
- Archive artifacts or archive indexes from a real installation.
- Raw transcript, platform plaintext, database plaintext, decrypted content, or
  secret material.

## Include allowlist

Only these shareable files are eligible for a package:

```text
docs/continuity-kit/ADOPTION_GUIDE.md
docs/continuity-kit/ARCHITECTURE.md
docs/continuity-kit/ARCHIVE_WORKFLOW.md
docs/continuity-kit/CRON_DRY_RUNS.md
docs/continuity-kit/CURSOR_MODEL.md
docs/continuity-kit/PACKAGING.md
docs/continuity-kit/README.md
docs/continuity-kit/RECOVERY_CHECKPOINTS.md
docs/continuity-kit/REVIEW_WORKFLOW.md
docs/continuity-kit/SAFETY_BOUNDARIES.md
docs/continuity-kit/VALIDATION_CHECKLIST.md
docs/continuity-kit/templates/archive-manifest.yaml
docs/continuity-kit/templates/last_archive_cursor.yaml
docs/continuity-kit/templates/last_scan_cursor.yaml
docs/continuity-kit/templates/monthly-index.yaml
docs/continuity-kit/templates/recovery-current-state.yaml
```

If this list changes, update the package validation checklist and re-run scoped
pre-release validation before staging or publishing the change.

## Exclude denylist

The following categories must never be included in a shareable package:

```text
memory/
recovery/
archive/
archives/
.hermes/
.env
*.env
*.db
*.sqlite
*.sqlite3
*.age
*.key
*.pem
*.p12
*.pfx
*.cookie
*cookies*
*session*
*telegram*
*export*
```

Also exclude any private instantiated template, local operational state,
credential store, shell history, cache, temporary file, decrypted artifact, raw
message export, or platform-specific plaintext export.

## Private-state exclusion rules

Packaging must follow these rules:

1. Start from the include allowlist, not from a broad directory glob.
2. Treat the exclude denylist as a second safety check.
3. Keep public templates placeholder-only.
4. Put installation-specific values only in private/local instantiated copies.
5. Do not include private repository paths, local absolute paths, real commit
   hashes, real message identifiers, real message ranges, real cron job
   identifiers, real database paths, or private archive details.
6. Do not include raw transcript content, platform plaintext, Hermes database
   plaintext, session plaintext, decrypted archive content, secrets, tokens,
   passwords, auth values, cookies, `.env` values, or private-key material.
7. Keep sibling repository references generic and read-only.
8. Stop if a package candidate contains any non-shareable state.

## Placeholder and redaction requirements

Use angle-bracket placeholders for generic values:

```text
<PACKAGE_VERSION>
<PACKAGE_CREATED_AT>
<EXPECTED_FILE_COUNT>
<CHECKSUM_ALGORITHM>
<VALIDATION_STATUS>
```

Placeholder rules:

- Use one placeholder style consistently.
- Do not use fake-looking hashes, identifiers, ranges, paths, job IDs, database
  paths, or platform export names.
- Do not include realistic secrets, tokens, cookies, private keys, or decrypted
  content as examples.
- Redaction is not a substitute for exclusion; private content should not enter
  the package candidate at all.

## Optional package layout

If a future approval authorizes a package artifact, the recommended internal
layout is:

```text
continuity-kit/
  README.md
  ADOPTION_GUIDE.md
  ARCHITECTURE.md
  ARCHIVE_WORKFLOW.md
  CRON_DRY_RUNS.md
  CURSOR_MODEL.md
  PACKAGING.md
  RECOVERY_CHECKPOINTS.md
  REVIEW_WORKFLOW.md
  SAFETY_BOUNDARIES.md
  VALIDATION_CHECKLIST.md
  templates/
    archive-manifest.yaml
    last_archive_cursor.yaml
    last_scan_cursor.yaml
    monthly-index.yaml
    recovery-current-state.yaml
```

The package root should not contain repository-private state directories or
installation-specific files.

## Optional manifest model

A future release manifest may be generated only after separate approval. If used,
it should contain generic package metadata and file inventory only:

```yaml
package_name: hermesagent-continuity-kit
package_version: <PACKAGE_VERSION>
created_at: <PACKAGE_CREATED_AT>
expected_file_count: <EXPECTED_FILE_COUNT>
validation_status: <VALIDATION_STATUS>
files:
  - path: continuity-kit/README.md
    sha256: <SHA256_PLACEHOLDER>
```

Manifest rules:

- Do not include private source repository paths.
- Do not include real operational cursor values.
- Do not include archive artifact locations.
- Do not include platform export details.
- Do not include hostnames, user names, chat identifiers, or database paths.

## Optional checksum model

A future checksum file may be generated only after separate approval. If used,
the checksum model should:

- Hash only approved package files.
- Use a standard algorithm such as SHA-256.
- Record package-relative paths only.
- Be generated after the package content has passed pre-release validation.
- Be verified against the package artifact before adoption dry-run begins.

Checksum records must not contain private source paths or operational metadata.

## Dry-run export procedure

Before any real export artifact is created, perform a dry-run procedure:

1. Confirm the repository is clean or contains only explicitly approved packaging
   documentation changes.
2. Build the candidate file list from the include allowlist.
3. Confirm the candidate file count matches the expected count.
4. Confirm no excluded path category is present in the candidate list.
5. Run Markdown structural checks.
6. Run YAML template parse checks.
7. Run placeholder consistency checks.
8. Run private metadata scans.
9. Run raw, secret, private-key, and decrypted-content marker scans.
10. Confirm sibling repository references are generic read-only boundaries.
11. Run scoped `git diff --check` for changed packaging docs.
12. Run scoped `git add --dry-run` only if staging is being considered.

The dry-run should report booleans, counts, and file names only. It must not print
raw transcript content, platform plaintext, database plaintext, secret values,
private-key material, or decrypted content.

## Pre-release validation checklist

A package candidate is release-ready only when all checks pass:

- [ ] Candidate files match the include allowlist.
- [ ] No excluded path category is present.
- [ ] Markdown headings exist and fenced code blocks are balanced.
- [ ] YAML templates parse successfully.
- [ ] Placeholder style is consistent.
- [ ] No private metadata is present.
- [ ] No raw transcript, platform plaintext, database plaintext, decrypted
      content, secret, token, auth, cookie, `.env`, or private-key value is
      present.
- [ ] Sibling repository references are generic read-only boundaries.
- [ ] Protected cursor, recovery, archive, and cron surfaces are unchanged.
- [ ] Any manifest or checksum file was separately approved.
- [ ] Any real package artifact was separately approved.

## New server adoption dry-run prerequisites

Before copying the kit to a new server or installation:

- Confirm the source kit passed pre-release validation.
- Copy only the approved package files.
- Keep public templates placeholder-only.
- Instantiate templates only in private/local state on the target installation.
- Run target-side Markdown and YAML checks.
- Run target-side placeholder and redaction checks.
- Confirm no target private state is copied back into the shareable kit.
- Keep cron jobs report-only until separately approved.
- Treat cursor movement, archive production, archive decryption, and commit/push
  actions as separate approval gates.

## Do-not-proceed conditions

Stop and request a new approval if any of these occur:

- The candidate includes a file outside the include allowlist.
- The candidate includes a denied private-state path category.
- A template contains installation-specific values.
- A file contains private metadata, raw content, decrypted content, or secret
  material.
- A sibling repository boundary requires installation-specific details.
- Cursor, recovery, archive, or cron state changed unexpectedly.
- A real zip, tar, manifest, checksum, release, commit, or push is needed.

## Approval gates

Separate explicit approvals are required for:

- Creating or modifying `PACKAGING.md`.
- Staging packaging documentation.
- Committing packaging documentation.
- Pushing packaging documentation.
- Generating a package file list outside documentation.
- Creating a real zip or tar artifact.
- Creating a release manifest.
- Creating checksum files.
- Copying the package to another server or repository.
- Instantiating templates with private values.
- Changing cron jobs.
- Moving cursors.
- Producing or decrypting archives.

## Non-goals

This packaging boundary does not:

- Create a release artifact by itself.
- Define private operational state for a real installation.
- Replace the adoption guide.
- Replace recovery runbooks.
- Replace archive workflow documentation.
- Authorize cron changes.
- Authorize cursor movement.
- Authorize archive production or archive decryption.
- Authorize staging, commit, or push.
