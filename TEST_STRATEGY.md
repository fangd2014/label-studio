# Label Studio 测试方案（TEST STRATEGY）

## 1. 方案目标
在有限时间内，以最小可行测试集验证后端关键业务能力，并保证结果可复现、可审计。

## 2. 方法论
- 风险优先：优先覆盖导入安全、配置校验、核心动作逻辑
- 分层验证：
  - 单元/模块级：函数与逻辑分支
  - 组件级：Django 测试上下文（fixture + DB）
- 结果留痕：所有执行命令输出写入日志文件

## 3. 测试环境
- OS：macOS（本地开发环境）
- Python：`3.12.7`
- pytest：`7.2.2`
- 数据库：SQLite（`DJANGO_DB=sqlite`）
- 设置模块：`core.settings.label_studio`
- 虚拟环境：项目根目录 `.venv`

## 4. 测试范围设计
### 4.1 用例分组
1. `data_manager/actions`
   - 目标：验证 predictions -> annotations 表单选项逻辑
2. `data_import/uploader`
   - 目标：验证 URL 安全、扩展名、文件大小、重定向处理
3. `config_validation`（子集）
   - 目标：验证关键配置校验回归点

### 4.2 执行命令
```bash
source .venv/bin/activate
cd label_studio

DJANGO_DB=sqlite DJANGO_SETTINGS_MODULE=core.settings.label_studio \
pytest -q tests/data_manager/actions/test_predictions_to_annotations.py

DJANGO_DB=sqlite DJANGO_SETTINGS_MODULE=core.settings.label_studio \
pytest -q tests/data_import/test_uploader.py

DJANGO_DB=sqlite DJANGO_SETTINGS_MODULE=core.settings.label_studio \
pytest -q tests/test_config_validation.py \
-k 'config_validation_for_choices_workaround or missing_to_name_in_number_tag_fails or parse_wrong_xml'
```

## 5. 缺陷与阻塞处理流程
- 若测试启动失败：优先处理 conftest 级阻塞依赖
- 若出现版本冲突：锁定兼容版本并复跑
- 若单测失败：记录失败栈、定位模块、给出修复建议

## 6. 通过标准
- 本轮计划内测试执行完成
- 失败数 = 0（若有失败需提供缺陷单与回归结果）
- 日志完整可追溯

## 7. 后续扩展建议
1. 将当前三组用例加入 PR 必跑 smoke 阶段
2. 增加 `test_config_validation.py` 全量回归
3. 增加 PostgreSQL 模式回归（`DJANGO_DB=default`）
4. 在 CI 中固定 `moto` 兼容版本以避免测试中断
