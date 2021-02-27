from django.apps import AppConfig
from django.db.models.signals import pre_delete, pre_save
from . import signals


class KerberosConfig(AppConfig):
    name = 'django_kerberos'

    def ready(self):
        if not signals._SIGNALS_REGISTERED:
            signals._SIGNALS_REGISTERED = True
            self._register_signals()

    def _register_signals(self):
        KerberosUser = self.get_model('KerberosUser')

        # Create the kerberos principal for new users
        pre_save.connect(signals.create_principal, KerberosUser)
        pre_delete.connect(signals.delete_principal, KerberosUser)
