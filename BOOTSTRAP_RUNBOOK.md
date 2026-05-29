# Bootstrap Runbook

This runbook describes a safe first-run sequence for the Hermes Agent Continuity
Kit.

1. Clone or copy the public kit.
2. Run public-readiness validation.
3. Select a canonical approval profile.
4. Review the public/private boundary.
5. Instantiate templates only in a private/local setup after approval.
6. Configure optional Knowledge Workspace Adapter behavior.
7. Run the Release Test Harness.
8. Produce an approval receipt for every gated operation.

Hard stop if any step requires raw source output, decrypted archive output,
secrets, private keys, real runtime paths, cursor movement, archive creation,
cron/service changes, or non-allowlisted file changes.
