from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from .forms import KerberosUserCreationForm, DeactivateForm, PasswordlessResetForm
from .tokens import token_generator


class SignUpView(UserPassesTestMixin, CreateView):
    form_class = KerberosUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    # Limit signup ability to those invited by staff
    def test_func(self):

        # If FREE_SIGNUP is enabled allow users to sign themselves up
        if getattr(settings, 'FREE_SIGNUP', False):
            return True

        return self.request.user.is_staff


class DeactivateView(LoginRequiredMixin, FormView):
    form_class = DeactivateForm
    template_name = 'registration/deactivate.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Deactivate the current user
            user = request.user
            user.is_active = False
            user.scramble_password()
            user.save()

            return self.form_valid(form)

        return self.form_invalid(form)


class PasswordlessResetView(PasswordResetView):
    form_class = PasswordlessResetForm
    token_generator = token_generator


class PasswordlessResetConfirmView(PasswordResetConfirmView):
    token_generator = token_generator
