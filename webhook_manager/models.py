# webhook_manager/models.py
from django.db import models
from django.utils import timezone

class PullRequest(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_notification_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def should_send_notification(self):
        """Check if a notification should be sent based on the last sent time."""
        if not self.last_notification_sent:
            return True
        return timezone.now() >= self.last_notification_sent + timezone.timedelta(days=7)
