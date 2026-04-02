import { Button } from "@humansignal/ui";

const ROWS = [
  ["Owner", "组织级", "全量配置、计费、成员与安全策略"],
  ["Admin", "组织级", "成员管理、企业设置、项目监管"],
  ["Manager", "工作区级", "项目创建、分配成员、质量策略落地"],
  ["Reviewer", "项目级", "复审标注、退回修改、质量反馈"],
  ["Annotator", "项目级", "执行标注任务、提交结果与评论"],
];

export const RoleMatrixDialog = ({ onClose }) => {
  return (
    <div>
      <div style={{ marginBottom: 12 }}>角色矩阵帮助团队按组织 / 工作区 / 项目分层授权。</div>
      <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: 14 }}>
        <thead>
          <tr>
            <th style={{ textAlign: "left", borderBottom: "1px solid #e8e8e8", padding: "8px 6px" }}>角色</th>
            <th style={{ textAlign: "left", borderBottom: "1px solid #e8e8e8", padding: "8px 6px" }}>作用域</th>
            <th style={{ textAlign: "left", borderBottom: "1px solid #e8e8e8", padding: "8px 6px" }}>核心权限</th>
          </tr>
        </thead>
        <tbody>
          {ROWS.map((row) => (
            <tr key={row[0]}>
              <td style={{ borderBottom: "1px solid #f0f0f0", padding: "8px 6px" }}>{row[0]}</td>
              <td style={{ borderBottom: "1px solid #f0f0f0", padding: "8px 6px" }}>{row[1]}</td>
              <td style={{ borderBottom: "1px solid #f0f0f0", padding: "8px 6px" }}>{row[2]}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <Button onClick={onClose} aria-label="关闭角色矩阵">
        关闭
      </Button>
    </div>
  );
};
