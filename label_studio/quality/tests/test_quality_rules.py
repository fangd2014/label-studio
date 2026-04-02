from organizations.tests.factories import OrganizationFactory
from projects.tests.factories import ProjectFactory
from rest_framework.test import APITestCase


class TestQualityRulesAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='quality_owner')
        cls.owner = cls.organization.created_by
        cls.project = ProjectFactory(organization=cls.organization, created_by=cls.owner)

    def url(self):
        return f'/api/projects/{self.project.id}/quality/rules'

    def test_get_and_patch_quality_rules(self):
        self.client.force_authenticate(user=self.owner)

        get_response = self.client.get(self.url())
        assert get_response.status_code == 200
        assert get_response.json()['quality_rules'] == {}

        payload = {
            'quality_rules': {
                'auto_validation': True,
                'low_agreement_action': 'review_required',
            },
            'low_trust_threshold': 0.4,
            'annotator_evaluation_enabled': True,
            'maximum_annotations': 3,
        }

        patch_response = self.client.patch(self.url(), payload, format='json')
        assert patch_response.status_code == 200
        body = patch_response.json()
        assert body['quality_rules']['auto_validation'] is True
        assert body['low_trust_threshold'] == 0.4
        assert body['annotator_evaluation_enabled'] is True
        assert body['maximum_annotations'] == 3
