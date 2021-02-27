import kerberos
import logging
import subprocess

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
            # logging.exception("username/password mismatch")
            return False

    def set_password(self, username, password):
        subprocess.run(
            [
                'kadmin',
                '-r', settings.AUTH_SERVICE_REALM,
                '-p', settings.AUTH_SERVICE_NAME,
                '-kt', settings.KRB5_KTNAME,
                'change_password', '-pw', password, username,
            ],
            timeout=1,
            check=True,
        )

    def scramble_password(self, username):
        subprocess.run(
            [
                'kadmin',
                '-r', settings.AUTH_SERVICE_REALM,
                '-p', settings.AUTH_SERVICE_NAME,
                '-kt', settings.KRB5_KTNAME,
                'change_password', '-randkey', username,
            ],
            timeout=1,
            check=True,
        )

    def create_principal(self, username):
        subprocess.run(
            [
                'kadmin',
                '-r', settings.AUTH_SERVICE_REALM,
                '-p', settings.AUTH_SERVICE_NAME,
                '-kt', settings.KRB5_KTNAME,
                'add_principal', '-nokey',
                '+requires_preauth',
                '-allow_svr',
                username,
            ],
            timeout=1,
            check=True,
        )

    def delete_principal(self, username):
        if not username:
            return

        subprocess.run(
            [
                'kadmin',
                '-r', settings.AUTH_SERVICE_REALM,
                '-p', settings.AUTH_SERVICE_NAME,
                '-kt', settings.KRB5_KTNAME,
                'delete_principal', username,
            ],
            timeout=1,
            check=True,
        )
