# Codex 可执行任务清单（按文件级改动）

> 输入依据：
> - `docs/PRD/PRD_label_studio_enterprise_reverse.md`
> - `docs/PRD/SDD_label_studio_enterprise_reverse.md`
> - `docs/PRD/TEST_DESIGN_label_studio_enterprise_reverse.md`

## 1. 执行说明
- 目标：把企业版 PRD/SDD/TEST_DESIGN 拆成可直接分派给 Codex 的文件级任务。
- 策略：按里程碑分批交付，优先 P0（M1），再做 P1（M2），最后 P2（M3）。
- 约束：每个任务必须同时提交“代码 + 测试 + 文档/脚本（如涉及部署）”。

## 2. 里程碑 M1（P0）

### Task M1-01：企业能力开关与配置基线（ENT-FR-027 前置）
**Create**
- `label_studio/core/feature_flags/enterprise.py`
- `label_studio/core/feature_flags/tests/test_enterprise.py`
- `web/apps/labelstudio/src/utils/__tests__/license-flags.test.ts`

**Modify**
- `label_studio/core/settings/base.py`
- `label_studio/feature_flags.json`
- `web/apps/labelstudio/src/utils/license-flags.ts`
- `web/apps/labelstudio/src/utils/feature-flags.ts`

**Test**
- `pytest label_studio/core/feature_flags/tests/test_base.py -q`
- `pytest label_studio/core/feature_flags/tests/test_enterprise.py -q`

---

### Task M1-02：组织与工作空间隔离硬化（ENT-FR-001/002/003）
**Create**
- `label_studio/organizations/tests/test_tenant_isolation.py`

**Modify**
- `label_studio/organizations/middleware.py`
- `label_studio/organizations/mixins.py`
- `label_studio/core/api_permissions.py`
- `label_studio/projects/api.py`
- `label_studio/tasks/api.py`

**Test**
- `pytest label_studio/organizations/tests/test_tenant_isolation.py -q`
- `pytest label_studio/organizations/tests/test_api.py -q`

---

### Task M1-03：Workspace-Project 绑定与约束（ENT-FR-002/005）
**Create**
- `label_studio/organizations/migrations/0008_workspace_constraints.py`
- `label_studio/projects/migrations/0037_project_workspace_constraints.py`

**Modify**
- `label_studio/organizations/models.py`
- `label_studio/organizations/serializers.py`
- `label_studio/organizations/api.py`
- `label_studio/projects/models.py`
- `label_studio/projects/serializers.py`
- `label_studio/projects/api.py`

**Test**
- `pytest label_studio/organizations/tests/test_workspaces_api.py -q`
- `pytest label_studio/projects/tests/test_project_workspace.py -q`

---

### Task M1-04：RBAC 策略引擎与项目角色（ENT-FR-004/005/006）
**Create**
- `label_studio/projects/role_policies.py`
- `label_studio/projects/services/project_roles.py`
- `label_studio/projects/tests/test_policy_engine.py`

**Modify**
- `label_studio/projects/permissions.py`
- `label_studio/projects/api.py`
- `label_studio/projects/serializers.py`
- `label_studio/users/serializers.py`

**Test**
- `pytest label_studio/projects/tests/test_role_permissions.py -q`
- `pytest label_studio/projects/tests/test_project_member_roles.py -q`
- `pytest label_studio/projects/tests/test_policy_engine.py -q`

---

### Task M1-05：身份集成基础骨架（SCIM/SAML/LDAP 路由占位，ENT-FR-007/008/009）
**Create**
- `label_studio/identity/apps.py`
- `label_studio/identity/urls.py`
- `label_studio/identity/api.py`
- `label_studio/identity/serializers.py`
- `label_studio/identity/services/saml_service.py`
- `label_studio/identity/services/scim_service.py`
- `label_studio/identity/services/ldap_service.py`
- `label_studio/tests/identity/test_scim_api.py`

**Modify**
- `label_studio/core/settings/base.py`
- `label_studio/core/urls.py`
- `label_studio/users/models.py`

**Test**
- `pytest label_studio/tests/identity/test_scim_api.py -q`

---

### Task M1-06：审计日志域模型与落库链路（ENT-FR-011）
**Create**
- `label_studio/audit/apps.py`
- `label_studio/audit/models.py`
- `label_studio/audit/serializers.py`
- `label_studio/audit/api.py`
- `label_studio/audit/services.py`
- `label_studio/audit/migrations/0001_initial.py`
- `label_studio/audit/tests/test_audit_api.py`

