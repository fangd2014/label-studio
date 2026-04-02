from django.contrib.auth import authenticate
from django.utils import timezone
from users.models import User


class LDAPService:
    @staticmethod
    def authenticate_user(email, password):
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user and not user.check_password(password):
            user = None

        if user is None:
            user = authenticate(email=email, password=password)
        if user is None:
            return None

        updated_fields = []
        if user.identity_provider != 'ldap':
            user.identity_provider = 'ldap'
            updated_fields.append('identity_provider')
        if not user.is_identity_managed:
            user.is_identity_managed = True
            updated_fields.append('is_identity_managed')

        user.identity_synced_at = timezone.now()
        updated_fields.append('identity_synced_at')

        user.save(update_fields=updated_fields)
        return user
