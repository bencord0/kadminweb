import kerberos
import logging
import subprocess

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.debug import sensitive_variables

from .exceptions import KerberosManagementError


class KerberosBackend(ModelBackend):
    @sensitive_variables("password")
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not self.check_password(username, password):
            return None

        # User is now authenticated, create a User object
        UserModel = get_user_model()

        user, created = UserModel.objects.get_or_create(**{
            UserModel.USERNAME_FIELD: username,
        })

        return user

    @sensitive_variables("password")
    def check_password(self, username, password):
        try:
            return kerberos.checkPassword(
                username, password,
                getattr(settings, 'AUTH_SERVICE_NAME', 'http/app@example.com'),
                getattr(settings, 'AUTH_SERVICE_REALM', 'example.com'),
                True)
        except kerberos.BasicAuthError:
            # logging.exception("username/password mismatch")
            return False

    @sensitive_variables("password")
    def set_password(self, username, password):
        subprocess.run(
            [
                'kadmin',
                '-p', getattr(settings, 'AUTH_SERVICE_NAME', 'http/app@example.com'),
                '-r', getattr(settings, 'AUTH_SERVICE_REALM', 'example.com'),
                '-kt', getattr(settings, 'KRB5_KTNAME', '/etc/krb5.keytab'),
                'change_password', '-pw', password, username,
            ],
            timeout=5,
            check=True,
        )

    def scramble_password(self, username):
        subprocess.run(
            [
                'kadmin',
                '-p', getattr(settings, 'AUTH_SERVICE_NAME', 'http/app@example.com'),
                '-r', getattr(settings, 'AUTH_SERVICE_REALM', 'example.com'),
                '-kt', getattr(settings, 'KRB5_KTNAME', '/etc/krb5.keytab'),
                'change_password', '-randkey', username,
            ],
            timeout=1,
            check=True,
        )

    def create_principal(self, username):
        try:
            subprocess.run(
                [
                    'kadmin',
                    '-p', getattr(settings, 'AUTH_SERVICE_NAME', 'http/app@example.com'),
                    '-r', getattr(settings, 'AUTH_SERVICE_REALM', 'example.com'),
                    '-kt', getattr(settings, 'KRB5_KTNAME', '/etc/krb5.keytab'),
                    'add_principal', '-nokey',
                    '+requires_preauth',
                    '-allow_svr',
                    username,
                ],
                timeout=1,
                check=True,
            )
        except subprocess.CalledProcessError:
            raise KerberosManagementError

    def delete_principal(self, username):
        if not username:
            return

        subprocess.run(
            [
                'kadmin',
                '-p', getattr(settings, 'AUTH_SERVICE_NAME', 'http/app@example.com'),
                '-r', getattr(settings, 'AUTH_SERVICE_REALM', 'example.com'),
                '-kt', getattr(settings, 'KRB5_KTNAME', '/etc/krb5.keytab'),
                'delete_principal', username,
            ],
            timeout=1,
            check=True,
        )
