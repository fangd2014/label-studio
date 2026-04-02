# 企业版执行清单差异核对（更新于 2026-04-02）

基线文档：`docs/PRD/CODEX_EXEC_TASKS_label_studio_enterprise.md`

## 1. 核对结论（按里程碑）

- M1（P0）：已落地“组织-工作区-项目角色”主干能力，并补齐组织菜单中的“工作区管理”入口。
- M2（P1）：已系统启动并完成第一批可用交付（SAML/SCIM/LDAP、质量规则与一致性指标、协作评论与深链、企业前端入口）。
- M3（P2）：已系统启动并完成占位交付（Prompts 企业能力开关/API、Whitelabel 配置/API 与前端挂载）。

## 2. 本批已交付能力（V3）

### 2.1 M1 菜单补齐
- 组织页新增“工作区”菜单与管理页：`web/apps/labelstudio/src/pages/Organization/WorkspacePage/WorkspacePage.jsx`
- 前端 API 对接工作区：`web/apps/labelstudio/src/config/ApiConfig.js`

### 2.2 M2 身份能力
- 新增身份模块：`label_studio/identity/*`
- 后端路由接入：`label_studio/core/urls.py`、`label_studio/core/settings/base.py`
- 用户身份字段扩展：`label_studio/users/models.py`、`label_studio/users/migrations/0012_user_identity_fields.py`
- 组织工作区 SCIM 组字段：`label_studio/organizations/models.py`、`label_studio/organizations/migrations/0008_workspace_external_group_id.py`
- 测试：
  - `label_studio/tests/identity/test_scim_api.py`
  - `label_studio/tests/identity/test_saml_login.py`
  - `label_studio/tests/identity/test_scim_idempotent.py`
  - `label_studio/tests/identity/test_ldap_auth.py`

### 2.3 M2 质量能力
- 新增质量模块：`label_studio/quality/*`
- 项目质量字段：`label_studio/projects/models.py`、`label_studio/projects/migrations/0037_project_quality_fields.py`
- 接入项目/任务/数据管理：`label_studio/projects/serializers.py`、`label_studio/tasks/api.py`、`label_studio/data_manager/api.py`
- 测试：
  - `label_studio/quality/tests/test_quality_rules.py`
  - `label_studio/quality/tests/test_agreement_metrics.py`

### 2.4 M2 协作能力
- 新增协作模块：`label_studio/collaboration/*`
- 评论与深链 API：`/api/projects/<id>/collaboration/comments`、`/api/projects/<id>/collaboration/deep-link`
- 前端“复制深链”入口：`web/apps/labelstudio/src/pages/DataManager/DataManager.jsx`、`web/apps/labelstudio/src/components/CopyableTooltip/CopyableTooltip.jsx`
- 测试：
  - `label_studio/collaboration/tests/test_comments_api.py`
  - `label_studio/collaboration/tests/test_deep_links.py`

### 2.5 M2 企业前端入口
- 新增企业设置页：`web/apps/labelstudio/src/pages/Settings/EnterpriseSettings.jsx`
- 新增角色矩阵弹窗：`web/apps/labelstudio/src/pages/Organization/PeoplePage/RoleMatrixDialog.jsx`
- 设置菜单与组织成员页接入：
  - `web/apps/labelstudio/src/pages/Settings/index.jsx`
  - `web/apps/labelstudio/src/pages/Organization/PeoplePage/PeoplePage.jsx`

### 2.6 M3 Prompts 企业能力
- 新增模块：`label_studio/prompts_enterprise/*`
- 前端企业设置页展示与开关：`web/apps/labelstudio/src/pages/Settings/EnterpriseSettings.jsx`
- 测试：
  - `label_studio/prompts_enterprise/tests/test_prompts_api.py`

### 2.7 M3 Whitelabel
- 新增模块：`label_studio/branding/*`
- 支持登录页跳转变量：`label_studio/core/views.py`（`LOGIN_PAGE_URL`）
- 前端应用挂载品牌配置：`web/apps/labelstudio/src/app/App.jsx`
- API 示例扩展：`web/apps/labelstudio/src/config/ApiConfig.example.js`
- 测试：
  - `label_studio/branding/tests/test_branding_api.py`

## 3. 验证结果

- 已执行回归集合（13 项）全部通过：
  - `label_studio/organizations/tests/test_workspaces_api.py`
  - `label_studio/tests/identity/*`
  - `label_studio/quality/tests/*`
  - `label_studio/collaboration/tests/*`
  - `label_studio/prompts_enterprise/tests/test_prompts_api.py`
  - `label_studio/branding/tests/test_branding_api.py`

## 4. 剩余差异与后续建议

当前 V3 已完成“系统启动 + 可验证闭环”的核心目标，仍建议在后续批次补强：

1. 审计日志域模型与审计检索 API（M1-06 全量）。
2. Compose/Helm 契约校验与企业部署文档联动（M1-07/M1-08 全量）。
3. Enterprise CI 门禁与 smoke pipeline 常态化（M1-09 全量）。
4. Prompts 与 Whitelabel 从占位配置演进为持久化组织级配置与更细粒度 RBAC。
