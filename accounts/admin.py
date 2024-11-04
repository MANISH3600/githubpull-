from django.contrib import admin
from .models import UserProfile, SlackWebhook, Repository, PullRequest

# Register the UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display the user field in the admin
    search_fields = ('user__username',)  # Enable searching by username


# Register the SlackWebhook model
@admin.register(SlackWebhook)
class SlackWebhookAdmin(admin.ModelAdmin):
    list_display = ('url', 'github_token', 'notification_days', 'user_profile')  # Display relevant fields
    search_fields = ('url', 'user_profile__user__username')  # Enable searching by URL and associated username
    list_filter = ('notification_days',)  # Filter by notification days


# Register the Repository model
@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'github_url')  # Display the name and GitHub URL
    search_fields = ('name', 'github_url')  # Enable searching by name and GitHub URL
    filter_horizontal = ('slack_webhooks',)  # Use horizontal filter for many-to-many field


# Register the PullRequest model
@admin.register(PullRequest)
class PullRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at', 'repository', 'pull_request_id')  # Display relevant fields
    search_fields = ('title', 'repository__name', 'pull_request_id')  # Enable searching by title, repository name, and ID
    list_filter = ('repository', 'created_at')  # Filter by repository and creation date

