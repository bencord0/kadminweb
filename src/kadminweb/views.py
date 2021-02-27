from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    context = {
        'admin_enabled': settings.ENABLE_ADMIN,
        'free_signup': settings.FREE_SIGNUP,
    }

    return render(request, 'index.html', context=context)
