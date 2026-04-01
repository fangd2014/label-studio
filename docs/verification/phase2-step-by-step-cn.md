# 二期功能逐步验收（中文）

更新时间：2026-04-01

## 1. 目标

本验收文档用于验证二期四项能力是否可复现：

1. 工作区基础能力（默认工作区、项目自动绑定）
2. 项目级角色模型扩展（annotator/reviewer/manager）
3. 角色权限收口（项目写操作限制 + 标注能力保留）
4. 中文提示与 Docker 运行态验收

## 2. 本地测试命令（pytest）

```bash
.venv/bin/pytest \
  label_studio/organizations/tests/test_api.py \
  label_studio/organizations/tests/test_workspaces_api.py \
  label_studio/projects/tests/test_project_workspace.py \
  label_studio/projects/tests/test_project_member_roles.py \
  label_studio/projects/tests/test_role_permissions.py -q
```

本次结果：`14 passed`

---

## 3. Step 1 验证：工作区基础能力

### 3.1 pytest

```bash
.venv/bin/pytest \
  label_studio/organizations/tests/test_workspaces_api.py \
  label_studio/projects/tests/test_project_workspace.py -q
```

### 3.2 curl（示例）

```bash
# 列出组织工作区（应包含“默认工作区”）
curl -H "Authorization: Token <OWNER_TOKEN>" \
  http://localhost:8080/api/organizations/<ORG_ID>/workspaces

# 创建工作区
curl -X POST -H "Authorization: Token <OWNER_TOKEN>" -H "Content-Type: application/json" \
  -d '{"title":"算法团队","description":"算法标注项目工作区"}' \
  http://localhost:8080/api/organizations/<ORG_ID>/workspaces
```

预期：

1. 返回默认工作区标题为 `默认工作区`
2. 新创建工作区返回 `201`
3. 新建项目后 `workspace` 自动绑定默认工作区

---

## 4. Step 2 验证：项目成员角色

### 4.1 pytest

```bash
.venv/bin/pytest label_studio/projects/tests/test_project_member_roles.py -q
```

### 4.2 curl（示例）

```bash
# 创建项目成员（默认角色 annotator）
curl -X POST -H "Authorization: Token <OWNER_TOKEN>" -H "Content-Type: application/json" \
  -d '{"user": <USER_ID>}' \
  http://localhost:8080/api/projects/<PROJECT_ID>/memberships

# 更新角色为 manager
curl -X PATCH -H "Authorization: Token <OWNER_TOKEN>" -H "Content-Type: application/json" \
  -d '{"role":"manager"}' \
  http://localhost:8080/api/projects/<PROJECT_ID>/memberships/<USER_ID>/

# 查询成员列表（应包含 role 字段）
curl -H "Authorization: Token <OWNER_TOKEN>" \
  http://localhost:8080/api/projects/<PROJECT_ID>/memberships
```

预期：

1. 创建成员默认 `role=annotator`
2. 角色更新成功
3. 列表返回角色字段

---

## 5. Step 3 验证：角色权限收口

### 5.1 pytest

```bash
.venv/bin/pytest label_studio/projects/tests/test_role_permissions.py -q
```

### 5.2 curl（示例）

```bash
# annotator 尝试修改项目（应 403）
curl -X PATCH -H "Authorization: Token <ANNOTATOR_TOKEN>" -H "Content-Type: application/json" \
  -d '{"title":"forbidden"}' \
  http://localhost:8080/api/projects/<PROJECT_ID>/

# manager 修改项目（应 200）
curl -X PATCH -H "Authorization: Token <MANAGER_TOKEN>" -H "Content-Type: application/json" \
  -d '{"title":"manager-updated"}' \
  http://localhost:8080/api/projects/<PROJECT_ID>/

# annotator 创建标注（应 201）
curl -X POST -H "Authorization: Token <ANNOTATOR_TOKEN>" -H "Content-Type: application/json" \
  -d '{"result":[]}' \
  http://localhost:8080/api/tasks/<TASK_ID>/annotations/
```

预期：

1. annotator/reviewer 不能做项目管理写操作
2. manager 可以执行项目管理写操作
3. annotator 保留标注能力

---

## 6. Step 4 验证：中文提示 + Docker 运行态

### 6.1 重建并重启容器

```bash
docker compose up -d --build --force-recreate app nginx
docker compose exec -T app python label_studio/manage.py migrate
```

### 6.2 运行态脚本验收（已执行）

脚本输出摘要：

```json
{
  "workspace_api_status": 200,
  "workspace_default_title": "默认工作区",
  "project_workspace_bound": true,
  "membership_create_status": 201,
  "membership_default_role": "annotator",
  "invalid_role_status": 400,
  "invalid_role_has_cn_message": true,
  "annotator_patch_status": 403,
  "annotator_patch_detail": "当前项目角色无权执行此操作，请联系项目管理员。",
  "annotator_annotation_status": 201,
  "manager_patch_status": 200
}
```

说明：

1. 默认工作区与项目绑定正常
2. 角色默认值与更新正常
3. 中文错误提示已生效（角色非法值、权限拒绝）
4. manager/annotator 权限边界符合预期
