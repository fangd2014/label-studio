# 企业版执行清单差异核对（2026-04-01）

基线文档：`docs/PRD/CODEX_EXEC_TASKS_label_studio_enterprise.md`

## 1. 核对结论（按里程碑）

- M1（P0）：已落地“组织-工作区-项目角色”主干能力，企业契约、身份集成、审计、Helm/Compose 专项仍有较大缺口。
- M2（P1）：未系统启动（SAML/SCIM/LDAP、质量规则、协作、企业前端入口等）。
- M3（P2）：未系统启动（Prompts 企业能力、Whitelabel）。

## 2. 已落地能力（与清单映射）

### 2.1 组织/工作区/角色主干（部分覆盖 M1-02/M1-03/M1-04）
- 工作区模型与默认工作区：`label_studio/organizations/models.py`
- 工作区 API 与序列化：`label_studio/organizations/api.py`、`label_studio/organizations/serializers.py`
- 项目绑定工作区与成员角色：`label_studio/projects/models.py`、`label_studio/projects/serializers.py`、`label_studio/projects/api.py`
- 项目角色权限收口：`label_studio/core/api_permissions.py`、`label_studio/core/permissions.py`、`label_studio/projects/functions/next_task.py`
- 回归测试：
  - `label_studio/organizations/tests/test_workspaces_api.py`
  - `label_studio/projects/tests/test_project_workspace.py`
  - `label_studio/projects/tests/test_project_member_roles.py`
  - `label_studio/projects/tests/test_role_permissions.py`

### 2.2 中文优先与验收文档
- 中文提示与二期验收文档：`docs/verification/phase2-step-by-step-cn.md`

## 3. 主要差异（截至 2026-04-01）

以下任务在清单中标记为 `Create` 的文件大多尚未创建，属于实质差异：

- M1-01：企业开关基线（`core/feature_flags/enterprise.py` 及测试）
- M1-02：租户隔离专项测试（`organizations/tests/test_tenant_isolation.py`）
- M1-03：额外约束迁移（`organizations/migrations/0008_workspace_constraints.py`、`projects/migrations/0037_project_workspace_constraints.py`）
- M1-04：独立策略引擎模块（`projects/role_policies.py`、`projects/services/project_roles.py`、`test_policy_engine.py`）
- M1-05～M1-08：身份集成、审计、部署契约与 Helm/TLS 校验全套模块
- M1-09：企业专项 CI 门禁与 smoke 脚本
- M2 / M3：尚未启动

## 4. 本轮开发策略（先补可闭环能力）

本轮优先补齐“可验证交付闭环”，目标是完成：

1. 企业/二期专项 CI/CD 流程（自动测试、构建、部署验收）
2. 数据模拟脚本（可重复执行）
3. 浏览器主流程测试脚本（登录 -> 标注 -> 提交）
4. 自动化测试报告产出

以上完成后，再继续推进 M1 余下模块（身份、审计、部署契约等）。

## 5. 风险说明

- `CODEX_EXEC_TASKS` 里程碑跨度较大（M1~M3），无法在单批次改动内完整闭环。
- 当前优先方案为“先保证交付链路可执行”，再按清单逐任务推进并保持每步可验证。
