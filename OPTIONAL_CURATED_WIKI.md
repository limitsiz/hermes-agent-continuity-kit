# Optional Curated Wiki

A curated wiki is an optional Knowledge Workspace Adapter pattern. It publishes
approved summaries, decisions, runbooks, and glossary pages for human review.

## Rules

- Generate from approved summaries only.
- Do not sync raw source content.
- Do not include decrypted archive content.
- Do not include secrets or private-key material.
- Do not include private runtime state or real operator-specific identifiers.
- Keep the Continuity Engine and Audit Ledger as the source of approval state.

The curated wiki is not required for the core Hermes Agent Continuity Kit.
