#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BASE_URL="http://localhost:8080"
IMAGE_TAG="label-studio:phase2-v2-local"
HEADED_UI=false
OUTPUT_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url)
      BASE_URL="$2"
      shift 2
      ;;
    --image-tag)
      IMAGE_TAG="$2"
      shift 2
      ;;
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --headed-ui)
      HEADED_UI=true
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "${OUTPUT_DIR}" ]]; then
  OUTPUT_DIR="${REPO_ROOT}/test_artifacts/phase2-v2/$(date +%Y%m%d-%H%M%S)"
fi
mkdir -p "${OUTPUT_DIR}" "${OUTPUT_DIR}/ui"

if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
  PYTHON_BIN="${REPO_ROOT}/.venv/bin/python"
else
  PYTHON_BIN="python3"
fi

if [[ -x "${REPO_ROOT}/.venv/bin/pytest" ]]; then
  PYTEST_RUNNER=("${REPO_ROOT}/.venv/bin/pytest")
else
  PYTEST_RUNNER=(poetry run pytest)
fi

echo "== [1/7] Run targeted pytest with coverage =="
"${PYTEST_RUNNER[@]}" \
  label_studio/organizations/tests/test_api.py \
  label_studio/organizations/tests/test_workspaces_api.py \
  label_studio/organizations/tests/test_seed_phase2_demo_command.py \
  label_studio/projects/tests/test_project_workspace.py \
  label_studio/projects/tests/test_project_member_roles.py \
  label_studio/projects/tests/test_role_permissions.py \
  --cov=organizations.functions \
  --cov=organizations.models \
  --cov=organizations.api \
  --cov=organizations.serializers \
  --cov=projects.models \
  --cov=projects.serializers \
  --cov=projects.api \
  --cov=projects.functions.next_task \
  --cov=core.api_permissions \
  --cov=core.permissions \
  --cov-report=term \
  --cov-report=xml:"${OUTPUT_DIR}/coverage.xml" \
  -q | tee "${OUTPUT_DIR}/pytest.log"

echo "== [2/7] Build custom image =="
docker build -t "${IMAGE_TAG}" "${REPO_ROOT}" | tee "${OUTPUT_DIR}/docker-build.log"

echo "== [3/7] Upgrade containers with custom image =="
LABEL_STUDIO_IMAGE="${IMAGE_TAG}" docker compose -f "${REPO_ROOT}/docker-compose.yml" up -d --force-recreate app nginx db | tee "${OUTPUT_DIR}/docker-up.log"
LABEL_STUDIO_IMAGE="${IMAGE_TAG}" docker compose -f "${REPO_ROOT}/docker-compose.yml" exec -T app python label_studio/manage.py migrate | tee "${OUTPUT_DIR}/migrate.log"

echo "== [4/7] Seed phase2 demo data =="
seed_raw="$(
  LABEL_STUDIO_IMAGE="${IMAGE_TAG}" docker compose -f "${REPO_ROOT}/docker-compose.yml" exec -T app \
    python label_studio/manage.py seed_phase2_demo \
      --organization-title "二期验收组织" \
      --project-title "二期主流程验收项目" \
      --task-count 8
)"
printf '%s\n' "${seed_raw}" > "${OUTPUT_DIR}/seed.log"

seed_json="$(
  "${PYTHON_BIN}" - "${OUTPUT_DIR}/seed.log" <<'PY'
import json
import sys
from pathlib import Path

lines = [line.strip() for line in Path(sys.argv[1]).read_text(encoding='utf-8', errors='ignore').splitlines() if line.strip()]
for line in reversed(lines):
    try:
        json.loads(line)
        print(line)
        break
    except Exception:
        continue
else:
    raise SystemExit("No JSON payload found in seed command output")
PY
)"
printf '%s\n' "${seed_json}" > "${OUTPUT_DIR}/seed.json"

eval "$("${PYTHON_BIN}" - <<'PY' "${OUTPUT_DIR}/seed.json"
import json
import shlex
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
mapping = {
    "ORGANIZATION_ID": data["organization_id"],
    "PROJECT_ID": data["project_id"],
    "FIRST_TASK_ID": data["first_task_id"],
    "ANNOTATOR_USER_ID": data["annotator_user_id"],
    "OWNER_TOKEN": data["owner_token"],
    "MANAGER_TOKEN": data["manager_token"],
    "ANNOTATOR_TOKEN": data["annotator_token"],
    "ANNOTATOR_EMAIL": data["annotator_email"],
    "ANNOTATOR_PASSWORD": data["annotator_password"],
}
for key, value in mapping.items():
    print(f"{key}={shlex.quote(str(value))}")
PY
)"

echo "== [5/7] API smoke test =="
echo "Wait for API readiness..."
ready=false
for _ in $(seq 1 60); do
  status_code="$(curl -s -o /tmp/phase2_api_ready.txt -w '%{http_code}' "${BASE_URL%/}/api/projects/" || true)"
  if [[ "${status_code}" == "200" || "${status_code}" == "401" || "${status_code}" == "403" ]]; then
    ready=true
    break
  fi
  sleep 2
done
if [[ "${ready}" != "true" ]]; then
  echo "API readiness check failed, last status=${status_code}" >&2
  exit 1
fi

"${PYTHON_BIN}" "${REPO_ROOT}/scripts/phase2_api_smoke.py" \
  --base-url "${BASE_URL}" \
  --organization-id "${ORGANIZATION_ID}" \
  --project-id "${PROJECT_ID}" \
  --task-id "${FIRST_TASK_ID}" \
  --annotator-user-id "${ANNOTATOR_USER_ID}" \
  --owner-token "${OWNER_TOKEN}" \
  --manager-token "${MANAGER_TOKEN}" \
  --annotator-token "${ANNOTATOR_TOKEN}" \
  --output "${OUTPUT_DIR}/api-smoke.json" | tee "${OUTPUT_DIR}/api-smoke.log"

echo "== [6/7] UI smoke test (browser) =="
"${PYTHON_BIN}" -m pip install --quiet playwright==1.55.0
if [[ "$(uname -s)" == "Linux" ]]; then
  "${PYTHON_BIN}" -m playwright install --with-deps chromium
else
  "${PYTHON_BIN}" -m playwright install chromium
fi

ui_args=(
  "${REPO_ROOT}/scripts/phase2_ui_smoke.py"
  --base-url "${BASE_URL}"
  --email "${ANNOTATOR_EMAIL}"
  --password "${ANNOTATOR_PASSWORD}"
  --project-id "${PROJECT_ID}"
  --output-dir "${OUTPUT_DIR}/ui"
)
if [[ "${HEADED_UI}" == "true" ]]; then
  ui_args+=(--headed)
fi
"${PYTHON_BIN}" "${ui_args[@]}" | tee "${OUTPUT_DIR}/ui-smoke.log"

echo "== [7/7] Generate markdown report =="
"${PYTHON_BIN}" "${REPO_ROOT}/scripts/phase2_generate_report.py" \
  --artifacts-dir "${OUTPUT_DIR}" \
  --version "v2" \
  --output "${OUTPUT_DIR}/TEST_REPORT_PHASE2_V2.md" | tee "${OUTPUT_DIR}/report.log"

cp "${OUTPUT_DIR}/TEST_REPORT_PHASE2_V2.md" "${REPO_ROOT}/TEST_REPORT_PHASE2_V2.md"

echo "Pipeline finished. Artifacts: ${OUTPUT_DIR}"
