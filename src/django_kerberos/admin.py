from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import (
    KerberosUserCreationForm,
    KerberosUserChangeForm,
)


KerberosUser = get_user_model()


class KerberosUserAdmin(UserAdmin):
    add_form = KerberosUserCreationForm
    form = KerberosUserChangeForm
    model = KerberosUser
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
    )


admin.site.register(KerberosUser, KerberosUserAdmin)
