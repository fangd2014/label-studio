import type { TipsCollection } from "./types";

export const defaultTipsCollection: TipsCollection = {
  projectCreation: [
    {
      title: "你知道吗？",
      content: "在 Label Studio 企业版中，把项目组织到工作区后会更容易查找。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/manage_projects#Create-workspaces-to-organize-projects",
        params: {
          experiment: "project_creation_tip",
          treatment: "find_and_manage_projects",
        },
      },
    },
    {
      title: "更快完成权限开通",
      content: "在 Label Studio 企业版中，可通过工作区将成员批量分配到多个项目，简化权限开通流程。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/manage_projects#Add-or-remove-members-to-a-workspace",
        params: {
          experiment: "project_creation_tip",
          treatment: "faster_provisioning",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "在企业平台中，管理员可查看标注员绩效看板，以优化资源分配、团队管理和激励策略。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/dashboard_annotator",
        params: {
          experiment: "project_creation_tip",
          treatment: "annotator_dashboard",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "在 Label Studio 企业版中，你可以按项目与工作区控制内部成员和外部标注员的访问权限。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/manage_users#Roles-in-Label-Studio-Enterprise",
        params: {
          experiment: "project_creation_tip",
          treatment: "access_to_projects",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "你可以使用或修改数十种模板来配置标注界面，也可以通过简单的类 XML 标签从零自定义。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://labelstud.io/guide/setup",
        params: {
          experiment: "project_creation_tip",
          treatment: "templates",
        },
      },
    },
    {
      title: "面向 GenAI 的标注",
      content: "Label Studio 提供了监督微调、RAG 检索排序、RLHF、聊天机器人评测等多种模板。",
      closable: true,
      link: {
        label: "探索模板",
        url: "https://labelstud.io/templates/gallery_generative_ai",
        params: {
          experiment: "project_creation_tip",
          treatment: "genai_templates",
        },
      },
    },
  ],
  organizationPage: [
    {
      title: "看起来你的团队在壮大！",
      content: "在 Label Studio 企业版中，可为团队分配角色，并在项目和工作区层级控制敏感数据访问权限。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/manage_users#Roles-in-Label-Studio-Enterprise",
        params: {
          experiment: "organization_page_tip",
          treatment: "team_growing",
        },
      },
    },
    {
      title: "想让登录更简单、更安全？",
      content: "在 Label Studio 企业版中，可通过 SAML、SCIM2 或 LDAP 为团队启用单点登录（SSO）。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/auth_setup",
        params: {
          experiment: "organization_page_tip",
          treatment: "enable_sso",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "可试用 Label Studio Starter Cloud，为小团队与小规模项目优化。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://humansignal.com/pricing/",
        params: {
          experiment: "organization_page_tip",
          treatment: "starter_cloud_live",
        },
      },
    },
    {
      title: "想自动分发任务？",
      content: "可通过规则自动将任务分配给标注员，并仅在各自视图中展示已分配任务，精细控制任务可见性。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/setup_project#Set-up-annotation-settings-for-your-project",
        params: {
          experiment: "organization_page_tip",
          treatment: "automate_distribution",
        },
      },
    },
    {
      title: "与社区共享经验",
      content: "有问题，或想与其他 Label Studio 用户分享经验？欢迎加入社区 Slack 频道获取最新动态。",
      closable: true,
      link: {
        label: "加入社区",
        url: "https://label-studio.slack.com",
        params: {
          experiment: "organization_page_tip",
          treatment: "share_knowledge",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "Label Studio 支持与云存储、机器学习模型和常用工具集成，帮助自动化你的机器学习流程。",
      closable: true,
      link: {
        label: "查看集成目录",
        url: "https://labelstud.io/integrations/",
        params: {
          experiment: "organization_page_tip",
          treatment: "integration_points",
        },
      },
    },
  ],
  projectSettings: [
    {
      title: "将 AWS 承诺支出用于 Label Studio 企业版",
      content: "Label Studio 企业版已上线 AWS Marketplace，可直接使用已承诺支出优化数据标注流程。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://aws.amazon.com/marketplace/pp/prodview-wjac3msf77tny",
        params: {
          experiment: "project_settings_tip",
          treatment: "aws_marketplace",
        },
      },
    },
    {
      title: "用自动标注节省时间",
      content: "在企业平台中使用自动化能力，可快速标注大规模数据集，同时保持高质量。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/prompts_overview#Auto-labeling-with-Prompts",
        params: {
          experiment: "project_settings_tip",
          treatment: "auto_labeling",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "在 Label Studio 企业版中，可通过审核工作流与任务一致性评分提升标注数据质量。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://docs.humansignal.com/guide/quality",
        params: {
          experiment: "project_settings_tip",
          treatment: "quality_and_agreement",
        },
      },
    },
    {
      title: "评估 GenAI 模型",
      content: "在企业平台中结合自动化与人工监督，评估并保障 LLM 输出质量。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://humansignal.com/evals/",
        params: {
          experiment: "project_settings_tip",
          treatment: "evals",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "使用企业云服务可节省基础设施与升级维护时间，并获得更多自动化、质量与团队管理能力。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://humansignal.com/platform/",
        params: {
          experiment: "project_settings_tip",
          treatment: "infrastructure_and_upgrades",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "可试用 Label Studio Starter Cloud，为小团队与小规模项目优化。",
      link: {
        label: "了解更多",
        url: "https://humansignal.com/pricing/",
        params: {
          experiment: "project_settings_tip",
          treatment: "starter_cloud_live",
        },
      },
    },
    {
      title: "你知道吗？",
      content: "你可以通过后端 SDK 连接 ML 模型，用预标注或主动学习进一步提效。",
      closable: true,
      link: {
        label: "了解更多",
        url: "https://labelstud.io/guide/ml",
        params: {
          experiment: "project_settings_tip",
          treatment: "connect_ml_models",
        },
      },
    },
  ],
};
