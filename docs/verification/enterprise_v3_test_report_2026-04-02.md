# Enterprise V3 测试报告（2026-04-02）

## 1. 测试范围

- M1 菜单补齐：组织-工作区入口与工作区 API 兼容性
- M2：
  - 身份：SAML / SCIM / LDAP
  - 质量：质量规则与一致性指标
  - 协作：评论与深链
  - 企业前端入口：Enterprise Settings / 角色矩阵
- M3：
  - Prompts 企业能力占位 API
  - Whitelabel 配置 API 与前端品牌挂载

## 2. 执行命令

```bash
.venv/bin/pytest \
  label_studio/organizations/tests/test_workspaces_api.py \
  label_studio/tests/identity/test_scim_api.py \
  label_studio/tests/identity/test_saml_login.py \
  label_studio/tests/identity/test_scim_idempotent.py \
  label_studio/tests/identity/test_ldap_auth.py \
  label_studio/quality/tests/test_quality_rules.py \
  label_studio/quality/tests/test_agreement_metrics.py \
  label_studio/collaboration/tests/test_comments_api.py \
  label_studio/collaboration/tests/test_deep_links.py \
  label_studio/prompts_enterprise/tests/test_prompts_api.py \
  label_studio/branding/tests/test_branding_api.py -q
```

```bash
.venv/bin/coverage erase
.venv/bin/coverage run -m pytest <同上测试集合> -q
.venv/bin/coverage report
```

## 3. 结果摘要

- 用例总数：13
- 通过：13
- 失败：0
- 阻塞：0

## 4. 覆盖率

- 本次覆盖率（coverage report TOTAL）：`49%`
- 新增企业模块覆盖率（核心）：
  - `branding/api.py`：100%
  - `prompts_enterprise/api.py`：100%
  - `quality/api.py`：93%
  - `collaboration/api.py`：87%
  - `identity/api.py`：74%

## 5. 已知问题与风险

1. 前端 `nx/biome` 校验在当前环境未执行（缺少 `web/node_modules` 依赖），本次以前后端集成测试为主。
2. Prompts / Whitelabel 当前为“占位可用”方案（会话级配置），后续建议升级为组织级持久化配置与审计链路。
