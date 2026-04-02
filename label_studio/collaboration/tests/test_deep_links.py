from organizations.tests.factories import OrganizationFactory
from projects.tests.factories import ProjectFactory
from rest_framework.test import APITestCase
from tasks.tests.factories import AnnotationFactory, TaskFactory


class TestCollaborationDeepLinksAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='deep_link_owner')
        cls.owner = cls.organization.created_by
        cls.project = ProjectFactory(organization=cls.organization, created_by=cls.owner)
        cls.task = TaskFactory(project=cls.project)
        cls.annotation = AnnotationFactory(task=cls.task, project=cls.project, completed_by=cls.owner, result=[])

    def test_generate_deep_link(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(
            f'/api/projects/{self.project.id}/collaboration/deep-link',
            {
                'task_id': self.task.id,
                'annotation_id': self.annotation.id,
                'field': 'sentiment',
            },
        )

        assert response.status_code == 200
        deep_link = response.json()['deep_link']
        assert deep_link.startswith(f'/projects/{self.project.id}/data?')
        assert f'task={self.task.id}' in deep_link
        assert f'annotation={self.annotation.id}' in deep_link
        assert 'field=sentiment' in deep_link
