# webhook_manager/urls.py
from django.urls import path,include
from .views import setup_webhook, github_webhook

urlpatterns = [
    path('setup/', setup_webhook, name='setup_webhook'),
    path('webhook/', github_webhook, name='webhook'),
    path('accounts/', include('accounts.urls')),
]
