# Label Studio Enterprise 产品需求文档（PRD）

## 1. 文档信息
- 文档类型：企业版需求 PRD（用于后续开发与测试）
- 适用仓库：`label-studio`
- 需求来源文件：`docs/source/guide/enterprise_features.md`
- 对应线上页面：[enterprise_features](https://labelstud.io/guide/enterprise_features)
- 文档版本：`v1.1`
- 编写日期：`2026-04-01`
- 文档语言：中文

## 2. 编写范围与约束
### 2.1 范围内
1. 仅整理 `enterprise_features.md` 中明确给出的企业版能力。
2. 输出可用于开发排期与测试设计的功能需求（FR）和非功能需求（NFR）。
3. 为后续企业版实现提供需求编号、优先级、验收标准与测试关注点。

### 2.2 范围外
1. 不包含具体代码实现方案和数据库表结构（由 SDD 承接）。
2. 不包含合同条款和商务价格细节（仅记录能力与 SLA 目标）。
3. 不包含超出 `enterprise_features.md` 描述的推测性功能。

## 3. 产品目标
1. 建立企业级多租户能力，满足组织隔离、权限治理、身份集成与合规审计。
2. 建立可规模化的标注生产流程，支持自动分发、质量管理与协作闭环。
3. 支持企业部署形态（Kubernetes、Docker Compose、高可用、性能扩展）。
4. 提供可追踪的需求与验收基线，便于后续开发与测试协同。

## 4. 角色定义
| 角色 | 权限范围 | 关键职责 |
|---|---|---|
| Owner | 组织级全量控制 | 组织治理、计费与全局配置 |
| Admin | 组织级管理 | 成员管理、组织设置与合规管理 |
| Manager | 工作空间级管理 | 项目创建、项目成员管理、流程推进 |
| Reviewer | 项目级质量角色 | 审核标注、反馈与质量控制 |
| Annotator | 项目级执行角色 | 执行标注任务与提交结果 |

## 5. 功能需求（Functional Requirements）

### 5.1 租户、组织与权限治理

#### ENT-FR-001 组织级数据隔离（P0）
- 需求描述：系统必须支持 Organization 作为顶层租户，组织间数据、项目、成员与配置完全隔离。
- 验收标准：
  1. 组织 A 用户不可查看或访问组织 B 的项目、成员、统计和资源。
  2. 跨组织 API 请求必须返回无权限或不可见结果。
  3. 组织级计费与使用统计按组织独立核算。
- 测试要点：跨组织越权访问、ID 猜测访问、并发访问隔离。

#### ENT-FR-002 工作空间管理（P0）
- 需求描述：系统必须支持 Workspace 作为组织内项目分组单元，支持按团队/部门隔离管理。
- 验收标准：
  1. 项目可归属到指定 Workspace。
  2. Workspace 级别可配置访问控制与管理权限委派。
  3. 同一 Workspace 内项目可共享资源（按权限）。
- 测试要点：工作空间授权继承、跨空间访问限制、资源共享边界。

#### ENT-FR-003 多租户 SaaS 与私有化兼容（P0）
- 需求描述：企业版须同时支持多租户 SaaS 架构与私有化/本地化部署模式。
- 验收标准：
  1. SaaS 模式下组织隔离满足租户边界要求。
  2. On-prem 模式可独立部署并具备同等企业能力。
  3. 功能开关不因部署模式导致核心能力缺失（除明确标注外）。
- 测试要点：SaaS 与 On-prem 功能一致性回归、部署模式切换验证。

#### ENT-FR-004 角色分级 RBAC（P0）
- 需求描述：系统应提供 Owner/Admin/Manager/Reviewer/Annotator 五级角色体系。
- 验收标准：
  1. 角色权限矩阵在组织层、工作空间层、项目层生效。
  2. 不同角色在项目管理、标注、审核、用户管理上的能力符合矩阵定义。
  3. 低权限用户不可执行高权限操作。
- 测试要点：权限矩阵全覆盖测试、拒绝路径测试、UI 与 API 一致性测试。

#### ENT-FR-005 项目级角色独立分配（P0）
- 需求描述：用户在不同项目中可拥有不同项目角色（如一个项目是 Annotator，另一个项目是 Reviewer）。
- 验收标准：
  1. 同一用户可在不同项目持有不同角色且互不干扰。
  2. 项目权限判断以项目角色为准，不被其他项目角色污染。
- 测试要点：多项目复合角色权限测试。

#### ENT-FR-006 用户生命周期管理（P0）
- 需求描述：支持企业级用户全生命周期管理：邀请、批量操作、活动监控、停用账号。
- 验收标准：
  1. 支持邀请制注册并可控制加入范围。
  2. 支持批量角色与工作空间成员关系操作。
  3. 停用账号后保留历史标注与审计记录。
- 测试要点：批量操作一致性、停用后历史可追溯性。

### 5.2 认证与身份管理

#### ENT-FR-007 SSO / SAML 2.0 集成（P0）
- 需求描述：系统需支持通过 SAML 2.0 与企业 IdP（如 Okta、Google SAML、Ping、AD）集成。
- 验收标准：
  1. 支持 SAML 登录与退出流程。
  2. 支持从 IdP 同步基础身份信息。
  3. 支持证书轮换与配置更新后不中断登录能力。
- 测试要点：SSO 登录链路、异常证书/时钟偏差处理、回退登录策略。

#### ENT-FR-008 SCIM 2.0 自动供给（P0）
- 需求描述：支持 SCIM 2.0 用户自动创建、更新、停用与组推送。
- 验收标准：
  1. Create/Update/Deactivate 流程可用。
  2. Push Groups 可映射工作空间和项目成员关系。
  3. SCIM 停用用户后，访问被立即撤销，历史数据保留。
- 测试要点：用户供给幂等性、批量推送一致性、停用即时生效。

#### ENT-FR-009 LDAP 集成（P1）
- 需求描述：支持 LDAP 认证接入，并保留本地角色管理能力。
- 验收标准：
  1. LDAP 用户可完成认证登录。
  2. LDAP 认证与本地 RBAC 权限控制可同时生效。
- 测试要点：LDAP 连接异常降级、目录字段映射兼容性。

### 5.3 安全与合规

#### ENT-FR-010 企业安全架构能力（P0）
- 需求描述：企业版需具备增强安全能力，包括 Redis TLS（含客户端证书）、IP allowlist/VPN、组织级隔离插件能力等。
- 验收标准：
  1. Redis 可启用 TLS 与证书认证链路。
  2. 云存储访问可配置 IP allowlist 或 VPN 限制策略。
  3. 自定义插件与前端定制在组织隔离边界内运行。
- 测试要点：传输加密有效性、网络访问控制、插件隔离测试。

#### ENT-FR-011 数据安全与审计日志（P0）
- 需求描述：系统需支持端到端 TLS/SSL 与全量审计日志能力。
- 验收标准：
  1. 关键组件通信链路可启用 TLS/SSL。
  2. 用户关键操作必须写入审计日志。
  3. 审计日志支持检索、导出与追责定位。
- 测试要点：日志完整性、日志不可抵赖性、审计检索性能。

#### ENT-FR-012 高级云存储身份能力（P1）
- 需求描述：支持 S3 IAM Role 与 GCS Workload Identity Federation 等企业级云存储认证方式。
- 验收标准：
  1. 支持 IAM Role 或静态凭证接入 S3。
  2. 支持 WIF 方式接入 GCS，避免硬编码密钥。
- 测试要点：临时凭证刷新、权限最小化策略验证。

### 5.4 智能标注与自动化能力

#### ENT-FR-013 AI 辅助能力开关与预测分数展示（P1）
- 需求描述：支持 AI 辅助功能开关及预测/置信分数展示。
- 验收标准：
  1. 可按项目启用或关闭 AI helper 工具。
  2. 标注界面可显示预测分数并参与决策。
- 测试要点：开关生效范围、预测分数显示一致性。

#### ENT-FR-014 自动化 Active Learning 闭环（P1）
- 需求描述：支持“标注->Webhook->模型 fit()->predict()->下一任务”闭环。
- 验收标准：
  1. 标注提交后可触发模型训练或更新回调。
  2. 新预测可回流到后续任务并参与采样排序。
  3. 闭环失败可重试并记录状态。
- 测试要点：Webhook 可靠性、训练失败补偿、预测回流正确性。

#### ENT-FR-015 Prompts 能力（附加收费，P2）
- 需求描述：支持内置 Prompts 模块，包括模板、内联生成、预标注、任务生成。
- 验收标准：
  1. 支持定义 Prompt 输入/输出/模型参数模板。
  2. 支持在标注界面直接运行 Prompt。
  3. 支持基于 Prompt 输出创建任务或预填标签。
- 测试要点：Prompt 模板复用、调用链路稳定性、权限隔离。

#### ENT-FR-016 插件扩展框架（P1）
- 需求描述：支持项目级 JavaScript 插件扩展，支持事件驱动与外部 API 集成。
- 验收标准：
  1. 支持任务加载、切换等事件触发逻辑。
  2. 支持验证、覆盖层、上下文逻辑等 UI 扩展。
  3. 支持插件测试与预览能力。
- 测试要点：插件生命周期、异常隔离、性能影响评估。

### 5.5 质量控制与分析

#### ENT-FR-017 质量控制流程（P0）
- 需求描述：支持自动校验、审核工作流、一致性控制等质量机制。
- 验收标准：
  1. 支持自动校验规则。
  2. 支持可配置审核流程（通过、驳回、反馈）。
  3. 支持质量门禁防止低质量数据进入发布阶段。
- 测试要点：校验规则触发、审核流状态迁移、异常闭环。

#### ENT-FR-018 一致性指标体系（P1）
- 需求描述：支持 30+ 内置互标一致性指标（IoU、编辑距离、F1/Precision/Recall 等）。
- 验收标准：
  1. 不同标注类型可选择适配指标。
  2. 指标结果可实时展示并支持矩阵视图。
- 测试要点：指标计算正确性、跨任务聚合准确性。

#### ENT-FR-019 低信任标注员护栏（P1）
- 需求描述：支持低信任标注员暂停和标注上限控制。
- 验收标准：
  1. 可根据质量规则手动或自动暂停标注员。
  2. 可设置每用户标注上限防止异常产出。
- 测试要点：自动暂停阈值触发、恢复流程、上限拦截。

#### ENT-FR-020 项目与人员绩效看板（P1）
- 需求描述：支持项目看板与标注员看板，追踪任务量、耗时、审核周转、分布等指标。
- 验收标准：
  1. 项目看板支持日期筛选和可视化重排。
  2. 标注员看板支持个人效率与质量分析。
  3. 看板指标与底层数据统计保持一致。
- 测试要点：指标口径一致性、筛选准确性、权限可见范围。

### 5.6 项目与标注流程增强

#### ENT-FR-021 企业版项目设置（P0）
- 需求描述：企业版应提供 OSS 不具备的项目设置能力（如 Workspace、Proxy、任务分发、Task Reservation、Skip Queue、Sampling、Review/Quality 高级项、项目成员角色管理、Reset Cache 等）。
- 验收标准：
  1. 企业版设置项在项目配置页可见并可保存。
  2. 配置生效后影响任务分发、审核流与质量策略。
  3. 与 OSS 共享设置项保持兼容，不破坏已有流程。
- 测试要点：设置项可见性、保存幂等性、配置生效路径回归。

#### ENT-FR-022 批量标注（P1）
- 需求描述：支持在 Data Manager 中对多任务进行批量标注，覆盖图像、文本、音频、视频等主要类型。
- 验收标准：
  1. 支持批量选择任务并应用统一标注。
  2. 受角色权限控制（Reviewer/Manager/Admin/Owner）。
  3. 支持文档中列出的主要控制标签类型。
- 测试要点：批量一致性、回滚策略、角色拦截。

#### ENT-FR-023 自动分发与队列策略（P0）
- 需求描述：支持 Auto distribution、重叠标注、任务锁超时、跳过队列策略。
- 验收标准：
  1. 项目发布后标注员可立即获得任务。
  2. 支持配置最小标注重叠数量。
  3. 支持配置任务锁定超时与 Skip Queue 行为（重排/忽略等）。
- 测试要点：任务领取公平性、锁超时释放、跳过队列策略正确性。

#### ENT-FR-024 标注结果过滤与排序（P1）
- 需求描述：Data Manager 支持字段级过滤、任务排序与复合过滤。
- 验收标准：
  1. 支持按标签结果、区域属性、审核动作过滤。
  2. 支持按创建时间、预测置信度、元数据排序。
  3. 支持多条件组合筛选。
- 测试要点：过滤准确率、组合条件逻辑、性能表现。

### 5.7 协作能力

#### ENT-FR-025 评论与通知（P1）
- 需求描述：支持注释区域/字段级线程评论与通知。
- 验收标准：
  1. 支持评论、回复、查看线程。
  2. 角色权限决定评论删除/解决能力。
  3. 新评论和回复可触发通知。
- 测试要点：评论权限、通知触达、并发回复一致性。

#### ENT-FR-026 深链能力（P1）
- 需求描述：支持生成指向特定任务/标注/区域/字段的深链接。
- 验收标准：
  1. 深链可直接打开目标上下文。
  2. 无权限用户访问深链时应被拒绝。
- 测试要点：链接稳定性、权限校验、过期策略（如有）。

### 5.8 部署、可用性与企业服务

#### ENT-FR-027 企业部署模式（P0）
- 需求描述：支持 Kubernetes 与 Docker Compose 企业部署，且部署配置可参数化、可审计、可复现。
- 验收标准：
  1. Docker Compose 拓扑至少包含 `nginx`、`app`、`rqworkers_low`、`rqworkers_default`、`rqworkers_high`、`rqworkers_critical` 六类服务。
  2. Compose 支持外部 PostgreSQL/Redis、License 文件挂载、Worker 队列拆分。
  3. Compose 镜像仓库可配置，默认值采用当前安装指南中的 `heartexlabs/label-studio-enterprise`，并兼容企业功能页中的仓库写法差异。
  4. Compose 通过 `env.list` 注入关键配置，至少覆盖 `LICENSE`、`LABEL_STUDIO_HOST`、`POSTGRE_*`、`REDIS_*`。
  5. K8s 部署支持 Helm 3，且 `enterprise.enabled=true` 与 `enterprise.enterpriseLicense.secretName/secretKey` 生效。
  6. K8s 部署支持外部 PostgreSQL/Redis 接入，并可通过 `postgresql.enabled=false`、`redis.enabled=false` 显式关闭内置依赖。
  7. 通过 `helm install <RELEASE_NAME> heartex/label-studio -f ls-values.yaml` 可完成安装，且 `kubectl get pods` 所有核心 Pod 达到 Ready。
- 测试要点：安装成功率、配置正确性、证书与 Secret 加载、升级回归。

#### ENT-FR-028 高可用与性能扩展（P0）
- 需求描述：支持多副本、队列扩展、存储代理、查询优化、Redis 异步任务体系，并提供可落地的容量规划与运维控制面。
- 验收标准：
  1. 支持 `app.replicas` 与 `rqworker.queues.{low,default,high,critical}.replicas` 独立扩缩容。
  2. 默认队列扩容策略可配置，且支持 `default` 队列副本数高于其他队列（建议 4 倍）以匹配主任务负载。
  3. 支持 PostgreSQL/Redis 高可用与 TLS 接入（含客户端证书模式）。
  4. K8s 部署支持应用与 Nginx 探针配置（如 `/version`、`/nginx_health`）并可通过参数覆盖。
  5. 支持标准运维重启动作：`kubectl rollout restart deployment/<RELEASE_NAME>-ls-rqworker` 与 `...-ls-app`。
  6. 生产部署支持启用 `SSRF_PROTECTION_ENABLED=true` 的安全基线。
  7. 大项目场景下查询与任务处理性能可接受。
- 测试要点：故障切换、扩容压测、队列堆积恢复能力、探针误判率、TLS 握手稳定性。

### 5.8.1 部署子需求（可用于 Codex 编码实现）

#### ENT-DEP-001 Docker Compose 编排契约（P0）
- 需求描述：提供可直接落地的 Compose 编排模板与参数契约。
- 验收标准：
  1. 服务拓扑、命令、挂载目录与队列名称满足 `install_enterprise_docker.md` 基线。
  2. `license.txt` 必须以只读方式挂载到 `/label-studio-enterprise/license.txt`。
  3. 缺失 License、PostgreSQL 或 Redis 连接参数时，部署前检查失败并输出明确错误信息。
- 测试要点：编排完整性、参数缺失校验、错误提示可读性。

#### ENT-DEP-002 Kubernetes Helm 值契约（P0）
- 需求描述：定义企业版 `ls-values.yaml` 最小可用键集合，便于模板化生成。
- 验收标准：
  1. 最小可用键至少包含：`global.image.*`、`global.imagePullSecrets`、`global.pgConfig.*`、`global.redisConfig.*`、`enterprise.enabled`、`enterprise.enterpriseLicense.*`、`app.ingress.*`、`app.replicas`、`rqworker.queues.*.replicas`。
  2. 支持通过 Secret 坐标引用数据库与 Redis 凭据，不在配置文件明文硬编码敏感信息。
  3. `postgresql.enabled=false` 与 `redis.enabled=false` 在外部依赖模式下必须可配置。
- 测试要点：最小 values 验证、Secret 引用有效性、内置依赖开关行为。

#### ENT-DEP-003 Secret 管理契约（P0）
- 需求描述：统一部署密钥和证书 Secret 规范，支持 Registry、License、TLS 证书三类密钥。
- 验收标准：
  1. 支持镜像拉取 Secret（如 `heartex-pull-key`）与 License Secret（如 `lse-license`）。
  2. 支持 PostgreSQL/Redis TLS Secret，包含 `ca.crt`、`client.crt`、`client.key` 键位映射。
  3. Secret 名称、键名错误时可在部署前/部署期被识别并可追踪定位。
- 测试要点：Secret 缺失与错配测试、证书热更新回归。

#### ENT-DEP-004 TLS 与连接安全契约（P0）
- 需求描述：定义 PostgreSQL/Redis 连接 TLS 参数契约，满足企业合规要求。
- 验收标准：
  1. PostgreSQL 支持 `verify-ca` / `verify-full`，且推荐 `verify-full`。
  2. Redis 支持 `redisSslCertReqs` 与证书路径映射配置。
  3. TLS 开启后，业务路径与异步队列路径均能稳定运行。
- 测试要点：双向证书链验证、证书失效/过期处理、TLS 回归。

#### ENT-DEP-005 运维命令与生命周期契约（P1）
- 需求描述：统一安装、重启、卸载的标准运维命令和验收动作。
- 验收标准：
  1. 安装命令、重启命令、卸载命令与文档保持一致并可自动化执行。
  2. 每次部署后必须执行 `kubectl get pods` 或等价健康检查。
  3. 重启动作不应破坏持久化数据与许可状态。
- 测试要点：重复部署幂等性、重启后状态一致性、卸载残留检查。

#### ENT-DEP-006 容量规划与扩展建议契约（P1）
- 需求描述：将容量规划建议固化为可配置策略，用于压测和扩缩容。
- 验收标准：
  1. 支持基于并发标注规模调整 `app.resources` 与 `rqworker.resources`。
  2. 支持按可用区数量设置副本下限（生产环境）。
  3. 支持队列级副本策略并可通过配置变更快速生效。
- 测试要点：压力下扩容收敛时间、资源瓶颈定位、配置变更生效时延。

#### ENT-FR-029 Whitelabeling（附加收费，P2）
- 需求描述：支持自定义品牌、域名与登录页跳转。
- 验收标准：
  1. 支持 logo、颜色、样式定制。
  2. 支持自定义域名。
  3. 支持登录页重定向配置。
- 测试要点：品牌配置生效、域名证书、重定向安全性。

#### ENT-FR-030 企业支持与专业服务（P1）
- 需求描述：支持 99.9% Uptime SLA、高级技术支持、CSM、实施与标注服务。
- 验收标准：
  1. 明确 SLA 指标与统计口径。
  2. 支持标准化支持流程与升级路径。
  3. 支持实施与运维服务协同机制。
- 测试要点：SLA 统计可验证性、告警与工单闭环流程。

## 6. 非功能需求（NFR）

### ENT-NFR-001 可用性与可靠性
- 目标：达到企业支持承诺的可用性目标（99.9% Uptime）。
- 要求：关键组件具备故障转移能力，任务与队列具备重试机制。

### ENT-NFR-002 安全与合规
- 要求：关键链路 TLS 加密、审计日志留痕、身份系统可对接企业目录。
- 要求：满足企业环境的网络边界和部署约束（含 air-gapped 场景）。

### ENT-NFR-003 性能与扩展
- 要求：支持大规模项目数据管理，查询性能在可接受范围内。
- 要求：支持横向扩展（应用副本、队列副本、存储代理）。

### ENT-NFR-004 可观测性
- 要求：核心流程（标注、审核、分发、回调、导出）具备可监控与可审计能力。

### ENT-NFR-005 可配置性与可维护性
- 要求：企业版能力应通过配置项控制，便于环境迁移与版本升级。

## 7. 测试需求与用例矩阵（用于后续测试设计）

| 测试用例ID | 覆盖需求 | 核心场景 | 预期结果 | 优先级 |
|---|---|---|---|---|
| TC-ENT-001 | ENT-FR-001/002/003 | 多组织多工作空间并发访问 | 数据与权限完全隔离 | P0 |
| TC-ENT-002 | ENT-FR-004/005 | 5 角色矩阵 + 多项目混合角色 | 权限严格按角色矩阵执行 | P0 |
| TC-ENT-003 | ENT-FR-006 | 邀请、批量授权、停用账号 | 流程成功且历史可追溯 | P0 |
| TC-ENT-004 | ENT-FR-007 | SAML SSO 登录与登出 | 登录链路稳定，权限正确映射 | P0 |
| TC-ENT-005 | ENT-FR-008 | SCIM 创建/更新/停用/组推送 | 用户状态与成员关系自动同步 | P0 |
| TC-ENT-006 | ENT-FR-010/011 | TLS + 审计日志覆盖测试 | 关键操作均可审计，链路加密有效 | P0 |
| TC-ENT-007 | ENT-FR-012 | S3 IAM 与 GCS WIF 接入 | 无硬编码密钥，访问稳定 | P1 |
| TC-ENT-008 | ENT-FR-014 | 标注触发 fit/predict 闭环 | 回调成功，预测可回流下一任务 | P1 |
| TC-ENT-009 | ENT-FR-015/016 | Prompt 与插件扩展场景 | 扩展能力可用且权限隔离 | P2 |
| TC-ENT-010 | ENT-FR-017/018/019 | 自动校验 + 一致性指标 + 低信任护栏 | 质量规则正确触发并可度量 | P0 |
| TC-ENT-011 | ENT-FR-020 | 项目/标注员看板指标一致性 | 指标口径一致，过滤有效 | P1 |
| TC-ENT-012 | ENT-FR-021/023 | 企业项目设置 + 自动分发 | 设置生效，分发和锁队列逻辑正确 | P0 |
| TC-ENT-013 | ENT-FR-022/024 | 批量标注 + 过滤排序 | 批量操作正确，筛选准确 | P1 |
| TC-ENT-014 | ENT-FR-025/026 | 评论通知 + 深链协作 | 消息可达，深链定位准确且有权限控制 | P1 |
| TC-ENT-015 | ENT-FR-027/028 | K8s/Compose 部署 + HA + 扩容压测 | 部署稳定，故障可恢复，性能可接受 | P0 |
| TC-ENT-016 | ENT-FR-029 | Whitelabel 配置变更 | 品牌与域名配置正确生效 | P2 |
| TC-ENT-017 | ENT-FR-030 | SLA 统计与支持流程演练 | SLA 指标可验证，支持流程可闭环 | P1 |
| TC-ENT-018 | ENT-DEP-001 | Compose 拓扑与环境变量校验 | 缺参阻断部署，正确配置可启动 | P0 |
| TC-ENT-019 | ENT-DEP-002 | `ls-values.yaml` 最小可用集验证 | Helm 安装成功且核心功能可用 | P0 |
| TC-ENT-020 | ENT-DEP-003/004 | Secret + TLS 证书链路验证 | 证书正确加载，连接稳定且可观测 | P0 |
| TC-ENT-021 | ENT-DEP-005 | Helm 安装/重启/卸载生命周期测试 | 生命周期命令可重复执行且状态正确 | P1 |
| TC-ENT-022 | ENT-DEP-006 | 队列与副本扩缩容压测 | 扩容生效且吞吐提升符合预期 | P1 |

## 8. 开发迭代建议（里程碑）

### 里程碑 M1：企业基础能力（P0）
- 覆盖：ENT-FR-001~011、021、023、027、028、ENT-DEP-001~004。
- 目标：先打通企业版“可用+可管+可部署”最小闭环。

### 里程碑 M2：质量与效率增强（P1）
- 覆盖：ENT-FR-012~014、016~020、022、024~026、030、ENT-DEP-005~006。
- 目标：提升标注质量、运营效率和协作效率。

### 里程碑 M3：增值能力（P2）
- 覆盖：ENT-FR-015、029。
- 目标：补齐 Prompts/Whitelabel 等商业增强能力。

## 9. 发布验收退出标准
1. 全部 P0 需求通过功能、权限、安全、部署回归测试。
2. P0 相关关键路径无阻塞级缺陷（严重级/致命级为 0）。
3. 多租户隔离、SSO/SCIM、审计日志、自动分发、HA 压测报告齐备。
4. 测试用例矩阵中 P0 项全部通过，P1/P2 有明确残留风险与处理计划。
5. 部署子需求 `ENT-DEP-001~004` 在至少一个 Compose 环境和一个 Kubernetes 环境中完成端到端验收。

## 10. 需求追溯来源
- 主来源：`docs/source/guide/enterprise_features.md`
- 部署细化补充来源：
  1. `docs/source/guide/install_enterprise_docker.md`
  2. `docs/source/guide/install_enterprise_k8s.md`
  3. `docs/source/guide/helm_values.md`
  4. [Enterprise deployment options](https://labelstud.io/guide/enterprise_features#Enterprise-deployment-options)
- 对应章节：
  1. Organizations and Workspaces
  2. Multi-tenant SaaS architecture
  3. User management and role-based access control
  4. Authentication and identity management
  5. Advanced security features
  6. Advanced labeling & evaluation workflows
  7. Quality workflows and analytics
  8. Project Management
  9. Annotation workflow features
  10. Collaboration features
  11. Enterprise deployment options
  12. Performance and scalability features
  13. Whitelabeling
  14. Enterprise support & professional services

## 11. 面向 Codex 的开发输入与交付约束

### 11.1 开发输入（必须）
1. `enterprise_features.md` 的部署章节作为能力范围边界。
2. `install_enterprise_docker.md` 作为 Compose 编排基线。
3. `install_enterprise_k8s.md` 与 `helm_values.md` 作为 Helm 键与 Secret 契约基线。

### 11.2 建议代码交付物（可直接拆任务）
1. 部署模板：`docker-compose.enterprise.yml`（或同等模板文件）。
2. K8s 模板：`ls-values.enterprise.yaml`（最小可用 + 生产建议两套）。
3. 参数校验脚本：对 `LICENSE`、`POSTGRE_*`、`REDIS_*`、`enterpriseLicense`、`imagePullSecrets` 进行启动前校验。
4. TLS 配置模块：统一 PostgreSQL 与 Redis TLS 参数注入逻辑（Compose 与 Helm 双路径）。
5. 运维脚本：安装、重启、健康检查、回滚/卸载脚本化封装。

### 11.3 Definition of Done（DoD）
1. `ENT-FR-027`、`ENT-FR-028`、`ENT-DEP-001~004` 全量通过自动化测试。
2. 同一套配置可以在测试环境重复部署至少 3 次且结果一致。
3. 关键失败路径（缺 Secret、证书错误、DB 不可达、Redis 不可达）有明确错误码或可检索日志。
4. 交付文档包含参数说明、样例配置、常见故障排查步骤。
