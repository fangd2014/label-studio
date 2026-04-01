from organizations.tests.factories import OrganizationFactory
from projects.models import ProjectMember
from projects.tests.factories import ProjectFactory
from rest_framework.test import APITestCase
from users.tests.factories import UserFactory


class TestProjectMemberRoleAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='project_role_owner')
        cls.owner = cls.organization.created_by
        cls.project = ProjectFactory(organization=cls.organization, created_by=cls.owner)
        cls.member_user = UserFactory(username='project_member', active_organization=cls.organization)

    def list_url(self):
        return f'/api/projects/{self.project.id}/memberships'

    def detail_url(self):
        return f'/api/projects/{self.project.id}/memberships/{self.member_user.id}/'

    def test_create_membership_uses_default_annotator_role(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(self.list_url(), {'user': self.member_user.id}, format='json')

        assert response.status_code == 201
        body = response.json()
        assert body['role'] == 'annotator'

        membership = ProjectMember.objects.get(project=self.project, user=self.member_user)
        assert membership.role == 'annotator'

    def test_patch_membership_role(self):
        self.client.force_authenticate(user=self.owner)
        ProjectMember.objects.create(project=self.project, user=self.member_user)

        response = self.client.patch(self.detail_url(), {'role': 'manager'}, format='json')

        assert response.status_code == 200
        assert response.json()['role'] == 'manager'

        membership = ProjectMember.objects.get(project=self.project, user=self.member_user)
        assert membership.role == 'manager'

    def test_list_memberships_returns_role_field(self):
        self.client.force_authenticate(user=self.owner)
        ProjectMember.objects.create(project=self.project, user=self.member_user, role='reviewer')

        response = self.client.get(self.list_url())

        assert response.status_code == 200
        memberships = response.json()
        project_member = next(item for item in memberships if item['user'] == self.member_user.id)
        assert project_member['role'] == 'reviewer'

    def test_patch_membership_invalid_role_returns_chinese_error(self):
        self.client.force_authenticate(user=self.owner)
        ProjectMember.objects.create(project=self.project, user=self.member_user)

        response = self.client.patch(self.detail_url(), {'role': 'invalid_role'}, format='json')

        assert response.status_code == 400
        assert '角色仅支持 annotator、reviewer、manager' in str(response.json())
