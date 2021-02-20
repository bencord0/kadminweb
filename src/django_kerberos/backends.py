import kerberos
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class KerberosBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not self.check_password(username, password):
            return None

        # User is now authenticated, create a User object
        UserModel = get_user_model()

        user, created = UserModel.objects.get_or_create(**{
            UserModel.USERNAME_FIELD: username,
        })

        return user

    def check_password(self, username, password):
        try:
            return kerberos.checkPassword(
                username, password,
                settings.AUTH_SERVICE_NAME,
                settings.AUTH_SERVICE_REALM,
                True)
        except kerberos.BasicAuthError:
            logging.exception("username/password mismatch")
            return False
