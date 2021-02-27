from django.conf import settings
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(TemplateView):
    http_method_names = ['get']
    template_name = 'index.html'
    extra_context = {
        'admin_enabled': settings.ENABLE_ADMIN,
        'free_signup': settings.FREE_SIGNUP,
    }
