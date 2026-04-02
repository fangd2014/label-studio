import { SidebarMenu } from "../../components/SidebarMenu/SidebarMenu";
import { PeoplePage } from "./PeoplePage/PeoplePage";
import { WebhookPage } from "../WebhookPage/WebhookPage";
import { WorkspacePage } from "./WorkspacePage/WorkspacePage";

const ALLOW_ORGANIZATION_WEBHOOKS = window.APP_SETTINGS.flags?.allow_organization_webhooks;

const MenuLayout = ({ children, ...routeProps }) => {
  const menuItems = [PeoplePage, WorkspacePage];

  if (ALLOW_ORGANIZATION_WEBHOOKS) {
    menuItems.push(WebhookPage);
  }
  return <SidebarMenu menuItems={menuItems} path={routeProps.match.url} children={children} />;
};

const organizationPages = {
  WorkspacePage,
};

if (ALLOW_ORGANIZATION_WEBHOOKS) {
  organizationPages[WebhookPage] = WebhookPage;
}

export const OrganizationPage = {
  title: "组织",
  path: "/organization",
  exact: true,
  layout: MenuLayout,
  component: PeoplePage,
  pages: organizationPages,
};
