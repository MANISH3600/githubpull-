from django.contrib import admin
from .models import PullRequest

class PullRequestAdmin(admin.ModelAdmin):

    list_display = ('title', 'url', 'last_notification_sent','created_at')
    

    list_filter = ('last_notification_sent','created_at')  
    search_fields = ('title',)


admin.site.register(PullRequest, PullRequestAdmin)
