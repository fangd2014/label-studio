from django.utils import timezone
from organizations.models import Organization
from users.models import User


class SAMLService:
    @staticmethod
    def login(payload):
        email = payload['email'].strip().lower()
        first_name = payload.get('first_name', '').strip()
        last_name = payload.get('last_name', '').strip()
        organization_id = payload.get('organization_id')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': first_name,
                'last_name': last_name,
                'identity_provider': 'saml',
                'is_identity_managed': True,
                'identity_synced_at': timezone.now(),
            },
        )

        updated_fields = []
        if not created:
            if first_name and user.first_name != first_name:
                user.first_name = first_name
                updated_fields.append('first_name')
            if last_name and user.last_name != last_name:
                user.last_name = last_name
                updated_fields.append('last_name')

        if user.identity_provider != 'saml':
            user.identity_provider = 'saml'
            updated_fields.append('identity_provider')
        if not user.is_identity_managed:
            user.is_identity_managed = True
            updated_fields.append('is_identity_managed')

        user.identity_synced_at = timezone.now()
        updated_fields.append('identity_synced_at')

        if organization_id:
            organization = Organization.objects.filter(pk=organization_id).first()
            if organization:
                if not organization.has_user(user):
                    organization.add_user(user)
                if user.active_organization_id != organization.id:
                    user.active_organization = organization
                    updated_fields.append('active_organization')

        if updated_fields:
            user.save(update_fields=list(dict.fromkeys(updated_fields)))

        return user, created
