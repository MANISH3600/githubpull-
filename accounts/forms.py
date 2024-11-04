from django import forms
from .models import SlackWebhook

class SlackWebhookForm(forms.ModelForm):
    """Form to capture Slack webhook information along with GitHub details."""
    repository_url = forms.URLField(label='GitHub Repository URL', required=True)
    github_token = forms.CharField(label='GitHub Token', max_length=255, required=True, widget=forms.PasswordInput)
    slack_url = forms.URLField(label='Slack Webhook URL', required=True)
    notification_days = forms.IntegerField(label='Notification Days', required=True, min_value=1)

    class Meta:
        model = SlackWebhook
        fields = ['repository_url', 'github_token', 'slack_url', 'notification_days']

    def clean(self):
        cleaned_data = super().clean()
        # You can perform additional validation here if necessary
        return cleaned_data
