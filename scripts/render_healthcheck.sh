#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <frontend-url> <backend-url>" >&2
  exit 1
fi

FRONTEND_URL="${1%/}"
BACKEND_URL="${2%/}"

check_url() {
  local label="$1"
  local url="$2"

  echo "Checking ${label}: ${url}"
  curl -fsS "${url}" >/dev/null
}

check_url "backend health" "${BACKEND_URL}/health"
check_url "backend homepage payload" "${BACKEND_URL}/api/public/homepage"
check_url "backend artists payload" "${BACKEND_URL}/api/artists"
check_url "frontend home" "${FRONTEND_URL}/"
check_url "frontend login" "${FRONTEND_URL}/login"

echo "Render healthcheck completed successfully."