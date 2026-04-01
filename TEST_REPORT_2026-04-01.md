# Label Studio 测试报告（2026-04-01）

## 1. 执行概览
- 执行日期：2026-04-01
- 执行环境：本地开发机（macOS）
- Python：`3.12.7`
- pytest：`7.2.2`
- 测试数据库：SQLite
- 配置：`DJANGO_DB=sqlite`，`DJANGO_SETTINGS_MODULE=core.settings.label_studio`

## 2. 执行范围
- `tests/data_manager/actions/test_predictions_to_annotations.py`
- `tests/data_import/test_uploader.py`
- `tests/test_config_validation.py`（关键回归子集）

## 3. 执行结果
| 测试集 | 结果摘要 | 耗时 |
|---|---|---|
| `test_predictions_to_annotations.py` | `1 passed` | `0.21s` |
| `test_uploader.py` | `13 passed` | `10.39s` |
| `test_config_validation.py` 子集 | `3 passed, 7 deselected` | `9.57s` |

### 汇总
- 已执行：17 个
- 通过：17
- 失败：0
- 跳过/取消选择：7（策略性未执行）
- 结论：本轮测试范围内通过，未发现阻断缺陷。

## 4. 过程问题与处理
1. 初始阻塞：`freezegun` 缺失导致 `tests/conftest.py` 导入失败
   - 处理：安装 `freezegun~=1.5.1`
2. 兼容问题：`moto 5.x` 缺少 `mock_s3`
   - 处理：降级并锁定 `moto==4.2.14`
3. 依赖解析耗时高
   - 处理：先最小化依赖安装，再按报错补齐

## 5. 测试证据
- `test_artifacts/2026-04-01/test_predictions_to_annotations.log`
- `test_artifacts/2026-04-01/test_uploader.log`
- `test_artifacts/2026-04-01/test_config_validation_subset.log`

## 6. 风险与建议
- 风险：测试依赖对版本敏感（尤其 `moto`）
- 建议：
  1. 在 CI requirements 中固定 `moto==4.2.14`
  2. 增加 smoke job，至少覆盖本报告三组用例
  3. 后续补跑 `test_config_validation.py` 全量与 PostgreSQL 模式
