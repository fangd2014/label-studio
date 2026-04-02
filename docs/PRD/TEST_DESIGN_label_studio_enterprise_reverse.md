# Label Studio Enterprise 测试设计文档

## 1. 文档信息
- 文档类型：测试设计（Test Design / Test Strategy）
- 关联文档：`docs/PRD/PRD_label_studio_enterprise_reverse.md`、`docs/PRD/SDD_label_studio_enterprise_reverse.md`
- 适用仓库：`label-studio`
- 版本：`v1.0`
- 日期：`2026-04-01`

## 2. 测试目标
1. 验证企业版需求 `ENT-FR-001~030` 与部署子需求 `ENT-DEP-001~006` 的功能正确性与可回归性。
2. 验证主链路“租户治理 -> 身份接入 -> 任务分发 -> 质量闭环 -> 企业部署”端到端可用。
3. 验证多租户隔离、权限边界、身份同步、TLS/Secret、审计留痕等高风险场景。
4. 建立可持续自动化回归资产，支撑后续 Codex 持续开发与发布门禁。

## 3. 测试范围

### 3.1 范围内
1. 组织与工作空间隔离。
2. RBAC 与项目级角色体系。
3. SAML、SCIM、LDAP 身份集成。
4. 企业安全（TLS、审计、云存储身份能力）。
5. 标注工作流增强（自动分发、批量标注、过滤排序、深链协作）。
6. 质量与分析（审核流、一致性指标、低信任护栏、绩效看板）。
7. 企业部署体系（Compose、Helm、Secret/TLS、扩缩容、生命周期运维）。

### 3.2 范围外
1. 第三方平台本身稳定性（仅验证集成适配逻辑）。
2. UI 视觉主观评审。
3. 商务合同与收费系统。

## 4. 测试对象与层次

| 层次 | 目标 | 工具建议 | 通过标准 |
|---|---|---|---|
| 单元测试 | 规则引擎、权限决策、参数校验、TLS 配置解析 | `pytest` | 核心模块通过率 100% |
| API 集成测试 | 认证鉴权、角色权限、身份同步、工作流接口 | `pytest + APIClient` | P0/P1 API 零阻断缺陷 |
| 端到端测试 | 企业主流程与跨模块协同 | API 编排 + 最小 UI 验证 | 关键链路全绿 |
| 部署验证测试 | Compose/Helm 配置、Secret/TLS、扩缩容、重启回归 | Shell + k8s CLI + 自动化脚本 | 双环境部署验收通过 |
| 非功能测试 | 性能、并发、可靠性、安全性 | 压测 + 安全脚本 + 观测平台 | 指标达到准出阈值 |

## 5. 测试环境设计

### 5.1 环境分层
1. DEV：开发自测，验证单功能和分支逻辑。
2. SIT：系统集成测试，执行全链路回归。
3. UAT：业务验收与发布前确认。
4. PERF：性能与扩缩容专项环境。

### 5.2 环境矩阵
| 环境 | 部署方式 | 身份接入 | TLS | 目标 |
|---|---|---|---|---|
| ENV-A | Docker Compose | 本地账号/Mock IdP | 关闭 | 最小功能回归 |
| ENV-B | Docker Compose | SAML/SCIM Mock | 开启（Redis/PG） | 部署与安全回归 |
| ENV-C | Kubernetes + Helm | 企业 IdP 联调 | 开启（Redis/PG） | 生产拟态回归 |
| ENV-D | Kubernetes + Helm | 企业 IdP 联调 | 开启 | 压测与 HA 演练 |

### 5.3 基础依赖
1. PostgreSQL >= 13。
2. Redis >= 6（建议支持 ACL/TLS）。
3. 对象存储（S3/GCS/Azure 至少一类）。
4. 可控 ML Backend（含成功与失败场景）。
5. Webhook 接收端（可观测重试与 payload）。
6. IdP 模拟器或企业 IdP 沙箱（SAML/SCIM/LDAP）。

