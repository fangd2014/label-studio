"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license."""

import logging  # noqa: I001
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

import rules

logger = logging.getLogger(__name__)


class AllPermissions(BaseModel):
    model_config = ConfigDict(protected_namespaces=('__.*__', '_.*'))

    organizations_create: str = 'organizations.create'
    organizations_view: str = 'organizations.view'
    organizations_change: str = 'organizations.change'
    organizations_delete: str = 'organizations.delete'
    organizations_invite: str = 'organizations.invite'
    projects_create: str = 'projects.create'
    projects_view: str = 'projects.view'
    projects_change: str = 'projects.change'
    projects_delete: str = 'projects.delete'
    projects_reset_cache: str = 'projects.reset_cache'
    tasks_create: str = 'tasks.create'
    tasks_view: str = 'tasks.view'
    tasks_change: str = 'tasks.change'
    tasks_delete: str = 'tasks.delete'
    views_reset: str = 'views.reset'
    annotations_create: str = 'annotations.create'
    annotations_view: str = 'annotations.view'
    annotations_change: str = 'annotations.change'
    annotations_delete: str = 'annotations.delete'
    actions_perform: str = 'actions.perform'
    predictions_any: str = 'predictions.any'
    avatar_any: str = 'avatar.any'
    labels_create: str = 'labels.create'
    labels_view: str = 'labels.view'
    labels_change: str = 'labels.change'
    labels_delete: str = 'labels.delete'
    models_create: str = 'models.create'
    models_view: str = 'models.view'
    models_change: str = 'models.change'
    models_delete: str = 'models.delete'
    model_provider_connection_create: str = 'model_provider_connection.create'
    model_provider_connection_view: str = 'model_provider_connection.view'
    model_provider_connection_change: str = 'model_provider_connection.change'
    model_provider_connection_delete: str = 'model_provider_connection.delete'
    webhooks_view: str = 'webhooks.view'
    webhooks_change: str = 'webhooks.change'
    users_token_any: str = 'users.token.any'

    storages_view: str = 'storages.view'
    storages_change: str = 'storages.change'
    storages_sync: str = 'storages.sync'

    views_view: str = 'views.view'
    views_create: str = 'views.create'
    views_change: str = 'views.change'
    views_delete: str = 'views.delete'


all_permissions = AllPermissions()

PROJECT_ROLE_ANNOTATOR = 'annotator'
PROJECT_ROLE_REVIEWER = 'reviewer'
PROJECT_ROLE_MANAGER = 'manager'

PROJECT_ROLE_MANAGER_ONLY_PERMISSIONS = frozenset(
    {
        all_permissions.projects_create,
        all_permissions.projects_change,
        all_permissions.projects_delete,
        all_permissions.projects_reset_cache,
        all_permissions.tasks_create,
        all_permissions.tasks_change,
        all_permissions.tasks_delete,
        all_permissions.views_create,
        all_permissions.views_change,
        all_permissions.views_delete,
        all_permissions.views_reset,
        all_permissions.labels_create,
        all_permissions.labels_change,
        all_permissions.labels_delete,
        all_permissions.models_create,
        all_permissions.models_change,
        all_permissions.models_delete,
        all_permissions.storages_change,
        all_permissions.storages_sync,
        all_permissions.webhooks_change,
    }
)


def get_view_permission_required(view: Any, method: str) -> Optional[str]:
    """Resolve the permission code configured on a view for the current HTTP method."""
    permission_required = getattr(view, 'permission_required', None)
    if permission_required is None:
        return None

    if isinstance(permission_required, str):
        return permission_required

    if isinstance(permission_required, ViewClassPermission):
        return getattr(permission_required, method, None)

    if hasattr(permission_required, method):
        return getattr(permission_required, method)

    return None


def project_role_allows_permission(role: Optional[str], permission: Optional[str]) -> bool:
    """Check if a project role allows a given permission code."""
    if permission is None:
        return True

    if role == PROJECT_ROLE_MANAGER:
        return True

    if role in {PROJECT_ROLE_ANNOTATOR, PROJECT_ROLE_REVIEWER}:
        return permission not in PROJECT_ROLE_MANAGER_ONLY_PERMISSIONS

    # Backward-compatible fallback when no project role is assigned.
    return True


class ViewClassPermission(BaseModel):
    GET: Optional[str] = None
    PATCH: Optional[str] = None
    PUT: Optional[str] = None
    DELETE: Optional[str] = None
    POST: Optional[str] = None


def make_perm(name, pred, overwrite=False):
    if rules.perm_exists(name):
        if overwrite:
            rules.remove_perm(name)
        else:
            return
    rules.add_perm(name, pred)


for _, permission_name in all_permissions:
    make_perm(permission_name, rules.is_authenticated)
