from organizations.tests.factories import OrganizationFactory
from rest_framework.test import APITestCase


class TestOrganizationWorkspaceAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='owner_ws')
        cls.owner = cls.organization.created_by

    def get_url(self):
        return f'/api/organizations/{self.organization.id}/workspaces'

    def test_list_workspaces_returns_default_workspace(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(self.get_url())

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['is_default'] is True
        assert response.json()[0]['title'] == '默认工作区'

    def test_create_workspace(self):
        self.client.force_authenticate(user=self.owner)

        payload = {
            'title': '算法团队',
            'description': '算法标注项目工作区',
        }
        response = self.client.post(self.get_url(), payload, format='json')

        assert response.status_code == 201
        body = response.json()
        assert body['title'] == payload['title']
        assert body['description'] == payload['description']
        assert body['is_default'] is False
