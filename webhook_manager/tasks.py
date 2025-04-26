from celery import shared_task
from django.utils import timezone
from django.db import models
from accounts.models import PullRequest
import requests

@shared_task
def send_pull_request_notifications():
    current_date = timezone.now()
    notification_interval = timezone.timedelta(seconds=10)

    pull_requests = PullRequest.objects.prefetch_related('repository__slack_webhooks').filter(
        models.Q(last_notification_sent__isnull=True) |
        models.Q(last_notification_sent__lte=current_date - notification_interval)
    )

    for pr in pull_requests:
        time_open = current_date - pr.created_at
        slack_webhooks = pr.repository.slack_webhooks.all()

        if not slack_webhooks:
            print(f"No Slack webhooks found for repository '{pr.repository.name}'")
            continue

        for slack_webhook in slack_webhooks:
            if time_open.days >= 1:  
                message = (
                    f"*🚨 Hey Team! 🚨*\n\n"
                    f"*This pull request is taking too long!*\n\n"
                    f"⏳ The PR titled *'{pr.title}'* has been open for *{time_open.days} days, "
                    f"{time_open.seconds // 3600} hours, and {(time_open.seconds // 60) % 60} minutes*.\n\n"
                    f"*Please review it as soon as possible!*\n\n"
                    f"🔗 *[View the pull request here]*({pr.url})\n\n"
                    f"⏰ *Let's get this resolved quickly!*\n\n"
                    f"-----------------------------------------\n\n"
                    f"                                         \n\n*"

                )

            else:  
                message = (
                    f"*🔔 New Pull Request Notification!* 🔔\n\n"
                    f"📝 PR titled *'{pr.title}'* is now open.\n\n"
                    f"⏳ It has been open for *{time_open.days} days, "
                    f"{time_open.seconds // 3600} hours, and {(time_open.seconds // 60) % 60} minutes*.\n\n"
                    f"💬 *Please review and leave comments!*\n\n"
                    f"🔗 *[View the pull request here]*({pr.url})"
                )
                

            send_slack_notification(slack_webhook.url, message)


        pr.last_notification_sent = current_date
        pr.save()

def send_slack_notification(url, message):
    payload = {'text': message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification to Slack for {url}: {e}")
