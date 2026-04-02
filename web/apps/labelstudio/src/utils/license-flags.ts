import { isFlagEnabled } from "@humansignal/core/lib/utils/helpers";

export function isInLicense(id: string) {
  return isFlagEnabled(id, window.APP_SETTINGS?.flags || {});
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
