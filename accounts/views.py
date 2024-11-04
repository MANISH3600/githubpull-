from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SlackWebhookForm
from .models import SlackWebhook, UserProfile, Repository
import re
from webhook_manager.views import * 
from urllib.parse import urlparse
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
                user_profile=UserProfile.objects.get(user=request.user)  
            )
            slack_webhooks.save()  


            repo_url = form.cleaned_data['repository_url'] 
             # Assuming you provide a GitHub URL here
            print("the repo url is :" + repo_url)

            repofullname = extract_repo_name(repo_url)


            # Create the Repository object
            repository = Repository.objects.create(
                name=repofullname,
                github_url=repo_url,
            )

            # Link the created SlackWebhook to the Repository
            repository.slack_webhooks.add(slack_webhooks)
            print("the repo name and url is "+repository.name,repository.github_url)

            setup_webhook(repo_name= repofullname,token = slack_webhooks.github_token)
            print("the setup waws done ")
            print("the repo full name is "+ repofullname)

            return render(request, 'accounts/success.html') 
    else:
        form = SlackWebhookForm()

    return render(request, 'accounts/add_slack_webhook.html', {'form': form})  


from urllib.parse import urlparse

def extract_repo_name(url):


    parsed_url = urlparse(url)

    path_parts = parsed_url.path.strip('/').split('/')
    

    if len(path_parts) >= 2:
        owner = path_parts[-2]  
        repo_name = path_parts[-1] 
        owner_repo_name = f"{owner}/{repo_name}"  
        print(owner_repo_name)
        return  owner_repo_name  


