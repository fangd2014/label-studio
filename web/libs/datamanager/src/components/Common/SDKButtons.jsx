import { useSDK } from "../../providers/SDKProvider";
import { Button } from "@humansignal/ui";

const ariaLabelMap = {
  settingsClicked: "设置按钮",
  importClicked: "导入按钮",
  exportClicked: "导出按钮",
};

const SDKButton = ({ eventName, testId, ...props }) => {
  const sdk = useSDK();

  return sdk.hasHandler(eventName) ? (
    <Button
      {...props}
      size={props.size ?? "small"}
      look={props.look ?? "outlined"}
      variant={props.variant ?? "neutral"}
      aria-label={ariaLabelMap[eventName] ?? `${eventName.replace("Clicked", "")} 按钮`}
      data-testid={testId}
      onClick={() => {
        sdk.invoke(eventName);
      }}
    />
  ) : null;
};

export const SettingsButton = ({ ...props }) => {
  return <SDKButton {...props} eventName="settingsClicked" />;
};

export const ImportButton = ({ ...props }) => {
  return <SDKButton {...props} eventName="importClicked" testId="dm-import-button" />;
};

export const ExportButton = ({ ...props }) => {
  return <SDKButton {...props} eventName="exportClicked" testId="dm-export-button" />;
};
