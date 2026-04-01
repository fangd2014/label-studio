# Label Studio OSS 产品需求文档（PRD）

## 1. 文档信息
- 文档类型：反向 PRD（基于现有代码实现梳理）
- 适用仓库：`label-studio`
- 文档版本：`v1.0`
- 编写日期：`2026-04-01`
- 文档语言：中文

## 2. Problem（要解决的问题）
机器学习项目在数据标注环节通常存在以下痛点：

- 数据源多样（文本、图像、音频、视频、HTML、时序）导致工具碎片化。
- 标注规范经常变化，传统工具难以快速适配新任务。
- 多人协作时任务分配、进度追踪、质量控制和一致性管理成本高。
- 模型预标注与人工复核流程割裂，难以形成持续优化闭环。
- 标注数据导入导出、云存储接入、API 自动化能力不足。

Label Studio 的产品目标是提供一套可配置、可协作、可扩展的数据标注平台，覆盖从项目创建、任务导入、标注执行、质量管理到导出与集成的完整流程。

## 3. PoC Notes（代码实现依据）
本 PRD 主要基于以下模块反向整理：

- 核心域模型：`label_studio/projects/models.py`、`label_studio/tasks/models.py`
- 项目与任务 API：`label_studio/projects/api.py`、`label_studio/tasks/api.py`
- 数据管理：`label_studio/data_manager/api.py`、`label_studio/data_manager/actions/*`
- 数据导入导出：`label_studio/data_import/*`、`label_studio/data_export/*`
- 存储、ML、Webhook：`label_studio/io_storages/*`、`label_studio/ml/*`、`label_studio/webhooks/*`
- 用户与组织：`label_studio/users/*`、`label_studio/organizations/*`
- 前端信息架构：`web/apps/labelstudio/src/pages/*`
- 会话与认证：`label_studio/session_policy/*`、`label_studio/jwt_auth/*`

## 4. 产品目标与非目标
### 4.1 产品目标
- 支持多模态数据标注与统一项目管理。
- 支持多人协作、任务流转、标注历史与基础质量控制。
- 支持模型预测接入，实现预标注、交互式建议、训练触发。
- 支持 API 化导入导出与云存储集成，便于流水线自动化。
- 提供可观测性（健康检查、版本信息、指标挂载点）和基础安全能力。

### 4.2 非目标（当前 OSS 范围）
- 不覆盖企业版专属能力（如部分高级模型供应商、企业权限细粒度策略等）。
- 不提供完整工作流编排系统（仅提供动作 API 与基础异步任务能力）。

## 5. 用户角色与用户故事
### 5.1 角色
- 组织管理员：管理组织成员、项目配置、系统级策略。
- 项目负责人：创建项目、配置标注界面、导入任务、管理导出与集成。
- 标注员：执行标注、保存草稿、查看说明、提交或跳过任务。
- 算法工程师：接入 ML Backend、触发训练、导入/管理预测版本。
- 平台集成方：通过 REST API 与 Webhook 对接外部系统。

### 5.2 用户故事
- 作为项目负责人，我希望快速创建项目并配置标注界面，以便团队尽快开始标注。
- 作为标注员，我希望系统自动分配下一个可标注任务，并支持草稿与跳过，以便连续高效工作。
- 作为算法工程师，我希望把模型预测接入标注流程并回收人工结果，以便提升模型迭代效率。
- 作为平台集成方，我希望通过 API 批量导入/导出任务并订阅事件，以便自动化数据流水线。

## 6. 范围与信息架构
### 6.1 一级模块
- 组织与用户
- 项目管理
- 数据导入
- 数据管理与标注
- 质量与一致性
- 机器学习与预测
- 存储接入
- 数据导出
- Webhook 与开放 API
- 认证与会话策略

### 6.2 前端主要页面
- 项目列表：`/projects`
- 项目数据管理：`/projects/:id/data`
- 项目设置：`/projects/:id/settings/*`
- 组织成员：`/organization`
- 账户设置：`/settings`

## 7. 功能需求（Functional Requirements）

