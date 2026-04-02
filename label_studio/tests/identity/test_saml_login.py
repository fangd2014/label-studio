from organizations.tests.factories import OrganizationFactory
from rest_framework.test import APITestCase
from users.models import User


class TestSAMLLogin(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='saml_owner')

    def test_saml_login_create_and_update_user(self):
        payload = {
            'email': 'saml-user@example.com',
            'first_name': 'Sam',
            'last_name': 'Lee',
            'organization_id': self.organization.id,
        }

        first = self.client.post('/api/identity/saml/login', payload, format='json')
        assert first.status_code == 201
        assert first.json()['token']
        assert first.json()['user']['email'] == 'saml-user@example.com'

        second = self.client.post('/api/identity/saml/login', payload, format='json')
        assert second.status_code == 200

        user = User.objects.get(email='saml-user@example.com')
        assert user.active_organization_id == self.organization.id
        assert user.identity_provider == 'saml'
