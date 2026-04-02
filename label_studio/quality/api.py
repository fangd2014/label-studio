from core.permissions import ViewClassPermission, all_permissions
from projects.models import Project
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AgreementMetricsSerializer, QualityRulesSerializer
from .services import calculate_exact_match_agreement


class ProjectQualityRulesAPI(APIView):
    permission_required = ViewClassPermission(
        GET=all_permissions.projects_view,
        PATCH=all_permissions.projects_change,
    )

    def _get_project(self, request, project_id):
        project = Project.objects.filter(pk=project_id, organization=request.user.active_organization).first()
        if project is None:
            return None
        self.check_object_permissions(request, project)
        return project

    def get(self, request, project_id):
        project = self._get_project(request, project_id)
        if project is None:
            return Response({'detail': '项目不存在'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'quality_rules': project.quality_rules or {},
            'low_trust_threshold': project.low_trust_threshold,
            'annotator_evaluation_enabled': project.annotator_evaluation_enabled,
            'maximum_annotations': project.maximum_annotations,
        }
        serializer = QualityRulesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

    def patch(self, request, project_id):
        project = self._get_project(request, project_id)
        if project is None:
            return Response({'detail': '项目不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QualityRulesSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        update_fields = []
        if 'quality_rules' in payload:
            project.quality_rules = payload['quality_rules']
            update_fields.append('quality_rules')
        if 'low_trust_threshold' in payload:
            project.low_trust_threshold = payload['low_trust_threshold']
            update_fields.append('low_trust_threshold')
        if 'annotator_evaluation_enabled' in payload:
            project.annotator_evaluation_enabled = payload['annotator_evaluation_enabled']
            update_fields.append('annotator_evaluation_enabled')
        if 'maximum_annotations' in payload:
            project.maximum_annotations = payload['maximum_annotations']
            update_fields.append('maximum_annotations')

        if update_fields:
            project.save(update_fields=update_fields)

        return self.get(request, project_id)


class ProjectAgreementMetricsAPI(APIView):
    permission_required = all_permissions.projects_view

    def get(self, request, project_id):
        project = Project.objects.filter(pk=project_id, organization=request.user.active_organization).first()
        if project is None:
            return Response({'detail': '项目不存在'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        data = calculate_exact_match_agreement(project)
        serializer = AgreementMetricsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
