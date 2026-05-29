# Install Profiles

Install profiles describe safe adoption levels for the Hermes Agent Continuity
Kit. They do not change the canonical approval profile list.

## report-only adoption

Read public docs and run validation only. No files are instantiated.

## docs-only adoption

Copy public docs/templates into a planning workspace. Do not fill private values.

## safe local setup

Instantiate placeholder templates in a private/local location after approval.
Use synthetic or local-only values and keep secrets outside the kit.

## archive-local setup

Enable the Encrypted Archive Pipeline only after a separate archive approval.
Raw source material is encrypted and never printed.

## maintainer-guarded release setup

Maintainers validate public-readiness, clean-server behavior, package contents,
and release receipts before publishing.
