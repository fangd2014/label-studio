# 二期 V2 持续交付指南（中文）

更新时间：2026-04-01

## 1. 目标

将“二期能力”升级为可重复执行的持续交付流程，覆盖：

1. 后端回归测试与覆盖率统计
2. 自定义镜像构建
3. Docker 升级部署
4. 演示数据自动模拟
5. API 主流程冒烟
6. 浏览器主流程冒烟（登录 -> 标注 -> 提交）
7. Markdown 测试报告生成

## 2. 本地一键执行

```bash
bash scripts/phase2_v2_pipeline.sh \
  --base-url http://localhost:8080 \
  --image-tag label-studio:phase2-v2-local
```

执行完成后：

- 报告：`TEST_REPORT_PHASE2_V2.md`
- 全量产物：`test_artifacts/phase2-v2/<timestamp>/`

## 3. 企业 smoke 入口

```bash
bash scripts/enterprise/smoke_enterprise.sh
```

附加健康检查：

```bash
bash scripts/enterprise/check_enterprise_health.sh http://localhost:8080
```

## 4. CI 工作流

- `/.github/workflows/phase2-v2-cd.yml`
  - 运行二期 v2 全链路交付
  - 上传 `phase2-v2-artifacts`

- `/.github/workflows/tests-enterprise-contracts.yml`
  - 运行企业 smoke 契约验证
  - 上传 `enterprise-smoke-artifacts`

## 5. 关键脚本说明

- `scripts/phase2_v2_pipeline.sh`：编排测试、构建、部署、造数、API/UI 验收与报告
- `scripts/phase2_api_smoke.py`：校验角色权限、中文错误消息、工作区接口
- `scripts/phase2_ui_smoke.py`：Playwright 浏览器主流程测试
- `scripts/phase2_generate_report.py`：汇总生成测试报告

## 6. 产物清单（默认）

- `pytest.log`：后端测试日志
- `coverage.xml`：覆盖率明细
- `seed.json`：演示数据与登录凭据
- `api-smoke.json`：API 验收结果
- `ui/phase2-ui-result.json`：UI 验收结果
- `ui/phase2-ui-after-submit.png`：浏览器截图证据
- `TEST_REPORT_PHASE2_V2.md`：最终报告
