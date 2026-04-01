# Phase 2 Workspace & Roles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 以可验证的增量方式完成企业能力二期，先落地工作区基础，再推进项目级角色。

**Architecture:** 在 `organizations` 域新增 `Workspace`，并通过 `Project.workspace` 形成“组织 -> 工作区 -> 项目”层级。通过 API 暴露工作区管理能力，后续在 `ProjectMember` 扩展角色并收口权限。

**Tech Stack:** Django, DRF, Django ORM Migrations, pytest

---

### Task 1: 工作区基础能力（已执行）

**Files:**
- Modify: `label_studio/organizations/models.py`
- Modify: `label_studio/organizations/functions.py`
- Modify: `label_studio/organizations/serializers.py`
- Modify: `label_studio/organizations/api.py`
- Modify: `label_studio/organizations/urls.py`
- Modify: `label_studio/projects/models.py`
- Modify: `label_studio/projects/serializers.py`
- Create: `label_studio/organizations/migrations/0007_workspace.py`
- Create: `label_studio/projects/migrations/0035_project_workspace.py`
- Test: `label_studio/organizations/tests/test_workspaces_api.py`
- Test: `label_studio/projects/tests/test_project_workspace.py`

- [x] **Step 1: 写失败测试（RED）**
- [x] **Step 2: 运行测试确认失败**
Run: `python -m pytest label_studio/organizations/tests/test_workspaces_api.py label_studio/projects/tests/test_project_workspace.py -q`
Expected: `3 failed`

- [x] **Step 3: 实现最小功能（GREEN）**
- [x] **Step 4: 运行测试确认通过**
Run: `python -m pytest label_studio/organizations/tests/test_workspaces_api.py label_studio/projects/tests/test_project_workspace.py -q`
Expected: `3 passed`

### Task 2: 项目级角色模型扩展（下一步）

**Files:**
- Modify: `label_studio/projects/models.py` (`ProjectMember`)
- Modify: `label_studio/projects/serializers.py`
- Modify: `label_studio/projects/api.py`
- Create: `label_studio/projects/migrations/<new>.py`
- Test: `label_studio/projects/tests/test_project_member_roles.py`

- [x] **Step 1: 写失败测试（角色默认值/更新/查询）**
- [x] **Step 2: 运行失败测试**
- [x] **Step 3: 实现 role 字段与 API 更新**
- [x] **Step 4: 运行测试通过**
- [x] **Step 5: 回归已有项目接口测试**

### Task 3: 角色权限收口（下一步）

**Files:**
- Modify: `label_studio/projects/functions/next_task.py`
- Modify: `label_studio/core/permissions.py`
- Modify: `label_studio/core/api_permissions.py`
- Test: `label_studio/projects/tests/test_role_permissions.py`

- [x] **Step 1: 写失败测试（annotator/reviewer/manager 权限矩阵）**
- [x] **Step 2: 实现最小权限拦截**
- [x] **Step 3: 执行回归测试**

### Task 4: 中文化与验收脚本（下一步）

**Files:**
- Create: `docs/verification/phase2-step-by-step-cn.md`
- Modify: 相关 API 错误消息与前端文案

- [ ] **Step 1: 补齐中文提示与术语**
- [ ] **Step 2: 提供每步 curl/pytest 验证命令**
- [ ] **Step 3: Docker 环境验证并记录结果**
