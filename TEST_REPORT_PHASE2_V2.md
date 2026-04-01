# Label Studio 二期持续交付测试报告（v2）

生成时间：2026-04-01 20:37:40
产物目录：`test_artifacts/phase2-v2/20260401-run4`

## 1. 执行概览
- 版本：`v2`
- 项目ID：`7`
- 组织ID：`4`
- 测试任务ID：`10`

## 2. 自动化验证结果

### 2.1 后端测试
- 摘要：`16 passed in 19.09s`
- 通过：`16`
- 失败：`0`
- 覆盖率（本轮目标模块）：`54%`

### 2.2 API 主流程冒烟
- 总体：`通过`
- [PASS] annotator_patch_forbidden
- [PASS] annotator_patch_cn_message
- [PASS] manager_patch_allowed
- [PASS] invalid_role_status_400
- [PASS] invalid_role_cn_message
- [PASS] annotator_create_annotation
- [PASS] workspace_api_ok
- [PASS] workspace_default_cn_title

### 2.3 浏览器主流程冒烟
- 总体：`通过`
- 说明：`detected annotation saved success toast`
- 截图：`test_artifacts/phase2-v2/20260401-run4/ui/phase2-ui-after-submit.png`

## 3. 问题与差异
- 无阻断问题

## 4. 结论
- 当前交付链路：`可用`
- 建议：继续按 `docs/verification/enterprise_exec_gap_2026-04-01.md` 的差异项推进 M1 剩余任务。
