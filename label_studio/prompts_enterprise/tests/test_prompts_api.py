from organizations.tests.factories import OrganizationFactory
from rest_framework.test import APITestCase


class TestPromptsEnterpriseAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='prompts_owner')
        cls.owner = cls.organization.created_by

    def test_get_and_update_prompts_config(self):
        self.client.force_authenticate(user=self.owner)

        get_response = self.client.get('/api/prompts-enterprise/config')
        assert get_response.status_code == 200
        assert 'enabled' in get_response.json()
        assert get_response.json()['status'] == 'placeholder'

        post_response = self.client.post('/api/prompts-enterprise/config', {'enabled': True}, format='json')
        assert post_response.status_code == 200
        assert post_response.json()['enabled'] is True