**Modify**
- `label_studio/core/settings/base.py`
- `label_studio/core/urls.py`
- `label_studio/organizations/api.py`
- `label_studio/projects/api.py`
- `label_studio/users/api.py`
- `label_studio/session_policy/api.py`

**Test**
- `pytest label_studio/audit/tests/test_audit_api.py -q`

---

### Task M1-07：Compose 企业部署契约与校验器（ENT-DEP-001）
**Create**
- `deploy/enterprise/docker-compose.enterprise.yml`
- `deploy/enterprise/env.enterprise.example.list`
- `deploy/enterprise/validate_compose_env.py`
- `label_studio/tests/deployment/test_compose_contract.py`

**Modify**
- `deploy/docker-entrypoint.sh`
- `docs/source/guide/install_enterprise_docker.md`

**Test**
- `pytest label_studio/tests/deployment/test_compose_contract.py -q`
- `python deploy/enterprise/validate_compose_env.py --env-file deploy/enterprise/env.enterprise.example.list`

---

### Task M1-08：Helm/Secret/TLS 契约校验器（ENT-DEP-002/003/004）
**Create**
- `deploy/enterprise/ls-values.enterprise.minimal.yaml`
- `deploy/enterprise/ls-values.enterprise.prod.yaml`
- `deploy/enterprise/validate_helm_values.py`
- `label_studio/tests/deployment/test_helm_contract.py`
- `label_studio/tests/deployment/test_tls_contract.py`

**Modify**
- `docs/source/guide/install_enterprise_k8s.md`
- `docs/source/guide/helm_values.md`

**Test**
- `pytest label_studio/tests/deployment/test_helm_contract.py -q`
- `pytest label_studio/tests/deployment/test_tls_contract.py -q`
- `python deploy/enterprise/validate_helm_values.py --values deploy/enterprise/ls-values.enterprise.minimal.yaml`

---

### Task M1-09：P0 集成回归与 CI 门禁（ENT-FR/ENT-DEP P0 汇总）
**Create**
- `.github/workflows/tests-enterprise-contracts.yml`
- `scripts/enterprise/check_enterprise_health.sh`
- `scripts/enterprise/smoke_enterprise.sh`

**Modify**
- `.github/workflows/tests.yml`
- `docs/PRD/TEST_DESIGN_label_studio_enterprise_reverse.md`

**Test**
- 本地执行 `scripts/enterprise/smoke_enterprise.sh`
- 触发 CI 工作流并验证 P0 用例集通过

## 3. 里程碑 M2（P1）

### Task M2-01：SAML 登录链路实现（ENT-FR-007）
**Create**
- `label_studio/tests/identity/test_saml_login.py`

**Modify**
- `label_studio/identity/services/saml_service.py`
- `label_studio/identity/api.py`
- `label_studio/identity/serializers.py`
- `label_studio/users/api.py`

**Test**
- `pytest label_studio/tests/identity/test_saml_login.py -q`

---

### Task M2-02：SCIM 同步与幂等实现（ENT-FR-008）
**Create**
- `label_studio/tests/identity/test_scim_idempotent.py`

**Modify**
- `label_studio/identity/services/scim_service.py`
- `label_studio/identity/api.py`
- `label_studio/users/models.py`
- `label_studio/organizations/models.py`

**Test**
- `pytest label_studio/tests/identity/test_scim_api.py -q`
- `pytest label_studio/tests/identity/test_scim_idempotent.py -q`

---

### Task M2-03：LDAP 认证适配（ENT-FR-009）
**Create**
- `label_studio/tests/identity/test_ldap_auth.py`

**Modify**
- `label_studio/identity/services/ldap_service.py`
- `label_studio/users/api.py`
- `label_studio/core/settings/base.py`

**Test**
- `pytest label_studio/tests/identity/test_ldap_auth.py -q`

---

### Task M2-04：自动分发与队列策略增强（ENT-FR-023）
**Create**
- `label_studio/projects/tests/test_auto_distribution.py`
- `label_studio/projects/tests/test_skip_queue_policy.py`

**Modify**
- `label_studio/projects/functions/next_task.py`
- `label_studio/projects/models.py`
- `label_studio/projects/serializers.py`
- `label_studio/tasks/api.py`

**Test**
- `pytest label_studio/projects/tests/test_auto_distribution.py -q`
- `pytest label_studio/projects/tests/test_skip_queue_policy.py -q`
- `pytest label_studio/tests/test_next_task.py -q`

---

