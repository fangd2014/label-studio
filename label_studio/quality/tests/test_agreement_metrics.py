from organizations.tests.factories import OrganizationFactory
from projects.tests.factories import ProjectFactory
from rest_framework.test import APITestCase
from tasks.tests.factories import AnnotationFactory, TaskFactory
from users.tests.factories import UserFactory


class TestAgreementMetricsAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='agreement_owner')
        cls.owner = cls.organization.created_by
        cls.project = ProjectFactory(organization=cls.organization, created_by=cls.owner)
        cls.task = TaskFactory(project=cls.project)
        cls.user_a = UserFactory(active_organization=cls.organization)
        cls.user_b = UserFactory(active_organization=cls.organization)
        cls.user_c = UserFactory(active_organization=cls.organization)

        result_positive = [
            {
                'from_name': 'sentiment',
                'to_name': 'text',
                'type': 'choices',
                'value': {'choices': ['positive']},
            }
        ]
        result_negative = [
            {
                'from_name': 'sentiment',
                'to_name': 'text',
                'type': 'choices',
                'value': {'choices': ['negative']},
            }
        ]
        AnnotationFactory(task=cls.task, project=cls.project, completed_by=cls.user_a, result=result_positive)
        AnnotationFactory(task=cls.task, project=cls.project, completed_by=cls.user_b, result=result_positive)
        AnnotationFactory(task=cls.task, project=cls.project, completed_by=cls.user_c, result=result_negative)

    def test_agreement_metrics(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f'/api/projects/{self.project.id}/quality/agreement')

        assert response.status_code == 200
        body = response.json()
        assert body['metric'] == 'exact_match_consensus'
        assert body['tasks_evaluated'] == 1
        assert body['annotations_evaluated'] == 3
        assert abs(body['score'] - 0.6667) < 0.0001
