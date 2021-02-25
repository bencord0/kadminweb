from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class KerberosUserManager(UserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        # remove the 'password' field which is not available on this model
        extra_fields.pop('password', None)

        user = self.model(username=username, email=email, **extra_fields)
        user.save(using=self._db)
        return user


class KerberosUser(AbstractUser):
    username = models.CharField(max_length=256, primary_key=True)

    # Do not store the password in the database
    # Instead, fetch and verify from kerberos
    password = None

    objects = KerberosUserManager()

    def set_password(self, raw_password):
        from .backends import KerberosBackend
        backend = KerberosBackend()
        return backend.set_password(self.username, raw_password)

    def check_password(self, raw_password):
        from .backends import KerberosBackend
        backend = KerberosBackend()
        return backend.check_password(self.username, raw_password)
