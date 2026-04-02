from branding.serializers import BrandingConfigSerializer, BrandingConfigUpdateSerializer
from core.permissions import ViewClassPermission, all_permissions
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class BrandingConfigAPI(APIView):
    permission_required = ViewClassPermission(
        GET=all_permissions.projects_view,
        POST=all_permissions.projects_change,
    )

    SESSION_KEY = 'branding_config_override'

    def _base_config(self):
        return {
            'product_name': settings.BRANDING_PRODUCT_NAME,
            'logo_url': settings.BRANDING_LOGO_URL,
            'primary_color': settings.BRANDING_PRIMARY_COLOR,
            'login_page_url': settings.LOGIN_PAGE_URL,
            'support_url': settings.BRANDING_SUPPORT_URL,
        }

    def _current_config(self, request):
        config = self._base_config()
        config.update(request.session.get(self.SESSION_KEY, {}))
        serializer = BrandingConfigSerializer(data=config)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def get(self, request):
        return Response(self._current_config(request), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BrandingConfigUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        override = request.session.get(self.SESSION_KEY, {})
        override.update(serializer.validated_data)
        request.session[self.SESSION_KEY] = override

        return Response(self._current_config(request), status=status.HTTP_200_OK)
