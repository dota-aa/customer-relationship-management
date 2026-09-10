from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'activity_type', 'ip_address', 'created_at')
    readonly_fields = ('id', 'created_at')
