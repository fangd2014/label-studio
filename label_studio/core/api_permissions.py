from core.permissions import get_view_permission_required, project_role_allows_permission
from rest_framework.permissions import SAFE_METHODS, BasePermission


class HasObjectPermission(BasePermission):
    message = '当前用户没有权限执行此操作。'

    def _get_project_from_object(self, obj):
        project = getattr(obj, 'project', None)
        if project is not None:
            return project

        task = getattr(obj, 'task', None)
        if task is not None:
            return getattr(task, 'project', None)

        if getattr(obj, '_meta', None) is not None and obj._meta.model_name == 'project':
            return obj

        return None

    def _get_project_from_view(self, view):
        if hasattr(view, 'get_project') and callable(view.get_project):
            try:
                return view.get_project()
            except Exception:
                return None

        kwargs = getattr(view, 'kwargs', {}) or {}
        project_id = kwargs.get('project_id')
        if project_id is None and view.__class__.__module__.startswith('projects.') and 'pk' in kwargs:
            project_id = kwargs.get('pk')

        if project_id is None:
            return None

        from projects.models import Project

        return Project.objects.filter(pk=project_id).first()

    def _is_project_owner_or_creator(self, user, project):
        if project is None:
            return False

        if project.created_by_id == user.id:
            return True

        organization = getattr(project, 'organization', None)
        return bool(organization and organization.created_by_id == user.id)

    def _get_user_project_role(self, user, project):
        if project is None:
            return None

        from projects.models import ProjectMember

        return (
            ProjectMember.objects.filter(user=user, project=project, enabled=True)
            .values_list('role', flat=True)
            .first()
        )

    def _has_project_role_permission(self, request, view, project):
        permission = get_view_permission_required(view, request.method)
        if permission is None or project is None:
            return True

        if self._is_project_owner_or_creator(request.user, project):
            return True

        role = self._get_user_project_role(request.user, project)
        allowed = project_role_allows_permission(role, permission)
        if not allowed:
            self.message = '当前项目角色无权执行此操作，请联系项目管理员。'
        return allowed

    def has_permission(self, request, view):
        project = self._get_project_from_view(view)
        return self._has_project_role_permission(request, view, project)

    def has_object_permission(self, request, view, obj):
        has_permission = getattr(obj, 'has_permission', None)
        if callable(has_permission) and not has_permission(request.user):
            self.message = '当前用户没有该资源访问权限。'
            return False

        project = self._get_project_from_object(obj) or self._get_project_from_view(view)
        return self._has_project_role_permission(request, view, project)


class MemberHasOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS and not request.user.own_organization:
            return False

        return obj.has_permission(request.user)
