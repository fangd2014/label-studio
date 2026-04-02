from organizations.tests.factories import OrganizationFactory
from rest_framework.test import APITestCase
from users.models import User


class TestSCIMIdempotent(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='scim_idempotent_owner')
        cls.owner = cls.organization.created_by

    def test_scim_create_idempotent_by_external_id(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            'external_id': 'scim-idempotent-1',
            'email': 'idempotent@example.com',
            'first_name': 'First',
            'last_name': 'Version',
            'organization_id': self.organization.id,
        }

        first = self.client.post('/api/identity/scim/users', payload, format='json')
        assert first.status_code == 201

        second = self.client.post('/api/identity/scim/users', payload, format='json')
        assert second.status_code == 200

        assert User.objects.filter(identity_external_id='scim-idempotent-1').count() == 1