### FR-01 组织与成员管理
- 系统应支持组织创建、组织信息查询与更新。
- 系统应支持组织成员列表查询（分页），并可附带成员创建/贡献项目信息。
- 系统应支持成员软删除（不可删除自己）。
- 系统应支持邀请链接生成与重置。
- 验收标准：
  - 可通过 `GET/POST /api/organizations/`、`GET /api/organizations/{id}/memberships`、`DELETE /api/organizations/{id}/memberships/{user}` 完成组织与成员管理。

### FR-02 用户与账号管理
- 系统应支持登录、注册、登出、个人资料维护。
- 系统应支持获取当前用户信息（WhoAmI）与 API Token 重置。
- 系统应支持用户自定义热键配置。
- 验收标准：
  - `GET /api/current-user/whoami` 返回当前账号信息。
  - `POST /api/current-user/reset-token` 可重置 token。

### FR-03 项目生命周期管理
- 系统应支持项目创建、查询、更新、删除。
- 项目需支持草稿态与发布态（`is_draft` / `is_published`）。
- 项目名称应有长度约束（3~50）。
- 项目应支持颜色、采样策略、重叠标注策略、跳过策略等核心配置。
- 验收标准：
  - `GET/POST /api/projects/`、`GET/PATCH/DELETE /api/projects/{id}` 可完成项目生命周期管理。

### FR-04 标注界面配置（Label Config）
- 系统应支持 XML 标注配置的创建、校验和解析缓存。
- 系统应支持按项目校验配置与既有数据兼容性（strict 校验）。
- 系统应支持根据配置生成 sample task。
- 验收标准：
  - `POST /api/projects/validate` 与 `POST /api/projects/{id}/validate` 可返回校验结果。
  - `POST /api/projects/{id}/sample-task` 可返回示例任务。

### FR-05 数据导入
- 系统应支持通过 JSON body、文件上传、URL 三种方式导入任务。
- 系统应支持导入预测（predictions）和 reimport。
- 系统应支持异步导入状态查询（import/reimport status）。
- 系统应对任务总量和上传大小进行限制校验。
- 验收标准：
  - 主要接口：`POST /api/projects/{id}/import`、`POST /api/projects/{id}/reimport`、`GET /api/projects/{id}/imports/{import_id}`。
  - 服务端默认上限：`TASKS_MAX_NUMBER=1,000,000`，`DATA_UPLOAD_MAX_MEMORY_SIZE` 默认约 250MB。

### FR-06 导入文件格式支持
- 系统应支持 CSV/TSV/TXT/JSON 任务解析。
- 系统应支持图像、音视频、HTML/XML/PDF 等资产型文件作为任务数据源。
- 系统应校验扩展名白名单，并对跨文件数据列一致性进行校验。
- 验收标准：
  - 支持扩展名由 `SUPPORTED_EXTENSIONS` 控制（含 `.csv/.tsv/.txt/.json/.jpg/.png/.mp3/.wav/.mp4/.pdf` 等）。

### FR-07 任务查询与数据管理（Data Manager）
- 系统应支持视图（View）创建、更新、删除、重排和批量重置。
- 系统应支持任务列表分页、过滤、排序、选中集操作。
- 系统应返回聚合统计：总任务数、总标注数、总预测数。
- 验收标准：
  - `GET /api/dm/views`、`POST /api/dm/views/order`、`DELETE /api/dm/views/reset`。
  - `GET /api/tasks` 与 `GET /api/dm/*` 支持数据管理请求。

### FR-08 任务领取与队列策略
- 系统应支持“下一任务”分配，并考虑：
  - 任务锁（lock）
  - 采样策略（Sequential/Uniform/Uncertainty）
  - 重叠优先（show_overlap_first）
  - 跳过队列策略（REQUEUE_FOR_ME/REQUEUE_FOR_OTHERS/IGNORE_SKIPPED）
  - 草稿延期与历史回溯
- 验收标准：
  - `GET /api/projects/{id}/next` 可返回下一个任务及队列信息。

### FR-09 标注、草稿与预测管理
- 系统应支持任务下标注 CRUD。
- 系统应支持草稿创建、编辑、删除，以及 annotation 转 draft。
- 系统应支持预测 CRUD，并支持按任务/项目过滤。
- 系统应支持 Ground Truth 唯一性与跳过合法性校验。
- 验收标准：
  - `POST /api/tasks/{id}/annotations`、`GET/PATCH/DELETE /api/annotations/{id}`。
  - `GET/POST /api/tasks/{id}/drafts`、`POST /api/annotations/{id}/convert-to-draft`。

