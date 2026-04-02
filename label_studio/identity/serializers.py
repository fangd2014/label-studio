from rest_framework import serializers


class IdentityAuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = serializers.DictField()


class SAMLLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    organization_id = serializers.IntegerField(required=False)


class SCIMProvisionSerializer(serializers.Serializer):
    external_id = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField(default=True)
    organization_id = serializers.IntegerField(required=False)
    workspace_external_ids = serializers.ListField(
        child=serializers.CharField(max_length=255), required=False, default=list
    )

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('username'):
            raise serializers.ValidationError('SCIM 同步至少需要 email 或 username')
        return attrs


class SCIMPatchSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField(required=False)
    organization_id = serializers.IntegerField(required=False)
    workspace_external_ids = serializers.ListField(
        child=serializers.CharField(max_length=255), required=False, default=list
    )


class LDAPAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SCIMUserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    active = serializers.BooleanField()
    external_id = serializers.CharField()
    workspace_ids = serializers.ListField(child=serializers.IntegerField(), default=list)
