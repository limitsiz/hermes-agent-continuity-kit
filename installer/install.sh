#!/usr/bin/env sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec python3 -B "$SCRIPT_DIR/hermes_continuity_installer.py" "$@"
