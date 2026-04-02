from django.urls import path

from . import api

app_name = 'identity'

urlpatterns = [
    path('api/identity/saml/login', api.SAMLLoginAPI.as_view(), name='identity-saml-login'),
    path('api/identity/scim/users', api.SCIMUserListCreateAPI.as_view(), name='identity-scim-users'),
    path('api/identity/scim/users/<str:external_id>', api.SCIMUserDetailAPI.as_view(), name='identity-scim-user'),
    path('api/identity/ldap/auth', api.LDAPAuthAPI.as_view(), name='identity-ldap-auth'),
]
