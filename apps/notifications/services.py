from pydantic import BaseModel, Field, UUID4, field_validator
from django.contrib.auth import get_user_model

from .models import Notification, NotificationSettings
from apps.mailing.services import EmailPayload, send_email


User = get_user_model()


class NotificationPayLoad(BaseModel):
    user_id: int
    title: str = Field(max_length=32)
    message: str = Field(max_length=64)
    type: Notification.NotificationType
    source_id: UUID4 | None = None
    source_type: str | None = None

    @field_validator('user_id')
    @classmethod
    def check_user(cls, v: int) -> int:
        if not User.objects.filter(id=v).exists():
            raise ValueError('user not found')
        return v


def set_notification(payload: NotificationPayLoad):
    user = User.objects.get(id=payload.user_id)
    settings, _ = NotificationSettings.objects.get_or_create(user=user)

    if not settings.push_notification:
        """
        User doesn't want notification.
        """
        return None

    if settings.email_notification:
        """
        Send Email to user
        """
        email_payload = EmailPayload(
            subject=payload.title,
            body=payload.message,
            template_name='mailing/notification_email.html',
            context={
                'title': payload.title,
                'notification': payload.message,
                'notification_type': payload.type.value
            },
            receivers=[user.email],
        )
        send_email(email_payload)

    if not getattr(settings, payload.type.value, True):
        """
        check if user wants these type of notification
        """
        return None

    notification = Notification.objects.create(
        user=user,
        title=payload.title,
        message=payload.message,
        type=payload.type.value,
        source_type=payload.source_type,
        source_id=payload.source_id,
    )
    return notification
