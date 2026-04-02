from django.urls import path

from . import api

app_name = 'branding'

urlpatterns = [
    path('api/branding/config', api.BrandingConfigAPI.as_view(), name='branding-config'),
]
