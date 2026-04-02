from organizations.tests.factories import OrganizationFactory
from rest_framework.test import APITestCase
from users.models import User


class TestSCIMApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='identity_owner')
        cls.owner = cls.organization.created_by

    def test_scim_create_user(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            '/api/identity/scim/users',
            {
                'external_id': 'scim-user-1',
                'email': 'scim-user-1@example.com',
                'first_name': 'SCIM',
                'last_name': 'User',
                'organization_id': self.organization.id,
                'active': True,
            },
            format='json',
        )

        assert response.status_code == 201
        assert response.json()['external_id'] == 'scim-user-1'
        assert response.json()['email'] == 'scim-user-1@example.com'
        assert response.json()['active'] is True

        user = User.objects.get(identity_external_id='scim-user-1')
        assert user.active_organization_id == self.organization.id
        assert user.identity_provider == 'scim'
