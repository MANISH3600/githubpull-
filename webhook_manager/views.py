import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import GitHubWebhookForm
from .models import PullRequest
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import *
from django.utils import timezone

def setup_webhook(repo_name, token):
    setup_github_webhook(repo_name, token)

def setup_github_webhook(repo_name, token):
    url = f'https://api.github.com/repos/{repo_name}/hooks'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    data = {
        "config": {
            "url": "https://b015-103-203-230-44.ngrok-free.app/webhook/",
            "content_type": "json"
        },
        "events": ["pull_request", "pull_request_review", "pull_request_review_comment"],
        "active": True
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Webhook created successfully.")
    else:
        print(f"Error creating GitHub webhook: {response.text}")

@csrf_exempt
def github_webhook(request):
    if request.method == "POST":
        event_type = request.headers.get('X-GitHub-Event')
        if event_type == "pull_request":
            payload = json.loads(request.body)
            repo_name = payload['repository']['full_name']
            pr_data = payload.get('pull_request', {})
            pr_title = pr_data.get('title')
            pr_url = pr_data.get('html_url')
            try:
                repository = Repository.objects.get(name=repo_name)
            except Repository.DoesNotExist:
                return JsonResponse({'status': 'repository not found'}, status=404)
            pull_request = PullRequest.objects.create(
                title=pr_title,
                url=pr_url,
                repository=repository,
                pull_request_id=pr_data.get('id')
            )
            notify_slack(pull_request, repo_name)
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'status': 'ignored'}, status=200)
    return JsonResponse({'status': 'invalid method'}, status=405)

def notify_slack(pull_request, repo_name):
    try:
        repository = Repository.objects.get(name=repo_name)
    except Repository.DoesNotExist:
        return
    slack_webhooks = repository.slack_webhooks.all()
    if not slack_webhooks.exists():
        return
    message = f"New Pull Request: {pull_request.title} - {pull_request.url}"
    for slack_webhook in slack_webhooks:
        slack_webhook_url = slack_webhook.url
        payload = {'text': message}
        response = requests.post(slack_webhook_url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send notification to Slack: {response.text}")
    pull_request.last_notification_sent = timezone.now()
    pull_request.save()





















