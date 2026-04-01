#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write('\n')


def main() -> int:
    parser = argparse.ArgumentParser(description='Phase2 UI smoke test via Playwright')
    parser.add_argument('--base-url', default='http://localhost:8080')
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--project-id', type=int, required=True)
    parser.add_argument('--label-text', default='积极')
    parser.add_argument('--output-dir', default='output/playwright/phase2-ui')
    parser.add_argument('--headed', action='store_true')
    args = parser.parse_args()

    base_url = args.base_url.rstrip('/')
    output_dir = Path(args.output_dir)
    screenshot_path = output_dir / 'phase2-ui-after-submit.png'
    html_snapshot_path = output_dir / 'phase2-ui-after-submit.html'
    result_path = output_dir / 'phase2-ui-result.json'
    output_dir.mkdir(parents=True, exist_ok=True)

    result: dict[str, Any] = {
        'status': 'failed',
        'base_url': base_url,
        'project_id': args.project_id,
        'email': args.email,
        'label_text': args.label_text,
        'error': '',
        'verification': '',
        'artifacts': {
            'screenshot': str(screenshot_path),
            'snapshot_html': str(html_snapshot_path),
        },
    }

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not args.headed)
            context = browser.new_context(locale='zh-CN')
            page = context.new_page()

            page.goto(f'{base_url}/user/login', wait_until='domcontentloaded', timeout=30000)
            page.fill('input[name="email"]', args.email)
            page.fill('input[name="password"]', args.password)
            page.click('button[type="submit"]')
            page.wait_for_url(re.compile(rf'^{re.escape(base_url)}/($|\\?)'), timeout=30000)

            page.goto(
                f'{base_url}/projects/{args.project_id}/data?labeling=1',
                wait_until='networkidle',
                timeout=45000,
            )

            # Label first visible choice, then submit current annotation.
            page.locator(f'text={args.label_text}').first.click(timeout=20000)
            page.click("button[aria-label='Submit current annotation']", timeout=20000)

            success_toast_found = False
            try:
                page.locator('text=Annotation saved successfully').first.wait_for(timeout=12000)
                success_toast_found = True
            except PlaywrightTimeoutError:
                try:
                    page.locator('text=标注已保存').first.wait_for(timeout=6000)
                    success_toast_found = True
                except PlaywrightTimeoutError:
                    success_toast_found = False

            page.screenshot(path=str(screenshot_path), full_page=True)
            html_snapshot_path.write_text(page.content(), encoding='utf-8')
            browser.close()

            if success_toast_found:
                result['status'] = 'passed'
                result['verification'] = 'detected annotation saved success toast'
            else:
                result['status'] = 'failed'
                result['error'] = 'annotation success toast not detected after submit'

    except Exception as exc:
        result['status'] = 'failed'
        result['error'] = f'{type(exc).__name__}: {exc}'

    _write_json(result_path, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