### 5.4 测试数据
1. 多租户数据：2 个组织、4 个工作空间、10+ 项目。
2. 角色数据：Owner/Admin/Manager/Reviewer/Annotator 全组合。
3. 任务数据：文本/图像/音频/视频混合，覆盖 10k/100k 规模。
4. 异常数据：坏证书、无效 Secret、越权请求、无效 SAML 断言。

## 6. 测试方法与策略

### 6.1 功能测试策略
1. 每个 `ENT-FR` 至少 1 组主用例与 1 组异常用例。
2. 每个 `ENT-DEP` 至少覆盖“正确配置”与“错误配置阻断”双路径。
3. 对高风险模块执行等价类、边界值和状态迁移覆盖。

### 6.2 集成测试策略
1. 身份链路：SAML 登录 -> SCIM 同步 -> RBAC 生效。
2. 业务链路：自动分发 -> 标注提交 -> 审核 -> 质量统计 -> 导出。
3. 部署链路：配置校验 -> 安装 -> 健康检查 -> 重启 -> 卸载。

### 6.3 回归策略
1. 每日回归集：P0 用例（租户隔离、鉴权、部署最小可用）。
2. 合并回归集：P0 + P1（身份同步、质量指标、核心部署升级）。
3. 周期全量回归：P0 + P1 + P2（含 Prompt/Whitelabel）。

### 6.4 安全策略
1. 认证与授权：未登录、越权、跨组织访问。
2. 密钥与证书：Secret 缺失、证书过期、证书链不完整。
3. 网络与输入：SSRF、防注入、配置注入风险。
4. 审计完整性：关键操作是否全量留痕、可检索、不可篡改。

### 6.5 性能与可靠性策略
1. `next task` 并发分配冲突率与吞吐。
2. 队列积压恢复时间与失败重试收敛时间。
3. 扩容前后 API P95/P99 延迟变化。
4. Pod 重启、节点故障、Redis/PG 短暂不可达时恢复能力。

## 7. 需求覆盖矩阵（ENT-FR/ENT-DEP -> 用例组）

| 需求 | 覆盖用例组 |
|---|---|
| ENT-FR-001 ~ 003 | TC-TEN-* |
| ENT-FR-004 ~ 006 | TC-RBAC-* |
| ENT-FR-007 ~ 009 | TC-IDM-* |
| ENT-FR-010 ~ 012 | TC-SEC-* |
| ENT-FR-013 ~ 016 | TC-AI-* |
| ENT-FR-017 ~ 020 | TC-QLT-* |
| ENT-FR-021 ~ 024 | TC-WF-* |
| ENT-FR-025 ~ 026 | TC-COL-* |
| ENT-FR-027 ~ 028 | TC-DEP-* |
| ENT-FR-029 ~ 030 | TC-OPS-* |
| ENT-DEP-001 ~ 006 | TC-DEP-CFG-* |
| ENT-NFR-001 ~ 005 | TC-NFR-* |

## 8. 核心测试用例设计（摘要）

### 8.1 多租户与权限
1. `TC-TEN-001`：跨组织资源访问阻断。
2. `TC-RBAC-001`：五角色矩阵权限校验。
3. `TC-RBAC-002`：多项目不同角色隔离。

### 8.2 身份集成
1. `TC-IDM-001`：SAML 登录成功与断言异常失败。
2. `TC-IDM-002`：SCIM 用户创建/更新/停用幂等。
3. `TC-IDM-003`：LDAP 不可达降级与可观测告警。

### 8.3 工作流与质量
1. `TC-WF-001`：自动分发 + 锁超时 + skip 队列策略。
2. `TC-WF-002`：批量标注权限控制与结果一致性。
3. `TC-QLT-001`：审核流状态迁移与回退。
4. `TC-QLT-002`：一致性指标计算准确性。
5. `TC-QLT-003`：低信任护栏自动暂停与恢复。