### Task M2-05：质量规则、一致性指标、低信任护栏（ENT-FR-017/018/019）
**Create**
- `label_studio/quality/apps.py`
- `label_studio/quality/services.py`
- `label_studio/quality/api.py`
- `label_studio/quality/serializers.py`
- `label_studio/quality/tests/test_quality_rules.py`
- `label_studio/quality/tests/test_agreement_metrics.py`

**Modify**
- `label_studio/projects/models.py`
- `label_studio/projects/api.py`
- `label_studio/tasks/api.py`
- `label_studio/data_manager/api.py`

**Test**
- `pytest label_studio/quality/tests/test_quality_rules.py -q`
- `pytest label_studio/quality/tests/test_agreement_metrics.py -q`

---

### Task M2-06：协作能力（评论通知 + 深链）（ENT-FR-025/026）
**Create**
- `label_studio/collaboration/apps.py`
- `label_studio/collaboration/models.py`
- `label_studio/collaboration/api.py`
- `label_studio/collaboration/serializers.py`
- `label_studio/collaboration/tests/test_comments_api.py`
- `label_studio/collaboration/tests/test_deep_links.py`

**Modify**
- `label_studio/core/urls.py`
- `web/apps/labelstudio/src/pages/DataManager/DataManager.jsx`
- `web/apps/labelstudio/src/components/CopyableTooltip/CopyableTooltip.jsx`

**Test**
- `pytest label_studio/collaboration/tests/test_comments_api.py -q`
- `pytest label_studio/collaboration/tests/test_deep_links.py -q`

---

### Task M2-07：前端企业设置入口与角色管理面板（ENT-FR-021/024/020）
**Create**
- `web/apps/labelstudio/src/pages/Settings/EnterpriseSettings.jsx`
- `web/apps/labelstudio/src/pages/Settings/EnterpriseSettings.prefix.css`
- `web/apps/labelstudio/src/pages/Organization/PeoplePage/RoleMatrixDialog.jsx`

**Modify**
- `web/apps/labelstudio/src/pages/Settings/index.jsx`
- `web/apps/labelstudio/src/pages/Settings/GeneralSettings.jsx`
- `web/apps/labelstudio/src/pages/Organization/PeoplePage/PeoplePage.jsx`
- `web/apps/labelstudio/src/routes/ProjectRoutes.jsx`
- `web/apps/labelstudio/src/utils/license-flags.ts`

**Test**
- `yarn test web/apps/labelstudio/src/pages/Settings --watch=false`

## 4. 里程碑 M3（P2）

### Task M3-01：Prompts 集成开关与接口占位（ENT-FR-015）
**Create**
- `label_studio/prompts_enterprise/apps.py`
- `label_studio/prompts_enterprise/api.py`
- `label_studio/prompts_enterprise/tests/test_prompts_api.py`

**Modify**
- `label_studio/core/settings/base.py`
- `label_studio/core/urls.py`
- `web/apps/labelstudio/src/pages/Settings/index.jsx`

**Test**
- `pytest label_studio/prompts_enterprise/tests/test_prompts_api.py -q`

---

### Task M3-02：Whitelabel 配置链路（ENT-FR-029）
**Create**
- `label_studio/branding/apps.py`
- `label_studio/branding/api.py`
- `label_studio/branding/serializers.py`
- `label_studio/branding/tests/test_branding_api.py`

**Modify**
- `label_studio/core/settings/base.py`
- `label_studio/core/views.py`
- `web/apps/labelstudio/src/config/ApiConfig.example.js`
- `web/apps/labelstudio/src/app/App.jsx`

**Test**
- `pytest label_studio/branding/tests/test_branding_api.py -q`

## 5. 全局交付检查（每个里程碑结束都执行）
1. `pytest -q`（至少覆盖本里程碑新增/变更测试集）。
2. `python -m pytest label_studio/tests/test_api.py -q`（基础 API 回归抽样）。
3. 前端改动执行：`yarn test` + `yarn lint`（按目录最小化运行）。
4. 更新文档映射：
   - `docs/PRD/PRD_label_studio_enterprise_reverse.md`
   - `docs/PRD/SDD_label_studio_enterprise_reverse.md`
   - `docs/PRD/TEST_DESIGN_label_studio_enterprise_reverse.md`

## 6. 建议提交粒度
1. 每个 Task 独立 commit。
2. commit message 模板：`feat(enterprise): <task-id> <short-summary>`。
3. 涉及 DB 迁移的 Task：必须在同一 commit 包含迁移与回归测试。
