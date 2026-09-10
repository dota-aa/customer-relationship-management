from django.db import models
from django.conf import settings

from core.models import BaseModel
from utils.texts import nb


User = settings.AUTH_USER_MODEL


class ActivityLog(BaseModel):
    class ActivityType(models.TextChoices):
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'
        PROFILE_UPDATE = 'profile_update', 'Profile Update'
        PASSWORD_CHANGE_REQUEST = 'password_change_request', 'Password Change Request'
        PASSWORD_CHANGE = 'password_change', 'Password change'
        NOTIFICATION_UPDATE = 'notification_update', 'Notification Settings Update'
        OTHER = 'other', 'Other'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    activity_type = models.CharField(choices=ActivityType.choices, default=ActivityType.OTHER)
    description = models.TextField(**nb)
    ip_address = models.GenericIPAddressField(**nb)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['activity_type'])
        ]
        # ordering = ('-created_at') -> from BaseModel

    def __str__(self):
        return f'{self.user.username} - {self.activity_type} - {self.created_at}'
