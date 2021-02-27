from .exceptions import KerberosManagementError

_SIGNALS_REGISTERED = False


def create_principal(sender, instance, *args, **kwargs):
    try:
        instance.create_principal()
    except KerberosManagementError:
        # User already exists in kerberos database
        pass


def delete_principal(sender, instance, *args, **kwargs):
    instance.delete_principal()
