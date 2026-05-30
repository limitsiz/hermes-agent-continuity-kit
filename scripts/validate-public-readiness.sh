#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root=""
args=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo-root)
      [ "$#" -ge 2 ] || { echo "usage_error=--repo-root requires a value" >&2; exit 2; }
      repo_root="$2"
      args+=("$1" "$2")
      shift 2
      ;;
    *)
      args+=("$1")
      shift
      ;;
  esac
done

if [ -z "$repo_root" ]; then
  repo_root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null || true)"
  if [ -z "$repo_root" ]; then
    repo_root="$(CDPATH= cd -- "$script_dir/../../.." && pwd)"
  fi
  args=("--repo-root" "$repo_root" "${args[@]}")
fi

exec python3 "$script_dir/validate_public_readiness.py" "${args[@]}"
