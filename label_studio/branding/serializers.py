from rest_framework import serializers


class BrandingConfigSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=128)
    logo_url = serializers.CharField(required=False, allow_blank=True)
    primary_color = serializers.RegexField(regex=r'^#[0-9A-Fa-f]{6}$')
    login_page_url = serializers.CharField(required=False, allow_blank=True)
    support_url = serializers.CharField(required=False, allow_blank=True)


class BrandingConfigUpdateSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=128, required=False)
    logo_url = serializers.CharField(required=False, allow_blank=True)
    primary_color = serializers.RegexField(regex=r'^#[0-9A-Fa-f]{6}$', required=False)
    login_page_url = serializers.CharField(required=False, allow_blank=True)
    support_url = serializers.CharField(required=False, allow_blank=True)
