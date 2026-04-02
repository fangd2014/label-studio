# v3.1 前端 CI 验收报告（中文化批次）

- 验收日期：2026-04-02
- 验收分支：`codex/operation-pages-zh-cn`
- 目标版本：`v3.1`
- 验收范围：前端依赖补齐、前端 lint、前端单元测试与覆盖率（含中文化断言回归）

## 1. 环境与依赖

- OS: macOS (darwin)
- Node.js: `v22.22.2`（通过 `PATH="/opt/homebrew/opt/node@22/bin:$PATH"` 固定版本）
- Yarn: `1.22.22`
- 依赖安装命令：`yarn install --frozen-lockfile`
- 结果：通过（`Already up-to-date`）

## 2. CI 验收命令与结果

### 2.1 Lint

- 命令：`yarn lint`
- 实际执行：`biome check --write .`
- 结果：通过（退出码 0）
- 备注：存在仓库基线级 warning（本次输出 483 warnings / 9 infos），未阻断本次 CI；后续可作为独立治理项。

### 2.2 单元测试（含覆盖率）

- 命令：`yarn test:unit:coverage`
- 结果：通过（退出码 0）
- 统计：
  - Test Suites: `127 passed, 127 total`
  - Tests: `3317 passed, 5 skipped, 3322 total`
  - 失败数：`0`

### 2.3 覆盖率汇总（基于 `web/coverage`）

- 数据文件：
  - `web/coverage/lcov.info`
  - `web/coverage/coverage-final.json`
- 汇总口径：
  - Lines: `14108 / 31949` = **44.16%**
  - Functions: `3620 / 7739` = **46.78%**
  - Branches: `7305 / 21745` = **33.59%**
  - Statements: `15013 / 34848` = **43.08%**
  - Coverage files: `521`

## 3. 本轮问题与修复记录

### 3.1 AnnotationButton 中文化断言兼容

- 文件：`web/libs/editor/src/components/AnnotationsCarousel/__tests__/AnnotationButton.test.tsx`
- 问题：英文断言与中文文案不一致，导致 2 个失败用例。
- 修复：
  - 预测分数字段断言改为中英文兼容。
  - “复制标注”菜单项改为精确匹配，避免与“复制标注 ID”冲突。
- 回归：`npx jest ...AnnotationButton.test.tsx --runInBand` 通过（32/32）。

### 3.2 OutlinerPanel 中文化断言兼容

- 文件：`web/libs/editor/src/components/SidePanels/OutlinerPanel/__tests__/OutlinerPanel.test.tsx`
- 问题：全量回归中出现 6 个失败用例，均为硬编码英文断言。
- 修复：
  - 增加 I18N 兼容断言（空态文案、筛选提示、隐藏计数、Learn more 文案）。
- 回归：`npx jest ...OutlinerPanel.test.tsx --runInBand` 通过（17/17）。

## 4. 验收结论

- 前端依赖：通过
- 前端 lint：通过（有基线 warning，不阻断）
- 前端单元测试：通过
- 覆盖率产物：已生成并可追溯
- 结论：**v3.1 中文化批次满足前端 CI 验收通过条件，可进入分批提交与推送阶段。**

## 5. 后续建议（非阻断）

1. 将 Biome warning 建立独立清理里程碑（按模块分治）。
2. 对中文化关键页面补充 Playwright 冒烟用例，作为 nightly 回归。
3. 按业务域设置覆盖率阈值（尤其是 editor/datamanager 核心路径）。
