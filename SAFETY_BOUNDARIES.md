# Safety Boundaries

This kit is designed to be shareable. Keep private operating data out of it.

## Never include

- Private repo paths or remotes.
- Real commit hashes.
- Real message ids or ranges.
- Real artifact, manifest, index, database, or export paths.
- Cron job identifiers or delivery targets.
- Raw transcript or message content.
- Platform export plaintext.
- Session database plaintext.
- Reasoning, tool payload, system prompt, or handoff plaintext.
- Secret, token, API key, password, environment, auth, cookie, or private key values.
- Age private identity content.
- Decrypted archive content.
- Shell history or browser cookie values.

## Placeholder policy

Use placeholders consistently:

```yaml
config_repo: "<CONFIG_REPO>"
state_db: "<HERMES_STATE_DB>"
archive_cursor: "<ARCHIVE_CURSOR_ID>"
review_cursor: "<REVIEW_CURSOR_ID>"
range: "<START_ID>-<END_ID>"
commit: "<COMMIT_SHA>"
cron_job: "<CRON_JOB_ID>"
```

Synthetic examples are allowed only when explicitly marked synthetic.

## Sibling repository boundary

Sibling repositories or external config repos are out of scope by default. Treat them as read-only unless explicitly approved. Do not mix another project’s credentials, archives, recovery metadata, or private state into this Continuity Kit.
