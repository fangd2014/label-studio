#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))


def _parse_pytest(pytest_log: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        'summary': 'not found',
        'passed': 0,
        'failed': 0,
        'deselected': 0,
        'coverage': 'N/A',
    }
    if not pytest_log.exists():
        return result

    lines = pytest_log.read_text(encoding='utf-8', errors='ignore').splitlines()
    summary_line = next((line for line in reversed(lines) if ' in ' in line and 'passed' in line), '')
    if summary_line:
        result['summary'] = summary_line.strip()
        passed_match = re.search(r'(\d+)\s+passed', summary_line)
        failed_match = re.search(r'(\d+)\s+failed', summary_line)
        deselected_match = re.search(r'(\d+)\s+deselected', summary_line)
        if passed_match:
            result['passed'] = int(passed_match.group(1))
        if failed_match:
            result['failed'] = int(failed_match.group(1))
        if deselected_match:
            result['deselected'] = int(deselected_match.group(1))

    coverage_line = next((line for line in reversed(lines) if line.startswith('TOTAL')), '')
    if coverage_line:
        coverage_match = re.search(r'(\d+%)\s*$', coverage_line.strip())
        if coverage_match:
            result['coverage'] = coverage_match.group(1)
    return result


def _format_check_item(check: dict[str, Any]) -> str:
    mark = 'PASS' if check.get('passed') else 'FAIL'
    return f'- [{mark}] {check.get("name", "unknown")}'


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate markdown report for phase2 pipeline')
    parser.add_argument('--artifacts-dir', required=True)
    parser.add_argument('--output')
    parser.add_argument('--version', default='v2')
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir)
    output_path = Path(args.output) if args.output else artifacts_dir / 'TEST_REPORT_PHASE2_V2.md'

    pytest_result = _parse_pytest(artifacts_dir / 'pytest.log')
    seed_result = _read_json(artifacts_dir / 'seed.json')
    api_result = _read_json(artifacts_dir / 'api-smoke.json')
    ui_result = _read_json(artifacts_dir / 'ui' / 'phase2-ui-result.json')

    api_checks = api_result.get('checks', []) if isinstance(api_result, dict) else []
    api_failed = [item for item in api_checks if not item.get('passed')]
    ui_status = ui_result.get('status', 'failed')
    ui_error = ui_result.get('error', '')

    issues: list[str] = []
    for failed in api_failed:
        issues.append(f'API: {failed.get("name", "unknown")} 未通过')
    if ui_status != 'passed':
        issues.append(f'UI: {ui_error or "主流程未通过"}')

    if pytest_result['failed'] > 0:
        issues.append(f'Pytest: 存在 {pytest_result["failed"]} 个失败用例')

    issue_text = '\n'.join(f'- {item}' for item in issues) if issues else '- 无阻断问题'
    api_checks_text = '\n'.join(_format_check_item(item) for item in api_checks) if api_checks else '- 无数据'

    report = f"""# Label Studio 二期持续交付测试报告（{args.version}）

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
产物目录：`{artifacts_dir}`

## 1. 执行概览
- 版本：`{args.version}`
- 项目ID：`{seed_result.get('project_id', 'N/A')}`
- 组织ID：`{seed_result.get('organization_id', 'N/A')}`
- 测试任务ID：`{seed_result.get('first_task_id', 'N/A')}`

## 2. 自动化验证结果

### 2.1 后端测试
- 摘要：`{pytest_result['summary']}`
- 通过：`{pytest_result['passed']}`
- 失败：`{pytest_result['failed']}`
- 覆盖率（本轮目标模块）：`{pytest_result['coverage']}`

### 2.2 API 主流程冒烟
- 总体：`{"通过" if api_result.get("passed") else "失败"}`
{api_checks_text}

### 2.3 浏览器主流程冒烟
- 总体：`{"通过" if ui_status == "passed" else "失败"}`
- 说明：`{ui_result.get('verification', ui_error or 'N/A')}`
- 截图：`{ui_result.get('artifacts', {}).get('screenshot', 'N/A')}`

## 3. 问题与差异
{issue_text}

## 4. 结论
- 当前交付链路：`{"可用" if not issues else "部分可用"}`
- 建议：继续按 `docs/verification/enterprise_exec_gap_2026-04-01.md` 的差异项推进 M1 剩余任务。
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')
    print(report)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
