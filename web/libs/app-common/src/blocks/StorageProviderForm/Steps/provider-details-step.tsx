import { getProviderConfig } from "../providers";
import { ProviderForm } from "../components/provider-form";
import Input from "apps/labelstudio/src/components/Form/Elements/Input/Input";
import { Toggle } from "@humansignal/ui";

interface ProviderDetailsStepProps {
  formData: any;
  errors: Record<string, string>;
  handleProviderFieldChange: (name: string, value: any) => void;
  handleFieldBlur?: (name: string, value: any) => void;
  provider?: string;
  isEditMode?: boolean;
  target?: "import" | "export";
}

export const ProviderDetailsStep = ({
  formData,
  errors,
  handleProviderFieldChange,
  handleFieldBlur,
  provider,
  isEditMode = false,
  target,
}: ProviderDetailsStepProps) => {
  const providerConfig = getProviderConfig(provider);

  if (!provider || !providerConfig) {
    return <div className="text-red-500">{!provider ? "未选择存储提供方" : `未知存储提供方：${provider}`}</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold">{providerConfig.title}</h2>
        <p className="text-muted-foreground">{providerConfig.description}</p>
      </div>

      {/* Title field - common for all providers */}
      <div className="space-y-2">
        <Input
          name="title"
          value={formData.title ?? ""}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleProviderFieldChange("title", e.target.value)}
          placeholder="请输入便于识别的名称（例如：法务文档、训练数据）"
          validate=""
          skip={false}
          labelProps={{}}
          ghost={false}
          tooltip=""
          tooltipIcon={null}
          required={true}
          label="存储名称"
          description="用于在项目中识别该连接"
          footer={errors.title ? <span className="text-negative-content">{errors.title}</span> : ""}
          className={errors.title ? "border-negative-content" : ""}
        />
      </div>

      <ProviderForm
        provider={providerConfig}
        formData={formData}
        errors={errors}
        onChange={handleProviderFieldChange}
        onBlur={handleFieldBlur}
        isEditMode={isEditMode}
        target={target}
      />

      {/* Export-specific common fields */}
      {target === "export" && (
        <div className="space-y-6">
          <div className="space-y-2">
            <Toggle
              checked={formData.can_delete_objects ?? false}
              onChange={(e) => handleProviderFieldChange("can_delete_objects", e.target.checked)}
              aria-label="允许从存储中删除对象"
              label="允许从存储中删除对象"
              description="关闭后，标注不会从存储中删除"
            />
          </div>
        </div>
      )}
    </div>
  );
};
