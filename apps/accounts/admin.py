from django.contrib import admin
from .models import User, Profile


class ProfileStackInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileStackInline,)
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
