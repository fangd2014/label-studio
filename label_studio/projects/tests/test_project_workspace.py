from organizations.tests.factories import OrganizationFactory
from projects.tests.factories import ProjectFactory
from rest_framework.test import APITestCase


class TestProjectWorkspace(APITestCase):
    def test_project_auto_binds_default_workspace(self):
        org = OrganizationFactory(created_by__username='workspace_owner')
        project = ProjectFactory(organization=org)
        project.refresh_from_db()

        assert hasattr(project, 'workspace_id')
        assert project.workspace_id is not None
