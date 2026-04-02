from django.urls import path

from . import api

app_name = 'collaboration'

urlpatterns = [
    path(
        'api/projects/<int:project_id>/collaboration/comments',
        api.CollaborationCommentsAPI.as_view(),
        name='collaboration-comments',
    ),
    path(
        'api/collaboration/comments/<int:comment_id>',
        api.CollaborationCommentDetailAPI.as_view(),
        name='collaboration-comment-detail',
    ),
    path(
        'api/projects/<int:project_id>/collaboration/deep-link',
        api.CollaborationDeepLinkAPI.as_view(),
        name='collaboration-deep-link',
    ),
]
