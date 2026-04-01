import json
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from organizations.models import Organization, Workspace
from projects.models import Project, ProjectMember
from tasks.models import Task


class TestSeedPhase2DemoCommand(TestCase):
    def test_command_creates_workspace_project_memberships_and_tasks(self):
        stdout = StringIO()
        call_command(
            'seed_phase2_demo',
            '--organization-title',
            '二期测试组织A',
            '--project-title',
            '二期测试项目A',
            '--owner-email',
            'phase2.owner.a@example.com',
            '--owner-password',
            'OwnerPass!123',
            '--manager-email',
            'phase2.manager.a@example.com',
            '--manager-password',
            'ManagerPass!123',
            '--annotator-email',
            'phase2.annotator.a@example.com',
            '--annotator-password',
            'AnnotatorPass!123',
            '--task-count',
            '3',
            stdout=stdout,
        )

        result = json.loads(stdout.getvalue())
        project = Project.objects.get(pk=result['project_id'])
        organization = Organization.objects.get(pk=result['organization_id'])
        default_workspace = Workspace.objects.get(organization=organization, is_default=True)

        assert project.workspace_id == default_workspace.id
        assert ProjectMember.objects.get(project=project, user_id=result['annotator_user_id']).role == 'annotator'
        assert ProjectMember.objects.get(project=project, user_id=result['manager_user_id']).role == 'manager'
        assert Task.objects.filter(project=project).count() == 3

    def test_command_is_idempotent_for_same_input(self):
        common_args = [
            '--organization-title',
            '二期测试组织B',
            '--project-title',
            '二期测试项目B',
            '--owner-email',
            'phase2.owner.b@example.com',
            '--owner-password',
            'OwnerPass!123',
            '--manager-email',
            'phase2.manager.b@example.com',
            '--manager-password',
            'ManagerPass!123',
            '--annotator-email',
            'phase2.annotator.b@example.com',
            '--annotator-password',
            'AnnotatorPass!123',
            '--task-count',
            '4',
        ]

        first_stdout = StringIO()
        call_command('seed_phase2_demo', *common_args, stdout=first_stdout)
        first = json.loads(first_stdout.getvalue())

        second_stdout = StringIO()
        call_command('seed_phase2_demo', *common_args, stdout=second_stdout)
        second = json.loads(second_stdout.getvalue())

        assert first['organization_id'] == second['organization_id']
        assert first['project_id'] == second['project_id']
        assert Project.objects.filter(title='二期测试项目B').count() == 1
        assert Task.objects.filter(project_id=first['project_id']).count() == 4
