# Memory Routing Policy

The Memory Router decides where candidate information belongs before any write
occurs.

## Routes

- Durable memory candidate
- Stale-memory correction
- Audit Ledger entry
- Knowledge Workspace Adapter note
- Safe-summary surface update
- No action

## Rules

Start with a candidate report. Do not write memory, docs, ledgers, or workspace
notes until an approval profile allows the target. Do not store raw source
content, decrypted archive content, secrets, private keys, or private runtime
state in public kit files.
