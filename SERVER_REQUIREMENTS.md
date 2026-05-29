# Server Requirements

The public kit assumes a clean server or workstation with standard filesystem
access and Git. Optional archive workflows may require compression, encryption,
and checksum tools selected by the maintainer.

## Required for docs validation

- Git
- A shell or equivalent command runner
- A Markdown-capable editor/viewer
- YAML parser for template validation

## Optional for archive workflows

- tar-compatible archiver
- zstd-compatible compressor
- age-compatible encryption tool
- SHA-256 checksum tool

## Public boundary

The public kit must not require secrets, private keys, local database access,
raw source content, decrypted archive content, private runtime state, or real
operator-specific identifiers.
