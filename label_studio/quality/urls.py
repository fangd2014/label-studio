from django.urls import path

from . import api

app_name = 'quality'

urlpatterns = [
    path('api/projects/<int:project_id>/quality/rules', api.ProjectQualityRulesAPI.as_view(), name='quality-rules'),
    path(
        'api/projects/<int:project_id>/quality/agreement',
        api.ProjectAgreementMetricsAPI.as_view(),
        name='quality-agreement',
    ),
]
