from django.test import override_settings
from rest_framework.test import APITestCase
from users.models import User


@override_settings(LDAP_ENABLED=True)
class TestLDAPAuth(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='ldap-user@example.com',
            username='ldap-user',
            password='ldap-pass-123',
        )

    def test_ldap_auth_success(self):
        response = self.client.post(
            '/api/identity/ldap/auth',
            {
                'email': 'ldap-user@example.com',
                'password': 'ldap-pass-123',
            },
            format='json',
        )

        assert response.status_code == 200
        assert response.json()['token']
        assert response.json()['user']['email'] == 'ldap-user@example.com'

    def test_ldap_auth_failed(self):
        response = self.client.post(
            '/api/identity/ldap/auth',
            {
                'email': 'ldap-user@example.com',
                'password': 'wrong-password',
            },
            format='json',
        )
        assert response.status_code == 401
