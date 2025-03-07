from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username


class SlackWebhook(models.Model):

    url = models.URLField(unique=True)  
    github_token = models.CharField(max_length=255) 
    notification_days = models.PositiveIntegerField(default=7)  
    user_profile = models.ForeignKey(UserProfile, related_name='slack_webhooks', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.url} - User: {self.user_profile.user.username}"


class Repository(models.Model):
    """Model to store GitHub repositories and link to multiple Slack webhooks."""
    name = models.CharField(max_length=255)
    github_url = models.URLField(unique=True) 
    slack_webhooks = models.ManyToManyField(SlackWebhook, related_name='repositories', blank=True)

    def __str__(self):
        return self.name


class PullRequest(models.Model):
    """Model to store pull requests and associate them with a repository."""
    title = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    last_notification_sent = models.DateTimeField(null=True, blank=True)  
    repository = models.ForeignKey(Repository, related_name='pull_requests', on_delete=models.CASCADE)
    pull_request_id = models.IntegerField(unique=True)  

    def __str__(self):
        return f"{self.title} (ID: {self.pull_request_id})"