### 8.4 部署与运维
1. `TC-DEP-CFG-001`：Compose 必填参数缺失阻断。
2. `TC-DEP-CFG-002`：Helm 最小 values 成功安装。
3. `TC-DEP-CFG-003`：Secret 键错误导致部署失败并可定位。
4. `TC-DEP-CFG-004`：PostgreSQL/Redis TLS 证书链验证。
5. `TC-DEP-OPS-001`：Helm 重启后业务状态一致。
6. `TC-DEP-OPS-002`：扩缩容后吞吐提升与稳定性验证。

## 9. 自动化策略

### 9.1 自动化分层
1. API 自动化：覆盖全部 P0/P1 需求。
2. 配置自动化：Compose/Helm 参数、Secret/TLS 契约校验。
3. 部署自动化：安装、重启、卸载、健康检查流水线。
4. 性能自动化：关键接口和队列压力基线。

### 9.2 自动化优先级
1. 第一优先：`ENT-FR-001~012`, `ENT-FR-021~028`, `ENT-DEP-001~004`。
2. 第二优先：`ENT-FR-013~020`, `ENT-DEP-005~006`。
3. 第三优先：`ENT-FR-029~030`, P2 增值能力。

### 9.3 建议测试目录
1. `label_studio/tests/enterprise/test_tenant_isolation.py`
2. `label_studio/tests/enterprise/test_rbac_matrix.py`
3. `label_studio/tests/enterprise/test_identity_saml_scim.py`
4. `label_studio/tests/enterprise/test_quality_workflow.py`
5. `label_studio/tests/enterprise/test_deployment_contracts.py`
6. `label_studio/tests/enterprise/test_deployment_tls.py`
7. `label_studio/tests/enterprise/test_ha_scaling.py`

## 10. 缺陷管理策略
1. 分级：S0（阻断）/S1（高）/S2（中）/S3（低）。
2. 记录字段：模块、环境、前置条件、步骤、期望/实际、日志、配置快照。
3. 关闭标准：修复完成 + 自动化回归通过 + 无新增副作用。

## 11. 测试准入与准出

### 11.1 准入标准
1. 企业版 PRD/SDD 已冻结本轮范围。
2. 至少一个 Compose 环境和一个 K8s 环境可用。
3. 身份模拟环境与基础测试数据准备完成。
4. 测试脚本可获取所需 Secret/TLS 证书（测试专用）。

### 11.2 准出标准
1. P0 用例通过率 100%。
2. P1 用例通过率 >= 95%。
3. 无未关闭 S0/S1 缺陷。
4. `ENT-DEP-001~004` 完成双环境端到端验收。
5. 关键性能指标满足阈值：
6. `next task`、`tasks list`、`review submit`、`export create` 的 P95 达标。
7. 部署生命周期命令（install/restart/uninstall）可重复执行且结果一致。

## 12. 测试里程碑建议
1. M1（基础能力）：多租户、RBAC、身份接入、最小部署验收。
2. M2（流程能力）：自动分发、质量指标、协作能力、部署增强。
3. M3（稳态能力）：性能压测、故障演练、发布门禁固化。

## 13. 风险与应对
1. 风险：企业 IdP 不稳定导致身份链路波动。
2. 应对：引入 SAML/SCIM Mock 与重放样本，分离“协议正确性”和“联通性”测试。
3. 风险：证书与 Secret 配置复杂，环境故障率高。
4. 应对：建立部署前静态校验器与标准化错误码。
5. 风险：多队列扩容策略不当导致任务堆积。
6. 应对：按队列维度建立监控与自动化扩容策略回归。

## 14. 交付物清单
1. 测试设计文档（本文件）。
2. 企业版测试用例文档（后续）：`docs/PRD/TEST_CASES_label_studio_enterprise_reverse.md`。
3. 自动化测试脚本与执行报告（持续更新）。
4. 部署验收报告（Compose + Kubernetes 双环境）。
