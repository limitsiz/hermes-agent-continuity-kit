# Clean Server Test

A clean-server validation should clone the public repository, run the Release Test Harness, run `installer/install.sh --profile standard --target <TARGET> --dry-run --non-interactive`, perform a standard install into a disposable target, and execute `bin/hck-validate-runtime`.
