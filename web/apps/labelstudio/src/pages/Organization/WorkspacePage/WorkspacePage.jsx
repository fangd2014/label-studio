import { Button, useToast } from "@humansignal/ui";
import { useAuth } from "@humansignal/core/providers/AuthProvider";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useUpdatePageTitle } from "@humansignal/core";
import { useAPI } from "../../../providers/ApiProvider";
import { cn } from "../../../utils/bem";
import "./WorkspacePage.prefix.css";

export const WorkspacePage = () => {
  const api = useAPI();
  const toast = useToast();
  const { user } = useAuth();
  const [workspaces, setWorkspaces] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  useUpdatePageTitle("工作区");

  const organizationId = user?.active_organization;

  const canCreate = useMemo(() => {
    return !submitting && !!title.trim();
  }, [submitting, title]);

  const loadWorkspaces = useCallback(async () => {
    if (!organizationId) return;

    setLoading(true);
    const result = await api.callApi("organizationWorkspaces", {
      params: { pk: organizationId },
    });
    setWorkspaces(Array.isArray(result) ? result : []);
    setLoading(false);
  }, [api, organizationId]);

  useEffect(() => {
    loadWorkspaces();
  }, [loadWorkspaces]);

  const createWorkspace = async (event) => {
    event.preventDefault();

    if (!organizationId || !title.trim()) return;

    setSubmitting(true);
    const created = await api.callApi("createOrganizationWorkspace", {
      params: { pk: organizationId },
      body: {
        title: title.trim(),
        description: description.trim(),
      },
    });
    setSubmitting(false);

    if (created) {
      toast.show({ message: "工作区创建成功" });
      setTitle("");
      setDescription("");
      loadWorkspaces();
    }
  };

  return (
    <section className={cn("workspace-page").toClassName()}>
      <header className={cn("workspace-page").elem("header").toClassName()}>
        <h2>工作区管理</h2>
        <p>按团队或业务线划分项目，支持组织内资源隔离与协作。</p>
      </header>

      <form className={cn("workspace-page").elem("form").toClassName()} onSubmit={createWorkspace}>
        <input
          className={cn("workspace-page").elem("input").toClassName()}
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="请输入工作区名称"
          aria-label="工作区名称"
        />
        <textarea
          className={cn("workspace-page").elem("textarea").toClassName()}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="可选：填写工作区描述"
          aria-label="工作区描述"
        />
        <div>
          <Button type="submit" disabled={!canCreate} waiting={submitting} aria-label="创建工作区">
            创建工作区
          </Button>
        </div>
      </form>

      <div className={cn("workspace-page").elem("list").toClassName()}>
        {loading ? (
          <div className={cn("workspace-page").elem("empty").toClassName()}>正在加载工作区...</div>
        ) : workspaces.length === 0 ? (
          <div className={cn("workspace-page").elem("empty").toClassName()}>暂无工作区</div>
        ) : (
          workspaces.map((workspace) => (
            <article className={cn("workspace-page").elem("item").toClassName()} key={workspace.id}>
              <div className={cn("workspace-page").elem("item-title").toClassName()}>
                {workspace.title}
                {workspace.is_default ? (
                  <span className={cn("workspace-page").elem("badge").toClassName()}>默认工作区</span>
                ) : null}
              </div>
              <div className={cn("workspace-page").elem("item-description").toClassName()}>
                {workspace.description || "未填写描述"}
              </div>
            </article>
          ))
        )}
      </div>
    </section>
  );
};

WorkspacePage.title = "工作区";
WorkspacePage.path = "/workspaces";
