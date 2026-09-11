from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ActivityLog
from apps.notifications.services import set_notification, NotificationPayLoad


@receiver(post_save, sender=ActivityLog)
def set_notification_for_log(sender, instance, created, **kwargs):
    if created and instance.user:
        payload = NotificationPayLoad(
            user_id=instance.user.id,
            title=f'{instance.get_activity_type_display()}',
            message=f'{instance.description}',
            type='activity',
            source_type=f'{instance.__class__}',
            source_id=instance.id,
        )
        set_notification(payload)
