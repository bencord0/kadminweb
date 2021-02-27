from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class KerberosUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        user = self.model(username=username, email=email, **extra_fields)

        user.create_principal()
        user.set_password(password)

        user.save(using=self._db)
        return user


class KerberosUser(AbstractUser):
    username = models.CharField(max_length=256, primary_key=True)

    # Do not store the password in the database
    # Instead, fetch and verify from kerberos
    password = None

    # Flag to indicate if the user principal exists in kerberos
    has_created_principal = models.BooleanField(default=False, editable=False)

    objects = KerberosUserManager()

    def set_password(self, raw_password):
        from .backends import KerberosBackend
        backend = KerberosBackend()
        return backend.set_password(self.username, raw_password)

    def scramble_password(self):
        from .backends import KerberosBackend
        backend = KerberosBackend()
        return backend.scramble_password(self.username)

    def check_password(self, raw_password):
        from .backends import KerberosBackend
        backend = KerberosBackend()
        return backend.check_password(self.username, raw_password)

    def _create_principal(self, username):
        from .backends import KerberosBackend
        backend = KerberosBackend()
        return backend.create_principal(username)

    def _delete_principal(self, username):
        from .backends import KerberosBackend
        backend = KerberosBackend()
        return backend.delete_principal(username)

    def create_principal(self):
        if not self.has_created_principal:
            self.has_created_principal = True
            self._create_principal(self.username)

    def delete_principal(self):
        self._delete_principal(self.username)
