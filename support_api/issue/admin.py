from django.contrib import admin
from issue.models import Issue, Comments


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'status', 'title', 'time_created')
    search_fields = ('created_by', 'title')
    list_filter = ('time_created', "time_updated", "status")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('issue_id', 'issue', 'created_by', 'time_created')


admin.site.register(Issue, IssueAdmin)
admin.site.register(Comments, CommentsAdmin)

