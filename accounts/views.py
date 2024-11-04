from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SlackWebhookForm
from .models import SlackWebhook, UserProfile, Repository
import re

@login_required  # Ensure that the user is logged in
def add_slack_webhook(request):
    """View to handle Slack webhook form submission."""
    if request.method == 'POST':
        form = SlackWebhookForm(request.POST)
        if form.is_valid():
            # Create the SlackWebhook object
            slack_webhooks = SlackWebhook(
                url=form.cleaned_data['slack_url'],
                github_token=form.cleaned_data['github_token'],
                notification_days=form.cleaned_data['notification_days'],
                user_profile=UserProfile.objects.get(user=request.user)  # Set the current user
            )
            slack_webhooks.save()  # Save the form data to the database

            # Extract repository name from the GitHub token (or URL)
            repo_url = form.cleaned_data['repository_url']  # Assuming you provide a GitHub URL here
            print("the repo url is :" + repo_url)
            repo_name = extract_repo_name(repo_url)
            print("the repo name is :" + repo_name)

            # Create the Repository object
            repository = Repository.objects.create(
                name=repo_name,
                github_url=repo_url,
            )

            # Link the created SlackWebhook to the Repository
            repository.slack_webhooks.add(slack_webhooks)
            print("the repo name and url is "+repository.name,repository.github_url)

            # Optionally link the repository to the slack_webhook if needed
            # repository.slack_webhooks.add(slack_webhook)

            return render(request, 'accounts/success.html')  # Render success template
    else:
        form = SlackWebhookForm()

    return render(request, 'accounts/add_slack_webhook.html', {'form': form})  # Render the form template
from urllib.parse import urlparse

def extract_repo_name(url):
    """Extract the repository name from the GitHub URL."""
    # Parse the URL
    parsed_url = urlparse(url)
    # Split the path and get the last part as the repository name
    path_parts = parsed_url.path.strip('/').split('/')
    return path_parts[-1] if len(path_parts) > 1 else None

# Example usage
github_url = "https://github.com/MANISH3600/Rating-and-Review-Api"
repo_name = extract_repo_name(github_url)