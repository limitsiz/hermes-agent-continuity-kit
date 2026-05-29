# Conversation Source Policy

Conversation/source handling is metadata-first. Public kit outputs may describe
source classes, counts, ranges, and validation results, but must not include raw
source content.

## Allowed metadata classes

- Source type
- Count
- Placeholder range
- Placeholder timestamp range
- Validation status
- Safety booleans

## Forbidden public output

- Raw message/source text
- Platform plaintext exports
- Tool payload/body/result plaintext
- Decrypted archive content
- Secrets, tokens, passwords, cookies, auth material, or private keys
- Real private runtime paths, real cursor/message identifiers, or real archive paths
