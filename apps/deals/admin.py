from django.contrib import admin
from .models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact', 'amount', 'stage', 'created_by')
    readonly_fields = ('id', 'updated_at', 'created_at')
