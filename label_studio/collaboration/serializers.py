from urllib.parse import urlencode

from collaboration.models import CollaborationComment
from rest_framework import serializers


def build_deep_link(project_id, task_id=None, annotation_id=None, field=None):
    params = {}
    if task_id:
        params['task'] = task_id
    if annotation_id:
        params['annotation'] = annotation_id
    if field:
        params['field'] = field

    query = urlencode(params)
    if query:
        return f'/projects/{project_id}/data?{query}'
    return f'/projects/{project_id}/data'


class CollaborationCommentSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(required=False, allow_null=True)
    annotation_id = serializers.IntegerField(required=False, allow_null=True)
    created_by = serializers.IntegerField(source='created_by_id', read_only=True)
    resolved_by = serializers.IntegerField(source='resolved_by_id', read_only=True)
    deep_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CollaborationComment
        fields = [
            'id',
            'project',
            'task_id',
            'annotation_id',
            'created_by',
            'message',
            'resolved',
            'resolved_by',
            'created_at',
            'updated_at',
            'deep_link',
        ]
        read_only_fields = ['project', 'created_by', 'resolved_by', 'created_at', 'updated_at', 'deep_link']

    def get_deep_link(self, obj):
        task_id = obj.task_id
        if task_id is None and obj.annotation_id:
            task_id = obj.annotation.task_id

        return build_deep_link(
            project_id=obj.project_id,
            task_id=task_id,
            annotation_id=obj.annotation_id,
        )


class CollaborationResolveSerializer(serializers.Serializer):
    resolved = serializers.BooleanField(required=True)
