#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8080}"

echo "Check: service health at ${BASE_URL}"

status_code="$(curl -s -o /tmp/ls_health_response.html -w '%{http_code}' "${BASE_URL}/user/login")"
if [[ "${status_code}" != "200" ]]; then
  echo "Login page health check failed, status=${status_code}" >&2
  exit 1
fi

if ! rg -q "登录|Label Studio" /tmp/ls_health_response.html; then
  echo "Login page content check failed" >&2
  exit 1
fi

echo "Enterprise health check passed"
