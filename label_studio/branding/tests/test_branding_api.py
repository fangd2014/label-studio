from organizations.tests.factories import OrganizationFactory
from rest_framework.test import APITestCase


class TestBrandingAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='branding_owner')
        cls.owner = cls.organization.created_by

    def test_get_and_update_branding_config(self):
        self.client.force_authenticate(user=self.owner)

        get_response = self.client.get('/api/branding/config')
        assert get_response.status_code == 200
        assert 'product_name' in get_response.json()
        assert 'primary_color' in get_response.json()

        update_response = self.client.post(
            '/api/branding/config',
            {
                'product_name': '星河智能标注',
                'primary_color': '#1D4ED8',
            },
            format='json',
        )
        assert update_response.status_code == 200
        assert update_response.json()['product_name'] == '星河智能标注'
        assert update_response.json()['primary_color'] == '#1D4ED8'
