

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
            "url": "https://d522-103-203-231-10.ngrok-free.app/webhook/",
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











































# import json
# import requests
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from .forms import GitHubWebhookForm
# from .models import PullRequest
# import json
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt




# def setup_webhook(request):
#     if request.method == 'POST':
#         form = GitHubWebhookForm(request.POST)
#         if form.is_valid():
#             token = form.cleaned_data['github_token']
#             repo_name = form.cleaned_data['repository_name']

#             setup_github_webhook(repo_name, token)
#             return render(request, 'webhook_manager/success.html') 
#     else:
#         form = GitHubWebhookForm()
#     return render(request, 'webhook_manager/setup_webhook.html', {'form': form})
# def setup_github_webhook(repo_name, token):
#     url = f'https://api.github.com/repos/{repo_name}/hooks'
#     headers = {
#         'Authorization': f'token {token}',
#         'Accept': 'application/vnd.github.v3+json',

#     }

#     data = {
#         "config": {
#             "url": "https://b015-103-203-230-44.ngrok-free.app/webhook/",  
#             "content_type": "json"
#         },
#         "events": ["pull_request"],
#         "active": True
#     }
#     response = requests.post(url, json=data, headers=headers)
#     if response.status_code == 201:
#         print("Webhook created successfully.")
#     else:
#         print(f"Error creating GitHub webhook: {response.text}")



# @csrf_exempt
# def github_webhook(request):
#     print("The request came")
#     if request.method == "POST":
#         print("The request came ")
#         event_type = request.headers.get('X-GitHub-Event')

#         if event_type == "pull_request":
#             print("The event is a pull request")

#             payload = json.loads(request.body)
#             print(request.body)
#             repo_name = payload['repository']['full_name']
#             print("The repo name is " + repo_name)
#             pr_data = payload.get('pull_request', {})
#             print( pr_data)
#             pr_title = pr_data.get('title')
#             print("the pull request title is" + pr_title)
#             pr_url = pr_data.get('html_url')
#             print("the pull request url is" +pr_url)


#             pull_request = PullRequest.objects.create(
#                 title=pr_title,
#                 url=pr_url,
#             )
#             print("The post is saved")


#             notify_slack(pull_request)


#             open_prs = get_open_pull_requests(repo_name)
#             if open_prs:
#                 notify_slack_of_open_prs(open_prs)

#             return JsonResponse({'status': 'success'}, status=200)

#         return JsonResponse({'status': 'ignored'}, status=200)

#     return JsonResponse({'status': 'invalid method'}, status=405)

# def get_open_pull_requests(repo_name):

#     token = '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'  
#     url = f'https://api.github.com/repos/{repo_name}/pulls?state=open'
#     headers = {
#         'Authorization': f'token {token}',
#         'Accept': 'application/vnd.github.v3+json',
#     }

#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.json()  #
#     else:
#         print(f"Failed to fetch open pull requests: {response.text}")
#         return []

# def notify_slack_of_open_prs(open_prs):
#     slack_webhook_url = 'https://hooks.slack.com/services/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'  
#     message = "Open Pull Requests:\n"

#     for pr in open_prs:
#         pr_title = pr.get('title')
#         pr_url = pr.get('html_url')
#         pr_created_at = pr.get('created_at')
#         message += f"- {pr_title} ({pr_url}) created at {pr_created_at}\n"

#     payload = {'text': message}
#     response = requests.post(slack_webhook_url, json=payload)
#     if response.status_code != 200:
#         print(f"Failed to send notification to Slack: {response.text}")


# def notify_slack(pull_request):
#     slack_webhook_url = 'https://hooks.slack.com/services/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' 
#     message = f"New Pull Request: {pull_request.title} - {pull_request.url}"

#     payload = {'text': message}
#     response = requests.post(slack_webhook_url, json=payload)
#     if response.status_code != 200:
#         print(f"Failed to send notification to Slack: {response.text}")
# # 