from django.db import models
from django.conf import settings
from core.models import BaseModel


User = settings.AUTH_USER_MODEL


class Notification(BaseModel):
    class NotificationType(models.TextChoices):
        NEW_LEAD = 'new_lead', 'New Lead'
        NEW_CONTACT = 'new_contact', 'New Contact'
        NEW_CUSTOMER = 'new_customer', 'New Customer'
        NEW_DEAL = 'new_deal', 'New Deal'
        DEAL_WON = 'deal_won', 'Deal Won'
        DEAL_LOST = 'deal_lost', 'Deal Lost'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField()
    message = models.CharField()

    type = models.CharField(choices=NotificationType.choices)

    is_read = models.BooleanField(default=False)

    # content type
    source_type = models.CharField()  # model name
    source_id = models.UUIDField()  # object it

    def __str__(self):
        return f'{self.title}-{self.message}'


class NotificationSettings(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')

    email_notification = models.BooleanField(default=True)
    push_notification = models.BooleanField(default=True)

    lead_update = models.BooleanField(default=True)
    contact_update = models.BooleanField(default=True)
    customer_update = models.BooleanField(default=True)
    deal_update = models.BooleanField(default=True)
    activity_update = models.BooleanField(default=True)

    def __str__(self):
        return f'Notification settings: {self.user.username}'
