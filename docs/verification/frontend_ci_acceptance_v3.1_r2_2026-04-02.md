# v3.1 前端 CI 验收报告（R2）

- 验收日期：2026-04-02
- 验收分支：`codex/operation-pages-zh-cn`
- 验收目标：未提交中文化批次继续提交前的完整前端依赖与 CI 回归
- 执行人：Codex

## 1) 环境基线

- Node.js：`v22.22.2`
- Yarn：`1.22.22`
- OS：macOS (darwin)

## 2) 验收命令与结果

1. 依赖安装
   - 命令：`PATH="/opt/homebrew/opt/node@22/bin:$PATH" yarn install --frozen-lockfile`
   - 结果：通过（Already up-to-date）

2. 前端 Lint
   - 命令：`PATH="/opt/homebrew/opt/node@22/bin:$PATH" yarn lint`
   - 结果：通过（退出码 0）
   - 说明：存在仓库基线 warning（483）与 info（9），本轮未新增阻断项

3. 前端单元测试 + 覆盖率
   - 命令：`PATH="/opt/homebrew/opt/node@22/bin:$PATH" yarn test:unit:coverage`
   - 结果：通过（退出码 0）
   - 总结：
     - Test Suites：`127 passed, 127 total`
     - Tests：`3317 passed, 5 skipped, 3322 total`
     - Failures：`0`

## 3) 覆盖率汇总

- 数据来源：
  - `web/coverage/lcov.info`
  - `web/coverage/coverage-final.json`

- 汇总结果：
  - Lines：`14108 / 31949` = **44.16%**
  - Functions：`3620 / 7739` = **46.78%**
  - Branches：`7305 / 21745` = **33.59%**
  - Statements：`15013 / 34848` = **43.08%**
  - Coverage files：`521`

## 4) 结论

- 前端依赖、lint、unit+coverage 均已完整复跑并通过。
- v3.1 当前分支具备继续进行“未提交中文化改动分批提交并推送”的条件。

## 5) 非阻断事项

1. `yarn lint` 的 warning/info 为仓库基线问题，建议单列技术债治理。
2. 现有控制台 React warning 主要来自测试 mock/act 方式，不影响本轮通过判定。
