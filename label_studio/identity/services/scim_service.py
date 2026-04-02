import secrets

from django.utils import timezone
from organizations.models import Organization, Workspace
from users.models import User


class SCIMService:
    @staticmethod
    def _resolve_organization(payload):
        organization_id = payload.get('organization_id')
        if not organization_id:
            return None
        return Organization.objects.filter(pk=organization_id).first()

    @classmethod
    def provision_user(cls, payload):
        external_id = payload['external_id'].strip()
        email = payload.get('email', '').strip().lower()
        username = payload.get('username', '').strip()

        user = User.objects.filter(identity_external_id=external_id).first()
        created = False

        if not user and email:
            user = User.objects.filter(email=email).first()

        if not user:
            effective_email = email or f'{external_id}@scim.local'
            user = User.objects.create_user(
                email=effective_email,
                password=secrets.token_urlsafe(24),
                username=username or effective_email.split('@')[0],
                first_name=payload.get('first_name', '').strip(),
                last_name=payload.get('last_name', '').strip(),
                is_active=payload.get('active', True),
            )
            created = True

        updated_fields = []
        if email and user.email != email:
            user.email = email
            updated_fields.append('email')
        if username and user.username != username:
            user.username = username
            updated_fields.append('username')

        first_name = payload.get('first_name')
        if first_name is not None and user.first_name != first_name.strip():
            user.first_name = first_name.strip()
            updated_fields.append('first_name')

        last_name = payload.get('last_name')
        if last_name is not None and user.last_name != last_name.strip():
            user.last_name = last_name.strip()
            updated_fields.append('last_name')

        active = payload.get('active')
        if active is not None and user.is_active != active:
            user.is_active = active
            updated_fields.append('is_active')

        if user.identity_external_id != external_id:
            user.identity_external_id = external_id
            updated_fields.append('identity_external_id')
        if user.identity_provider != 'scim':
            user.identity_provider = 'scim'
            updated_fields.append('identity_provider')
        if not user.is_identity_managed:
            user.is_identity_managed = True
            updated_fields.append('is_identity_managed')

        user.identity_synced_at = timezone.now()
        updated_fields.append('identity_synced_at')

        organization = cls._resolve_organization(payload)
        if organization:
            if not organization.has_user(user):
                organization.add_user(user)
            if user.active_organization_id != organization.id:
                user.active_organization = organization
                updated_fields.append('active_organization')

        if updated_fields:
            user.save(update_fields=list(dict.fromkeys(updated_fields)))

        workspace_ids = []
        workspace_external_ids = payload.get('workspace_external_ids') or []
        if organization and workspace_external_ids:
            workspace_ids = list(
                Workspace.objects.filter(
                    organization=organization, external_group_id__in=workspace_external_ids
                ).values_list('id', flat=True)
            )

        return user, created, workspace_ids

    @staticmethod
    def deactivate_user(external_id):
        user = User.objects.filter(identity_external_id=external_id).first()
        if not user:
            return None

        updated_fields = []
        if user.is_active:
            user.is_active = False
            updated_fields.append('is_active')

        user.identity_synced_at = timezone.now()
        updated_fields.append('identity_synced_at')
        user.save(update_fields=updated_fields)
        return user
