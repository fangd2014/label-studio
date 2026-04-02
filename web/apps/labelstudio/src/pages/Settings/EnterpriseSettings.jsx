import { Button } from "@humansignal/ui";
import { useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useAPI } from "../../providers/ApiProvider";
import { ProjectContext } from "../../providers/ProjectProvider";
import { cn } from "../../utils/bem";
import { isEnterpriseEdition } from "../../utils/license-flags";
import "./EnterpriseSettings.prefix.css";

export const EnterpriseSettings = () => {
  const api = useAPI();
  const { project } = useContext(ProjectContext);
  const [autoValidation, setAutoValidation] = useState(false);
  const [reviewRequired, setReviewRequired] = useState(true);
  const [lowTrustThreshold, setLowTrustThreshold] = useState("0.30");
  const [agreement, setAgreement] = useState(null);
  const [saving, setSaving] = useState(false);

  const enterpriseEnabled = useMemo(() => isEnterpriseEdition(), []);

  const loadData = useCallback(async () => {
    if (!project?.id) return;

    const rulesResponse = await api.callApi("projectQualityRules", {
      params: { projectId: project.id },
    });
    const agreementResponse = await api.callApi("projectAgreementMetrics", {
      params: { projectId: project.id },
    });

    setAutoValidation(Boolean(rulesResponse?.quality_rules?.auto_validation));
    setReviewRequired((rulesResponse?.quality_rules?.low_agreement_action ?? "review_required") === "review_required");
    setLowTrustThreshold(String(rulesResponse?.low_trust_threshold ?? 0.3));
    setAgreement(agreementResponse ?? null);
  }, [api, project?.id]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const saveRules = async () => {
    if (!project?.id) return;

    const threshold = Number.parseFloat(lowTrustThreshold);
    if (Number.isNaN(threshold) || threshold < 0 || threshold > 1) return;

    setSaving(true);
    await api.callApi("updateProjectQualityRules", {
      params: { projectId: project.id },
      body: {
        quality_rules: {
          auto_validation: autoValidation,
          low_agreement_action: reviewRequired ? "review_required" : "notify_only",
        },
        low_trust_threshold: threshold,
        annotator_evaluation_enabled: true,
      },
    });
    setSaving(false);
    loadData();
  };

  return (
    <div className={cn("enterprise-settings").toClassName()}>
      <h1>企业设置</h1>

      <section className={cn("enterprise-settings").elem("section").toClassName()}>
        <div className={cn("enterprise-settings").elem("title").toClassName()}>身份与访问</div>
        <div className={cn("enterprise-settings").elem("hint").toClassName()}>
          已接入 SAML / SCIM / LDAP 基础能力。后端 API 已可用于对接企业身份平台。
        </div>
      </section>

      <section className={cn("enterprise-settings").elem("section").toClassName()}>
        <div className={cn("enterprise-settings").elem("title").toClassName()}>质量护栏</div>
        <label className={cn("enterprise-settings").elem("line").toClassName()}>
          <span>开启自动校验</span>
          <input type="checkbox" checked={autoValidation} onChange={(e) => setAutoValidation(e.target.checked)} />
        </label>

        <label className={cn("enterprise-settings").elem("line").toClassName()}>
          <span>低一致性策略：要求复审</span>
          <input type="checkbox" checked={reviewRequired} onChange={(e) => setReviewRequired(e.target.checked)} />
        </label>

        <label className={cn("enterprise-settings").elem("line").toClassName()}>
          <span>低信任阈值（0~1）</span>
          <input
            className={cn("enterprise-settings").elem("input").toClassName()}
            value={lowTrustThreshold}
            onChange={(e) => setLowTrustThreshold(e.target.value)}
            aria-label="低信任阈值"
          />
        </label>

        <Button onClick={saveRules} waiting={saving} aria-label="保存企业质量规则">
          保存企业质量规则
        </Button>
      </section>

      <section className={cn("enterprise-settings").elem("section").toClassName()}>
        <div className={cn("enterprise-settings").elem("title").toClassName()}>一致性指标</div>
        <div className={cn("enterprise-settings").elem("hint").toClassName()}>
          指标：{agreement?.metric ?? "exact_match_consensus"}，得分：{agreement?.score ?? "-"}，评估任务数：
          {agreement?.tasks_evaluated ?? 0}
        </div>
      </section>

      {!enterpriseEnabled ? (
        <div className={cn("enterprise-settings").elem("warn").toClassName()}>
          当前许可证未识别为企业版，部分能力可能仅用于演示或联调。
        </div>
      ) : null}
    </div>
  );
};

EnterpriseSettings.menuItem = "企业";
EnterpriseSettings.path = "/enterprise";
