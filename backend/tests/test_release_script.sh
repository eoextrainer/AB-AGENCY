#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
SCRIPT_PATH="${REPO_ROOT}/scripts/stable_release.sh"

bash -n "${SCRIPT_PATH}"

grep -q -- "--ci" "${SCRIPT_PATH}"
grep -q -- "--push-rollback" "${SCRIPT_PATH}"
grep -q -- "docs/releases" "${SCRIPT_PATH}"

echo "stable_release.sh passed static checks"