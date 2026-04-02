from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.api import issue_auth_payload
from users.models import User

from .serializers import (
    LDAPAuthSerializer,
    SAMLLoginSerializer,
    SCIMPatchSerializer,
    SCIMProvisionSerializer,
    SCIMUserResponseSerializer,
)
from .services.ldap_service import LDAPService
from .services.saml_service import SAMLService
from .services.scim_service import SCIMService


def _serialize_scim_user(user, workspace_ids):
    payload = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name or '',
        'last_name': user.last_name or '',
        'active': user.is_active,
        'external_id': user.identity_external_id or '',
        'workspace_ids': workspace_ids or [],
    }
    serializer = SCIMUserResponseSerializer(data=payload)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


class SAMLLoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if not settings.IDENTITY_SAML_ENABLED:
            return Response({'detail': 'SAML 登录未启用'}, status=status.HTTP_403_FORBIDDEN)

        serializer = SAMLLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, created = SAMLService.login(serializer.validated_data)
        payload = issue_auth_payload(user)
        return Response(payload, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class SCIMUserListCreateAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SCIMProvisionSerializer

    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(identity_provider='scim').order_by('id')
        payload = [_serialize_scim_user(user, []) for user in queryset]
        return Response(payload, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not settings.IDENTITY_SCIM_ENABLED:
            return Response({'detail': 'SCIM 同步未启用'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, created, workspace_ids = SCIMService.provision_user(serializer.validated_data)
        payload = _serialize_scim_user(user, workspace_ids)
        return Response(payload, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class SCIMUserDetailAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SCIMPatchSerializer

    def patch(self, request, external_id, *args, **kwargs):
        user = User.objects.filter(identity_external_id=external_id).first()
        if not user:
            return Response({'detail': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = {'external_id': external_id, **serializer.validated_data}
        user, _, workspace_ids = SCIMService.provision_user(payload)
        return Response(_serialize_scim_user(user, workspace_ids), status=status.HTTP_200_OK)

    def delete(self, request, external_id, *args, **kwargs):
        user = SCIMService.deactivate_user(external_id)
        if not user:
            return Response({'detail': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LDAPAuthAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if not settings.LDAP_ENABLED:
            return Response({'detail': 'LDAP 认证未启用'}, status=status.HTTP_403_FORBIDDEN)

        serializer = LDAPAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = LDAPService.authenticate_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        if not user:
            return Response({'detail': 'LDAP 认证失败'}, status=status.HTTP_401_UNAUTHORIZED)

        payload = issue_auth_payload(user)
        return Response(payload, status=status.HTTP_200_OK)
