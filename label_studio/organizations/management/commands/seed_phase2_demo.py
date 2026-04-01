import json

from django.core.management.base import BaseCommand
from django.db import transaction
from organizations.models import Organization, OrganizationMember, Workspace
from projects.models import Project, ProjectMember
from tasks.models import Task
from users.models import User

PHASE2_LABEL_CONFIG = """
<View>
  <Text name="text" value="$text"/>
  <Choices name="sentiment" toName="text" choice="single">
    <Choice value="积极"/>
    <Choice value="中性"/>
    <Choice value="消极"/>
  </Choices>
</View>
""".strip()


class Command(BaseCommand):
    help = 'Seed phase2 demo data for workspace/role/UI main-flow verification'

    def add_arguments(self, parser):
        parser.add_argument('--organization-title', default='二期验收组织')
        parser.add_argument('--project-title', default='二期主流程验收项目')
        parser.add_argument('--task-count', default=8, type=int)

        parser.add_argument('--owner-email', default='phase2.owner@example.com')
        parser.add_argument('--owner-password', default='Phase2Owner!123')

        parser.add_argument('--manager-email', default='phase2.manager@example.com')
        parser.add_argument('--manager-password', default='Phase2Manager!123')

        parser.add_argument('--annotator-email', default='phase2.annotator@example.com')
        parser.add_argument('--annotator-password', default='Phase2Annotator!123')

    def handle(self, *args, **options):
        task_count = max(1, int(options['task_count']))

        with transaction.atomic():
            owner = self._upsert_user(
                email=options['owner_email'],
                password=options['owner_password'],
                username='phase2_owner',
            )
            manager = self._upsert_user(
                email=options['manager_email'],
                password=options['manager_password'],
                username='phase2_manager',
            )
            annotator = self._upsert_user(
                email=options['annotator_email'],
                password=options['annotator_password'],
                username='phase2_annotator',
            )

            organization = self._get_or_create_organization(
                title=options['organization_title'],
                owner=owner,
            )

            self._ensure_org_member(organization, owner, set_active=True)
            self._ensure_org_member(organization, manager, set_active=True)
            self._ensure_org_member(organization, annotator, set_active=True)

            workspace = Workspace.get_or_create_default(organization, created_by=owner)
            project = self._get_or_create_project(
                organization=organization,
                project_title=options['project_title'],
                workspace=workspace,
                owner=owner,
            )

            self._upsert_project_member(project, manager, ProjectMember.Role.MANAGER)
            self._upsert_project_member(project, annotator, ProjectMember.Role.ANNOTATOR)

            self._ensure_tasks(project=project, task_count=task_count)

        summary = {
            'organization_id': organization.id,
            'workspace_id': workspace.id,
            'project_id': project.id,
            'task_count': Task.objects.filter(project=project).count(),
            'first_task_id': Task.objects.filter(project=project).order_by('id').values_list('id', flat=True).first(),
            'owner_user_id': owner.id,
            'owner_email': owner.email,
            'owner_password': options['owner_password'],
            'owner_token': owner.get_token().key,
            'manager_user_id': manager.id,
            'manager_email': manager.email,
            'manager_password': options['manager_password'],
            'manager_token': manager.get_token().key,
            'annotator_user_id': annotator.id,
            'annotator_email': annotator.email,
            'annotator_password': options['annotator_password'],
            'annotator_token': annotator.get_token().key,
            'workspace_title': workspace.title,
            'project_title': project.title,
        }
        self.stdout.write(json.dumps(summary, ensure_ascii=False))

    @staticmethod
    def _upsert_user(email, password, username):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'is_active': True,
            },
        )

        updated_fields = []
        if not user.username:
            user.username = username
            updated_fields.append('username')
        if not user.is_active:
            user.is_active = True
            updated_fields.append('is_active')

        user.set_password(password)
        updated_fields.append('password')
        user.save(update_fields=updated_fields)

        if created:
            user.reset_token()
        elif not user.get_token():
            user.reset_token()

        return user

    @staticmethod
    def _get_or_create_organization(title, owner):
        organization = Organization.objects.filter(title=title).first()
        if organization is None:
            organization = Organization.create_organization(
                title=title,
                created_by=owner,
                legacy_api_tokens_enabled=True,
            )
        if organization.created_by_id is None:
            organization.created_by = owner
            organization.save(update_fields=['created_by'])

        # Keep legacy API token auth enabled for repeatable local/CI smoke checks.
        if hasattr(organization, 'jwt'):
            jwt_settings = organization.jwt
            update_fields = []
            if not jwt_settings.api_tokens_enabled:
                jwt_settings.api_tokens_enabled = True
                update_fields.append('api_tokens_enabled')
            if not jwt_settings.legacy_api_tokens_enabled:
                jwt_settings.legacy_api_tokens_enabled = True
                update_fields.append('legacy_api_tokens_enabled')
            if update_fields:
                jwt_settings.save(update_fields=update_fields)

        return organization

    @staticmethod
    def _ensure_org_member(organization, user, set_active=False):
        member = OrganizationMember.objects.filter(
            organization=organization,
            user=user,
            deleted_at__isnull=True,
        ).first()
        if member is None:
            OrganizationMember.objects.create(organization=organization, user=user)

        if set_active and user.active_organization_id != organization.id:
            user.active_organization = organization
            user.save(update_fields=['active_organization'])

    @staticmethod
    def _get_or_create_project(organization, project_title, workspace, owner):
        project, _ = Project.objects.get_or_create(
            organization=organization,
            title=project_title,
            defaults={
                'created_by': owner,
                'workspace': workspace,
                'label_config': PHASE2_LABEL_CONFIG,
                'show_instruction': False,
            },
        )

        update_fields = []
        if project.workspace_id != workspace.id:
            project.workspace = workspace
            update_fields.append('workspace')
        if project.created_by_id is None:
            project.created_by = owner
            update_fields.append('created_by')
        if not project.label_config or project.label_config == '<View></View>':
            project.label_config = PHASE2_LABEL_CONFIG
            update_fields.append('label_config')

        if update_fields:
            project.save(update_fields=update_fields)

        return project

    @staticmethod
    def _upsert_project_member(project, user, role):
        membership = ProjectMember.objects.filter(project=project, user=user).first()
        if membership is None:
            ProjectMember.objects.create(project=project, user=user, role=role, enabled=True)
            return

        update_fields = []
        if membership.role != role:
            membership.role = role
            update_fields.append('role')
        if not membership.enabled:
            membership.enabled = True
            update_fields.append('enabled')

        if update_fields:
            membership.save(update_fields=update_fields)

    @staticmethod
    def _ensure_tasks(project, task_count):
        existing_count = Task.objects.filter(project=project).count()
        if existing_count >= task_count:
            return

        for index in range(existing_count + 1, task_count + 1):
            Task.objects.create(
                project=project,
                data={
                    'text': f'二期验收示例文本 {index}',
                },
                meta={'seed': 'phase2', 'order': index},
                inner_id=index,
            )
