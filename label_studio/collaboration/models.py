from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class CollaborationComment(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='collaboration_comments')
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        related_name='collaboration_comments',
        null=True,
        blank=True,
    )
    annotation = models.ForeignKey(
        'tasks.Annotation',
        on_delete=models.SET_NULL,
        related_name='collaboration_comments',
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='collaboration_comments',
        null=True,
        blank=True,
    )
    message = models.TextField(_('message'))
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='resolved_collaboration_comments',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'collaboration_comment'
        ordering = ['-created_at', '-id']
