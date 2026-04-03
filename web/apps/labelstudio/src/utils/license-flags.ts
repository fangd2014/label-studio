import { isFlagEnabled } from "@humansignal/core/lib/utils/helpers";

function getLicenseFlagMap() {
  return {
    ...(window.APP_SETTINGS?.feature_flags ?? {}),
    ...(window.APP_SETTINGS?.flags ?? {}),
  };
}

export function isInLicense(id: string) {
  const defaultValue = window.APP_SETTINGS?.feature_flags_default_value === true;

  return isFlagEnabled(id, getLicenseFlagMap(), defaultValue);
}

const ENTERPRISE_LICENSE_FLAGS = [
  "enterprise",
  "enterprise_features",
  "lse_enterprise",
  "fflag_lse_enterprise_frontend",
];

export function isEnterpriseEdition() {
  const edition = (window.APP_SETTINGS?.version_edition ?? "").toLowerCase();
  if (edition.includes("enterprise")) return true;
  return ENTERPRISE_LICENSE_FLAGS.some((flag) => isInLicense(flag));
}
