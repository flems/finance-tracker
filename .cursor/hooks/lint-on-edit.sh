#!/usr/bin/env bash
set -euo pipefail

input=$(cat)
file=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty')

[[ -z "$file" ]] && exit 0

case "$file" in
  *.ts|*.vue)
    cd /Users/borisov_sv/pet/finance/frontend
    npx eslint --fix "$file" 2>/dev/null || true
    npx prettier --write "$file" 2>/dev/null || true
    ;;
  *.py)
    python3 -m ruff check --fix "$file" 2>/dev/null || true
    python3 -m ruff format "$file" 2>/dev/null || true
    ;;
esac

exit 0
