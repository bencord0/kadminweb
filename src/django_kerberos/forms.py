from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    PasswordResetForm,
    UserCreationForm,
    UserChangeForm,
    UsernameField,
)

from .tokens import token_generator


class KerberosUserCreationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
        field_classes = {
            'username': UsernameField,
            'email': forms.EmailField,
        }
        exclude = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True


class KerberosUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class PasswordlessResetForm(PasswordResetForm):
    def save(self, token_generator=token_generator, *args, **kwargs):
        return super().save(token_generator=token_generator, *args, **kwargs)


class DeactivateForm(forms.Form):
    deactivate = forms.BooleanField(label='Are you sure?', required=True)
