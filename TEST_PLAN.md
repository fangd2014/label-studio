# Label Studio 测试计划（TEST PLAN）

## 1. 文档目标
本计划用于定义 Label Studio 后端测试活动的目标、范围、资源、准入/准出标准与交付物，确保测试工作可执行、可追踪、可复用。

## 2. 测试对象
- 仓库：`label-studio`
- 本轮重点模块：
  - 数据管理动作：`tests/data_manager/actions/test_predictions_to_annotations.py`
  - 数据导入：`tests/data_import/test_uploader.py`
  - 配置校验：`tests/test_config_validation.py`（子集）

## 3. 测试范围
### 3.1 在范围内
- 预测转标注逻辑可用性（模型版本选项回退逻辑）
- 上传 URL 安全校验（SSRF/非法协议/扩展名/文件大小）
- 标签配置关键回归点（Choices、toName 必填、错误 XML）
- SQLite 条件下 Django 测试运行能力验证

### 3.2 不在范围内
- 全量测试集回归（含 loadtest、tavern 全链路、前端 E2E）
- 性能压测、安全渗透测试
- 生产环境联调与灰度验证

## 4. 测试目标
- 验证核心后端能力在当前代码下可正确执行
- 识别关键依赖与运行风险（测试环境启动、三方依赖兼容）
- 形成标准化测试资产：计划、方案、报告、日志

## 5. 测试策略摘要
采用风险驱动 + 冒烟回归策略：先验证测试环境可启动，再覆盖高价值功能点，最后输出可追溯结果。

## 6. 资源与职责
- 执行人：AI 测试执行代理（本次）
- 代码所有者：仓库维护者
- 主要工具：Python 3.12.7、pytest 7.2.2、Django SQLite 测试配置

## 7. 准入/准出标准
### 7.1 准入标准
- 本地可创建 Python 虚拟环境
- 依赖安装完成（含 Django、pytest、pytest-django、moto、freezegun）
- 环境变量设置可用：
  - `DJANGO_DB=sqlite`
  - `DJANGO_SETTINGS_MODULE=core.settings.label_studio`

### 7.2 准出标准
- 计划中的测试用例执行完成
- 无阻断级故障（Blocker）遗留
- 输出测试报告并附日志路径

## 8. 里程碑
1. 测试环境准备与依赖安装
2. 核心测试子集执行
3. 测试结果汇总与报告输出

## 9. 交付物
- `TEST_PLAN.md`
- `TEST_STRATEGY.md`
- `TEST_REPORT_2026-04-01.md`
- 原始日志：`test_artifacts/2026-04-01/*.log`

## 10. 风险与应对
- 风险：三方依赖版本不兼容导致测试无法启动（如 `moto` 版本变化）
- 应对：锁定兼容版本、记录安装轨迹、将环境要求写入报告