### FR-10 数据管理动作（Actions）
- 系统应支持在选中任务集上执行批量动作：
  - 拉取预测
  - 预测转标注
  - 删除任务/标注/预测
  - 去重任务
- 系统应支持动作表单动态加载。
- 验收标准：
  - `GET /api/dm/actions`、`POST /api/dm/actions?id=<action_id>`、`GET /api/dm/actions/{action_id}/form`。

### FR-11 质量与统计
- 系统应支持项目 summary 聚合（数据列、已创建标签、标注结构统计）。
- 系统应支持按任务返回标签分布（agreement endpoint）。
- 系统应支持 summary 缓存重置与重算。
- 验收标准：
  - `GET /api/projects/{id}/summary`、`POST /api/projects/{id}/summary/reset`、`GET /api/tasks/{id}/agreement`。

### FR-12 机器学习集成
- 系统应支持 ML Backend 接入（CRUD、健康检查、配置校验）。
- 系统应支持模型训练触发、测试预测、交互式预测。
- 系统应支持项目级模型版本管理，并可删除某模型版本预测。
- 验收标准：
  - `GET/POST /api/ml`、`PATCH/DELETE /api/ml/{id}`、`POST /api/ml/{id}/train`、`POST /api/ml/{id}/interactive-annotating`。

### FR-13 预标注与模型联动
- 系统应支持项目设置“使用预测进行预标注”。
- 系统应支持选择模型版本，并在任务加载时按配置获取预测。
- 系统应支持“提交标注时触发训练”开关。
- 验收标准：
  - 项目字段 `show_collab_predictions`、`model_version`、`min_annotations_to_start_training` 生效。

### FR-14 存储集成（Source/Target）
- 系统应支持 Source/Target 双向存储配置。
- 系统应支持 S3、GCS、Azure Blob、Redis、Local Files（受配置控制）。
- 系统应支持存储连接校验、文件浏览、同步、URI 解析/预签名。
- 验收标准：
  - `GET/POST/PATCH/DELETE /api/storages/*` 系列接口可管理存储。
  - `.../sync`、`.../validate`、`.../files`、`/tasks/{id}/resolve` 可用。

### FR-15 数据导出
- 系统应支持同步导出（兼容旧接口）和异步导出快照。
- 系统应支持导出格式查询、导出任务过滤、导出转换与下载。
- 系统应支持导出状态跟踪（created/in_progress/failed/completed）。
- 验收标准：
  - 同步：`GET /api/projects/{id}/export`。
  - 异步：`POST /api/projects/{id}/exports/`、`GET /api/projects/{id}/exports/*`。

### FR-16 Webhook 集成
- 系统应支持组织级/项目级 Webhook 管理。
- 系统应支持按动作订阅（项目、任务、标注、标签链接等）。
- 系统应支持附加请求头与开关控制（是否发送 payload、是否激活）。
- 验收标准：
  - `GET/POST /api/webhooks/`、`PATCH/DELETE /api/webhooks/{id}`、`GET /api/webhooks/info`。

### FR-17 自定义标签管理
- 系统应支持自定义标签（Label）及与项目配置的链接（LabelLink）。
- 系统应支持标签批量替换已存在标注结果。
- 验收标准：
  - `api/labels/*`、`api/label-links/*`、`POST /api/labels/bulk` 可用。

### FR-18 会话与认证策略
- 系统应支持 Session 超时策略（组织级）查询与更新。
- 系统应支持 JWT 设置、Refresh/Blacklist/Rotate 流程。
- 系统应支持 API token 列表与创建。
- 验收标准：
  - `GET/PATCH /api/session-policy/`、`api/jwt/settings`、`api/token/*` 可用。

### FR-19 有限状态机（FSM）与审计
- 系统应支持 Task/Annotation/Project 状态历史查询。
- 系统应支持手动执行可手动触发的状态迁移。
- 验收标准：
  - `GET /api/fsm/entities/{entity}/{id}/history`
  - `POST /api/fsm/entities/{entity}/{id}/transition/`

