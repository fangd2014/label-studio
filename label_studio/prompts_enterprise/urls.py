from django.urls import path

from . import api

app_name = 'prompts_enterprise'

urlpatterns = [
    path('api/prompts-enterprise/config', api.PromptsEnterpriseConfigAPI.as_view(), name='prompts-enterprise-config'),
]
