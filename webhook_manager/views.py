

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


from django.contrib.auth.decorators import login_required


from accounts.models import *

from django.utils import timezone



def setup_webhook(repo_name, token):
    

    setup_github_webhook(repo_name, token)
    print("the setup function ran ")

def setup_github_webhook(repo_name, token):
    print("the setup_github_webhook function ran")
    url = f'https://api.github.com/repos/{repo_name}/hooks'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }


    data = {
        "config": {
            "url": "https://d522-103-203-231-10.ngrok-free.app/webhook",
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
    print("The request came")
    if request.method == "POST":
        event_type = request.headers.get('X-GitHub-Event')

        if event_type == "pull_request":
            payload = json.loads(request.body)
            repo_name = payload['repository']['full_name']
            pr_data = payload.get('pull_request', {})
            pr_title = pr_data.get('title')
            pr_url = pr_data.get('html_url')
            pr_id = pr_data.get('id')
            action = payload.get("action")
            merged = pr_data.get("merged", False)

            try:
                repository = Repository.objects.get(name=repo_name)
            except Repository.DoesNotExist:
                print(f"Repository '{repo_name}' does not exist.")
                return JsonResponse({'status': 'repository not found'}, status=404)

            if action == "closed" and merged:
                try:
                    pr = PullRequest.objects.get(pull_request_id=pr_id)
                    print(f"✅ Pull request '{pr_title}' with ID {pr_id} in repository '{repo_name}' has been merged.")
                    pr.delete()
                    return JsonResponse({"status": "success", "message": f"Pull request {pr_id} merged and deleted."}, status=200)
                except PullRequest.DoesNotExist:
                    print(f"Pull request with ID {pr_id} not found in the database.")
                    return JsonResponse({"error": "Pull request not found."}, status=404)

            elif action == "closed" and not merged:
                try:
                    pr = PullRequest.objects.get(pull_request_id=pr_id)
                    print(f"🚫 Pull request '{pr_title}' with ID {pr_id} in repository '{repo_name}' has been closed.")
                    pr.delete()
                    return JsonResponse({"status": "success", "message": f"Pull request {pr_id} closed and deleted."}, status=200)
                except PullRequest.DoesNotExist:
                    print(f"Pull request with ID {pr_id} not found in the database.")
                    return JsonResponse({"error": "Pull request not found."}, status=404)

            elif action == "opened":
                pull_request = PullRequest.objects.create(
                    title=pr_title,
                    url=pr_url,
                    repository=repository,
                    pull_request_id=pr_id
                )
                print("The pull request is saved.")
                notify_slack(pull_request, repo_name)
                return JsonResponse({'status': 'success', 'message': 'Pull request opened and saved.'}, status=200)

        return JsonResponse({'status': 'ignored'}, status=200)

    return JsonResponse({'status': 'invalid method'}, status=405)

def notify_slack(pull_request, repo_name):
    try:
        repository = Repository.objects.get(name=repo_name)
    except Repository.DoesNotExist:
        print(f"No repository found with name: {repo_name}")
        return

    slack_webhooks = repository.slack_webhooks.all()
    if not slack_webhooks.exists():
        print(f"No SlackWebhook found for repository {repo_name}")
        return

    message = f"New Pull Request: {pull_request.title} - {pull_request.url}"

    for slack_webhook in slack_webhooks:
        payload = {'text': message}
        response = requests.post(slack_webhook.url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send notification to Slack: {response.text}")

    pull_request.last_notification_sent = timezone.now()
    pull_request.save()









































