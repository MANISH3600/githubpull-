from django.urls import path
from .views import add_slack_webhook  # Import your success view if created

urlpatterns = [
    path('add-slack-webhook/', add_slack_webhook, name='add_slack_webhook'),

]
