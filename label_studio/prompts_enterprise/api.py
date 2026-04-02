from core.permissions import ViewClassPermission, all_permissions
from django.conf import settings
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


class PromptsConfigSerializer(serializers.Serializer):
    enabled = serializers.BooleanField()
    providers = serializers.ListField(child=serializers.CharField())
    status = serializers.CharField()


class PromptsConfigUpdateSerializer(serializers.Serializer):
    enabled = serializers.BooleanField(required=True)


class PromptsEnterpriseConfigAPI(APIView):
    permission_required = ViewClassPermission(
        GET=all_permissions.projects_view,
        POST=all_permissions.projects_change,
    )

    def _build_payload(self, enabled):
        payload = {
            'enabled': enabled,
            'providers': ['openai', 'anthropic', 'custom'],
            'status': 'placeholder',
        }
        serializer = PromptsConfigSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def get(self, request):
        enabled = request.session.get('prompts_enterprise_enabled', settings.PROMPTS_ENTERPRISE_ENABLED)
        return Response(self._build_payload(bool(enabled)), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PromptsConfigUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.session['prompts_enterprise_enabled'] = serializer.validated_data['enabled']
        return Response(self._build_payload(serializer.validated_data['enabled']), status=status.HTTP_200_OK)
