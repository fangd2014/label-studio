from organizations.tests.factories import OrganizationFactory
from projects.models import ProjectMember
from projects.tests.factories import ProjectFactory
from rest_framework.test import APITestCase
from tasks.tests.factories import TaskFactory
from users.tests.factories import UserFactory


class TestProjectRolePermissions(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='role_owner')
        cls.owner = cls.organization.created_by
        cls.project = ProjectFactory(organization=cls.organization, created_by=cls.owner)
        cls.task = TaskFactory(project=cls.project)

        cls.annotator = UserFactory(username='role_annotator', active_organization=cls.organization)
        cls.reviewer = UserFactory(username='role_reviewer', active_organization=cls.organization)
        cls.manager = UserFactory(username='role_manager', active_organization=cls.organization)
        cls.candidate = UserFactory(username='role_candidate', active_organization=cls.organization)

        ProjectMember.objects.create(project=cls.project, user=cls.annotator, role=ProjectMember.Role.ANNOTATOR)
        ProjectMember.objects.create(project=cls.project, user=cls.reviewer, role=ProjectMember.Role.REVIEWER)
        ProjectMember.objects.create(project=cls.project, user=cls.manager, role=ProjectMember.Role.MANAGER)

    def project_url(self):
        return f'/api/projects/{self.project.id}/'

    def membership_url(self):
        return f'/api/projects/{self.project.id}/memberships'

    def annotations_url(self):
        return f'/api/tasks/{self.task.id}/annotations/'

    def test_annotator_cannot_update_project_settings(self):
        self.client.force_authenticate(user=self.annotator)

        response = self.client.patch(self.project_url(), {'title': 'annotator cannot edit'}, format='json')

        assert response.status_code == 403
        assert response.json()['detail'] == '当前项目角色无权执行此操作，请联系项目管理员。'

    def test_reviewer_cannot_create_project_membership(self):
        self.client.force_authenticate(user=self.reviewer)

        response = self.client.post(self.membership_url(), {'user': self.candidate.id}, format='json')

        assert response.status_code == 403

    def test_manager_can_create_project_membership(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.post(self.membership_url(), {'user': self.candidate.id}, format='json')

        assert response.status_code == 201
        assert response.json()['role'] == ProjectMember.Role.ANNOTATOR

    def test_annotator_can_create_annotation(self):
        self.client.force_authenticate(user=self.annotator)

        response = self.client.post(self.annotations_url(), {'result': []}, format='json')

        assert response.status_code == 201

    def test_next_task_role_helpers(self):
        from projects.functions import next_task

        assert next_task.get_user_project_role(self.annotator, self.project) == ProjectMember.Role.ANNOTATOR
        assert next_task.get_user_project_role(self.reviewer, self.project) == ProjectMember.Role.REVIEWER
        assert next_task.is_user_project_annotator(self.annotator, self.project) is True
        assert next_task.is_user_project_annotator(self.reviewer, self.project) is False
        assert next_task.is_user_restricted_project_role(self.reviewer, self.project) is True
        assert next_task.is_user_restricted_project_role(self.manager, self.project) is False
