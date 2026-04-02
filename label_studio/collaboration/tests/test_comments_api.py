from organizations.tests.factories import OrganizationFactory
from projects.tests.factories import ProjectFactory
from rest_framework.test import APITestCase
from tasks.tests.factories import AnnotationFactory, TaskFactory


class TestCollaborationCommentsAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='collab_owner')
        cls.owner = cls.organization.created_by
        cls.project = ProjectFactory(organization=cls.organization, created_by=cls.owner)
        cls.task = TaskFactory(project=cls.project)
        cls.annotation = AnnotationFactory(task=cls.task, project=cls.project, completed_by=cls.owner, result=[])

    def comments_url(self):
        return f'/api/projects/{self.project.id}/collaboration/comments'

    def test_create_list_and_resolve_comments(self):
        self.client.force_authenticate(user=self.owner)

        create_response = self.client.post(
            self.comments_url(),
            {
                'message': '请关注这个区域的标注边界',
                'task_id': self.task.id,
                'annotation_id': self.annotation.id,
            },
            format='json',
        )
        assert create_response.status_code == 201
        body = create_response.json()
        assert body['message'] == '请关注这个区域的标注边界'
        assert f'task={self.task.id}' in body['deep_link']
        assert f'annotation={self.annotation.id}' in body['deep_link']

        list_response = self.client.get(self.comments_url())
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        comment_id = body['id']
        resolve_response = self.client.patch(
            f'/api/collaboration/comments/{comment_id}',
            {'resolved': True},
            format='json',
        )
        assert resolve_response.status_code == 200
        assert resolve_response.json()['resolved'] is True
        assert resolve_response.json()['resolved_by'] == self.owner.id
