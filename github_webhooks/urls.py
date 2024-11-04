# github_webhooks/urls.py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webhook_manager.urls')),
    path('accounts/',include('accounts.urls'))

    
]

