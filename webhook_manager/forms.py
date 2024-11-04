# webhook_manager/forms.py
from django import forms

class GitHubWebhookForm(forms.Form):
    github_token = forms.CharField(widget=forms.PasswordInput)
    repository_name = forms.CharField(max_length=100)
