#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

OUTPUT_DIR="${REPO_ROOT}/test_artifacts/enterprise-smoke/$(date +%Y%m%d-%H%M%S)"
mkdir -p "${OUTPUT_DIR}"

echo "Run enterprise smoke pipeline"
bash "${REPO_ROOT}/scripts/phase2_v2_pipeline.sh" \
  --base-url http://localhost:8080 \
  --image-tag label-studio:enterprise-smoke-local \
  --output-dir "${OUTPUT_DIR}"

bash "${REPO_ROOT}/scripts/enterprise/check_enterprise_health.sh" "http://localhost:8080"

echo "Enterprise smoke finished. Artifacts: ${OUTPUT_DIR}"
