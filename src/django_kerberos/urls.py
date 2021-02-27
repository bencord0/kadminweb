from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('deactivate/', views.DeactivateView.as_view(), name='deactivate'),
    path('password_reset/', views.PasswordlessResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordlessResetConfirmView.as_view(), name='password_reset_confirm'),
]