### FR-20 可运维能力
- 系统应提供健康检查、版本信息与 API 文档入口。
- 系统应提供 metrics 挂载点和错误追踪接入能力。
- 验收标准：
  - `GET /health/`、`GET /api/version/`、`/docs/api/schema/*` 可访问。

## 8. 非功能需求（NFR）

### NFR-01 性能与容量
- 项目列表分页默认 30，最大 100。
- 任务列表分页默认 100，最大值由 `TASK_API_PAGE_SIZE_MAX` 控制。
- 组织成员分页默认 20，支持 `page_size=-1` 的全量模式。
- 导入支持流式 JSON 解析和批处理，降低大文件峰值内存。

### NFR-02 安全
- 默认要求认证访问（DRF `IsAuthenticated` + 对象级权限检查）。
- 支持 Session + JWT + API Token 机制。
- 支持外部 URL SSRF 防护与可配置 SSL 证书校验。
- 支持上传扩展名与文件大小限制。

### NFR-03 一致性与可靠性
- 关键聚合统计通过 summary/counter 更新与异步补偿任务保障一致性。
- 导入/导出/去重等耗时操作支持异步执行与状态轮询。
- Task lock 与 overlap 约束用于减少并发冲突。

### NFR-04 可扩展性
- 通过 feature flags 控制灰度功能。
- 通过动作注册机制扩展 Data Manager 批处理动作。
- 通过存储 provider、ML backend 接口扩展外部能力。

## 9. 核心数据对象
- Organization：组织主体，承载成员与项目。
- User：用户主体，具备 active_organization 与 token。
- Project：任务容器，承载标注配置、采样策略、模型配置。
- Task：待标注数据单元，包含 data/meta/overlap/is_labeled。
- Annotation / Draft / Prediction：人工结果、草稿、模型预测。
- ProjectSummary：聚合统计缓存对象。
- Import/Reimport/Export：异步作业与状态追踪对象。
- Storage：外部存储连接对象（源/目标）。
- Webhook：事件通知配置对象。

## 10. 关键业务流程
1. 创建项目：项目负责人创建项目 -> 配置 label config -> 保存。
2. 导入任务：选择 JSON/文件/URL 导入 -> 解析与校验 -> 写入任务。
3. 标注执行：标注员进入 Data Manager -> 系统分配 next task -> 提交标注/草稿/跳过。
4. 模型协作：算法工程师接入 ML backend -> 拉取或生成预测 -> 预标注展示 -> 人工修正。
5. 质量与导出：查看 summary/agreement -> 执行批量动作 -> 导出快照或格式转换。
6. 外部集成：通过 API 拉取数据，通过 Webhook 接收项目/任务/标注事件。

## 11. 指标（KPI）建议
- 业务效率：
  - 日均标注量（annotations/day）
  - 单任务平均标注时长（lead_time）
  - 导入到首个标注的时间（TTFA）
- 质量指标：
  - 重叠任务一致性趋势
  - Ground Truth 通过率
  - 跳过率与返工率
- 平台指标：
  - 导入成功率、导出成功率
  - ML 预测成功率/失败率
  - Webhook 投递成功率

## 12. 里程碑建议（用于后续迭代规划）
- M1（基础稳定）：导入/标注/导出链路稳定性与错误可观测性提升。
- M2（效率提升）：Data Manager 批处理动作与任务分配策略优化。
- M3（智能化）：ML 交互式预标注体验、模型版本管理与闭环评估增强。

## 13. 风险与开放问题
- 社区版与企业版能力边界在前后端均有分支，需在发布文案中明确。
- 部分历史文档对格式支持的描述可能与当前代码不完全一致，需统一口径。
- 当前权限模型在 OSS 下较粗粒度，若引入细粒度角色需提前规划迁移策略。

## 14. 附录：与贡献规范对齐
根据仓库 `CONTRIBUTING.md` 中 Feature Implementation 规范，本 PRD 已覆盖：
- Problem
- PoC Notes
- User Stories

可直接作为 `prd:` issue 的基础内容，后续补充具体 feature 范围与验收用例即可。
