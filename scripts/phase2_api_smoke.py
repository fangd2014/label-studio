#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any

import requests


def _request(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> requests.Response:
    headers = {'Authorization': f'Token {token}'}
    if payload is None:
        return requests.request(method, url, headers=headers, timeout=30)
    return requests.request(method, url, headers=headers, json=payload, timeout=30)


def _body(response: requests.Response) -> Any:
    try:
        return response.json()
    except Exception:
        return response.text


def _dump(result: dict[str, Any], output: str | None) -> None:
    content = json.dumps(result, ensure_ascii=False, indent=2)
    if output:
        with open(output, 'w', encoding='utf-8') as file:
            file.write(content + '\n')
    print(content)


def main() -> int:
    parser = argparse.ArgumentParser(description='Phase2 role/workspace API smoke verification')
    parser.add_argument('--base-url', default='http://localhost:8080')
    parser.add_argument('--project-id', type=int, required=True)
    parser.add_argument('--task-id', type=int, required=True)
    parser.add_argument('--annotator-user-id', type=int, required=True)
    parser.add_argument('--annotator-token', required=True)
    parser.add_argument('--manager-token', required=True)
    parser.add_argument('--owner-token')
    parser.add_argument('--organization-id', type=int)
    parser.add_argument('--output')
    args = parser.parse_args()

    base_url = args.base_url.rstrip('/')
    result: dict[str, Any] = {
        'base_url': base_url,
        'project_id': args.project_id,
        'task_id': args.task_id,
    }
    checks: list[tuple[str, bool]] = []

    annotator_patch_response = _request(
        'PATCH',
        f'{base_url}/api/projects/{args.project_id}/',
        args.annotator_token,
        {'title': 'annotator_forbidden_update'},
    )
    annotator_patch_body = _body(annotator_patch_response)
    annotator_patch_detail = (
        annotator_patch_body.get('detail') if isinstance(annotator_patch_body, dict) else str(annotator_patch_body)
    )
    result['annotator_patch_status'] = annotator_patch_response.status_code
    result['annotator_patch_detail'] = annotator_patch_detail
    checks.append(('annotator_patch_forbidden', annotator_patch_response.status_code == 403))
    checks.append(
        (
            'annotator_patch_cn_message',
            isinstance(annotator_patch_detail, str) and '当前项目角色无权执行此操作，请联系项目管理员。' in annotator_patch_detail,
        )
    )

    manager_patch_response = _request(
        'PATCH',
        f'{base_url}/api/projects/{args.project_id}/',
        args.manager_token,
        {'title': 'manager_update_ok'},
    )
    result['manager_patch_status'] = manager_patch_response.status_code
    checks.append(('manager_patch_allowed', manager_patch_response.status_code == 200))

    invalid_role_response = _request(
        'PATCH',
        f'{base_url}/api/projects/{args.project_id}/memberships/{args.annotator_user_id}/',
        args.manager_token,
        {'role': 'invalid_role'},
    )
    invalid_role_body = _body(invalid_role_response)
    invalid_role_text = str(invalid_role_body)
    result['invalid_role_status'] = invalid_role_response.status_code
    result['invalid_role_response'] = invalid_role_body
    checks.append(('invalid_role_status_400', invalid_role_response.status_code == 400))
    checks.append(('invalid_role_cn_message', '角色仅支持 annotator、reviewer、manager' in invalid_role_text))

    annotation_create_response = _request(
        'POST',
        f'{base_url}/api/tasks/{args.task_id}/annotations/',
        args.annotator_token,
        {'result': []},
    )
    result['annotator_annotation_status'] = annotation_create_response.status_code
    checks.append(('annotator_create_annotation', annotation_create_response.status_code == 201))

    if args.owner_token and args.organization_id:
        workspace_response = _request(
            'GET',
            f'{base_url}/api/organizations/{args.organization_id}/workspaces',
            args.owner_token,
        )
        workspace_body = _body(workspace_response)
        default_title = None
        if isinstance(workspace_body, list) and workspace_body:
            default_workspace = next((ws for ws in workspace_body if ws.get('is_default')), workspace_body[0])
            default_title = default_workspace.get('title')
        result['workspace_api_status'] = workspace_response.status_code
        result['workspace_default_title'] = default_title
        checks.append(('workspace_api_ok', workspace_response.status_code == 200))
        checks.append(('workspace_default_cn_title', default_title == '默认工作区'))

    result['checks'] = [{'name': name, 'passed': passed} for name, passed in checks]
    result['passed'] = all(passed for _, passed in checks)

    _dump(result, args.output)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
