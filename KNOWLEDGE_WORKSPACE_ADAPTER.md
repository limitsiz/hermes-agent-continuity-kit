# Knowledge Workspace Adapter

The Knowledge Workspace Adapter connects approved summaries to a user-selected
knowledge workspace. It is optional and product-agnostic.

## Adapter contract

- Read approved safe summaries when authorized.
- Write approved summaries only to allowlisted workspace paths.
- Keep raw source content out of workspace sync.
- Preserve public/private boundary metadata.
- Report validation results in an approval receipt.

## Adapter examples

- Filesystem Markdown workspace
- Documentation repository
- Local wiki
- Obsidian-compatible workspace as an optional adapter example

No adapter is part of the product identity. Retrieval discussions are optional
implementation details, not the public identity of the kit.
