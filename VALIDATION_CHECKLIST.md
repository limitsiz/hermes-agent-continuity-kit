# Validation Checklist

Use this checklist before staging or publishing Continuity Kit changes.

## Content safety

- [ ] No private repo paths.
- [ ] No real commit hashes.
- [ ] No real message ids or ranges.
- [ ] No real cron job ids.
- [ ] No real database, artifact, manifest, index, export, or identity paths.
- [ ] No raw transcript or platform plaintext.
- [ ] No session database plaintext.
- [ ] No decrypted archive content.
- [ ] No secret, token, auth, cookie, or private-key values.
- [ ] Placeholders are used consistently.
- [ ] Synthetic examples are labeled synthetic.

## Workflow correctness

- [ ] Archive cursor and review/audit cursor are described as separate.
- [ ] Recovery checkpoint advances only after both cursors align.
- [ ] Cron dry-run is report-only and metadata-only.
- [ ] Archive production is manual gated.
- [ ] Cursor advancement is a separate gate from archive commit/push.
- [ ] Validation precedes staging.

## Adoption checks

- [ ] Shareable kit files are copied as-is.
- [ ] Templates are instantiated only in private/local state.
- [ ] Placeholder replacement does not occur inside public/shareable templates.
- [ ] README file map lists all shareable docs and templates.
- [ ] Sibling repositories are represented only as generic read-only boundaries.

## Technical checks

```bash
git diff --check -- <EXPECTED_FILES>
git add --dry-run -- <EXPECTED_FILES>
```

Additional checks:

- Markdown headings present.
- Fenced code blocks balanced.
- YAML templates parse or pass structural checks.
- Strong marker scan for private key blocks, private identity strings, token assignments, raw content values, and decrypted content values.
- `git status --short` contains only approved files.
