_SIGNALS_REGISTERED = False

def create_principal(sender, instance, *args, **kwargs):
    instance.create_principal()


def delete_principal(sender, instance, *args, **kwargs):
    instance.delete_principal()
