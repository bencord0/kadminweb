from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserCreationForm,
    UserChangeForm,
    UsernameField,
)


class KerberosUserCreationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)
        field_classes = {'username': UsernameField}
        exclude = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True


class KerberosUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)
