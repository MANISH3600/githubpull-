from celery import shared_task
from django.utils import timezone
from django.db import models
from accounts.models import PullRequest
import requests

@shared_task
def send_pull_request_notifications():
    current_date = timezone.now()
    
    # Define the notification interval (10 seconds for testing)
    notification_interval = timezone.timedelta(seconds=10)

    # Fetch all pull requests that need notifications
    pull_requests = PullRequest.objects.prefetch_related('repository__slack_webhooks').filter(
        models.Q(last_notification_sent__isnull=True) |
        models.Q(last_notification_sent__lte=current_date - notification_interval)
    )

    # Loop through each pull request
    for pr in pull_requests:
        time_open = current_date - pr.created_at
        
        # Get associated Slack webhooks
        slack_webhooks = pr.repository.slack_webhooks.all()

        if not slack_webhooks:
            print(f"No Slack webhooks found for repository '{pr.repository.name}'")
            continue

        # Send notifications to each Slack webhook
        for slack_webhook in slack_webhooks:
            send_slack_notification(slack_webhook.url, pr, time_open)

        # Update the last notification sent time
        pr.last_notification_sent = current_date
        pr.save()

def send_slack_notification(url, pull_request, time_open):
    message = (
        f"New Pull Request:\n"
        f"- Title: {pull_request.title}\n"
        f"- URL: {pull_request.url}\n"
        f"- Opened for: {time_open.days} days, {time_open.seconds // 3600} hours, "
        f"and {(time_open.seconds // 60) % 60} minutes\n"
    )

    payload = {'text': message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification to Slack for {url}: {e}")
