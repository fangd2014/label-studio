from collaboration.models import CollaborationComment
from collaboration.serializers import (
    CollaborationCommentSerializer,
    CollaborationResolveSerializer,
    build_deep_link,
)
from core.permissions import ViewClassPermission, all_permissions
from projects.models import Project
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.models import Annotation, Task


class CollaborationCommentsAPI(APIView):
    permission_required = ViewClassPermission(
        GET=all_permissions.projects_view,
        POST=all_permissions.tasks_change,
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

        comments = CollaborationComment.objects.filter(project=project).select_related('annotation', 'task')
        serializer = CollaborationCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        project = self._get_project(request, project_id)
        if project is None:
            return Response({'detail': '项目不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollaborationCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = None
        annotation = None
        task_id = serializer.validated_data.get('task_id')
        annotation_id = serializer.validated_data.get('annotation_id')

        if task_id is not None:
            task = Task.objects.filter(pk=task_id, project=project).first()
            if task is None:
                return Response({'detail': '任务不存在或不属于当前项目'}, status=status.HTTP_400_BAD_REQUEST)

        if annotation_id is not None:
            annotation = Annotation.objects.filter(pk=annotation_id, project=project).first()
            if annotation is None:
                return Response({'detail': '标注不存在或不属于当前项目'}, status=status.HTTP_400_BAD_REQUEST)
            if task is None:
                task = annotation.task

        comment = CollaborationComment.objects.create(
            project=project,
            task=task,
            annotation=annotation,
            created_by=request.user,
            message=serializer.validated_data['message'],
            resolved=serializer.validated_data.get('resolved', False),
        )

        response_serializer = CollaborationCommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CollaborationCommentDetailAPI(APIView):
    permission_required = ViewClassPermission(
        PATCH=all_permissions.tasks_change,
    )

    def patch(self, request, comment_id):
        comment = CollaborationComment.objects.filter(pk=comment_id).select_related('project').first()
        if comment is None:
            return Response({'detail': '评论不存在'}, status=status.HTTP_404_NOT_FOUND)
        if comment.project.organization_id != request.user.active_organization_id:
            return Response({'detail': '评论不存在'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, comment.project)

        serializer = CollaborationResolveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resolved = serializer.validated_data['resolved']
        comment.resolved = resolved
        comment.resolved_by = request.user if resolved else None
        comment.save(update_fields=['resolved', 'resolved_by', 'updated_at'])

        response_serializer = CollaborationCommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class CollaborationDeepLinkAPI(APIView):
    permission_required = all_permissions.projects_view

    def get(self, request, project_id):
        project = Project.objects.filter(pk=project_id, organization=request.user.active_organization).first()
        if project is None:
            return Response({'detail': '项目不存在'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        task_id = request.query_params.get('task_id')
        annotation_id = request.query_params.get('annotation_id')
        field = request.query_params.get('field')

        if task_id:
            task_exists = Task.objects.filter(pk=task_id, project=project).exists()
            if not task_exists:
                return Response({'detail': '任务不存在'}, status=status.HTTP_400_BAD_REQUEST)

        if annotation_id:
            annotation_exists = Annotation.objects.filter(pk=annotation_id, project=project).exists()
            if not annotation_exists:
                return Response({'detail': '标注不存在'}, status=status.HTTP_400_BAD_REQUEST)

        deep_link = build_deep_link(project.id, task_id=task_id, annotation_id=annotation_id, field=field)
        return Response({'deep_link': deep_link}, status=status.HTTP_200_OK)
