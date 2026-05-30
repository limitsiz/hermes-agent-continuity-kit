# Validation Checklist

Use this checklist before staging or publishing Continuity Kit changes.

## Content safety

- [ ] No private repo paths.
- [ ] No real commit hashes.
- [ ] No real message IDs or ranges.
- [ ] No real cursor IDs in public/shareable docs.
- [ ] No real cron job IDs.
- [ ] No real database, artifact, manifest, index, export, or identity paths.
- [ ] No raw transcript or platform plaintext.
- [ ] No session database plaintext.
- [ ] No decrypted archive content.
- [ ] No secret, token, auth, cookie, `.env`, password, or private-key values.
- [ ] No operator-specific identity details.
- [ ] Placeholders are used consistently.
- [ ] Synthetic examples are labeled synthetic.

## Public/private boundary

- [ ] Public Kit content is limited to generic docs, templates, workflows, and
      validation rules.
- [ ] Private State values are represented only with placeholders.
- [ ] Private Ops are described as gated workflows, not bundled as runnable
      private-state scripts.
- [ ] The kit is not described as a role-specific operator identity system.
- [ ] The kit is described as continuity / memory audit / encrypted archive /
      recovery infrastructure.

## Workflow correctness

- [ ] Archive cursor and review/audit cursor are described as separate.
- [ ] Recovery checkpoint advances only after intended cursor alignment and a
      separate approval gate.
- [ ] Memory audit defaults to candidate report + explicit approval.
- [ ] Memory audit does not auto-write by default.
- [ ] Hermes persistent memory, safe-summary surfaces, and encrypted archive are
      described as distinct layers.
- [ ] Cron dry-run is report-only and metadata-only.
- [ ] Archive production is manual gated.
- [ ] Cursor advancement is a separate gate from archive commit/push.
- [ ] Recovery/decrypt is a separate private gate.
- [ ] Validation precedes staging.

## Cursor reconciliation checks

- [ ] Archive cursor answers encrypted backup coverage only.
- [ ] Review/audit cursor answers high-signal safe-summary coverage only.
- [ ] Archive candidate ranges are computed from archive cursor only.
- [ ] Review/audit cursor references do not affect archive candidate ranges.
- [ ] If cursors are reconciled at a checkpoint, no duplicate review cursor
      advancement is planned for that checkpoint.

## Adoption checks

- [ ] Shareable kit files are copied as-is.
- [ ] Templates are instantiated only in private/local state.
- [ ] Placeholder replacement does not occur inside public/shareable templates.
- [ ] README file map lists all shareable docs and templates.
- [ ] Sibling repositories are represented only as generic read-only boundaries.

## Expected files exact match

Before staging, compare changed files against the approved expected file list.
No cursor files, archive artifacts, recovery private state, cron files, gateway
config, remotes, secrets, auth files, or private keys should appear unless a
separate approval explicitly includes them.

## Secret/raw marker scan

Scan changed files for strong indicators:

- Private key blocks or private identity strings.
- Token-like assignments or `.env`-style values.
- Raw transcript or message body excerpts.
- Platform plaintext exports.
- Session database plaintext.
- Decrypted archive content.
- Real private paths, real cursor IDs, real message ranges, real commit hashes,
  real cron job IDs, or real artifact paths in public kit files.

Policy text that says forbidden content must not be included is not itself a
leak. Treat it as a leak only when an actual private value appears.

## Technical checks

```bash
git status -sb
git diff --check -- <EXPECTED_FILES>
git add --dry-run -- <EXPECTED_FILES>
```

Additional checks:

- Markdown headings present.
- Fenced code blocks balanced.
- YAML templates parse or pass structural checks.
- Strong marker scan is clean.
- `git diff --name-only` exactly matches approved files.
- Protected files remain unchanged.

## Naming and positioning

- [ ] Product name is `Hermes Agent Continuity Kit`.
- [ ] No legacy joined product-name spelling remains.
- [ ] No public product identity depends on external named methods, retrieval acronyms,
      note-app brands, peer-agent brands, executive role labels, private operator
      identity material, or private team structure.
- [ ] Note-app brands appear only, if at all, as optional Knowledge Workspace
      Adapter examples.

## Automation readiness

- [ ] Canonical approval profiles are documented.
- [ ] Hard stops are documented.
- [ ] Approval receipt template exists.
- [ ] Release Test Harness validation plan exists.


## Runtime MVP validation

- [ ] Installer dry-run succeeds.
- [ ] Standard install creates the expected runtime skeleton.
- [ ] Runtime validation passes.
- [ ] Memory audit remains report-only.
- [ ] Archive pipeline remains dry-run.
- [ ] Recovery refresh does not decrypt.
