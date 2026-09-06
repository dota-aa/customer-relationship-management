from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel
from utils.texts import nb


User = get_user_model()


class Contact(BaseModel):
    class ContactStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        LEAD = 'lead', 'Lead'

    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225, **nb)
    company = models.CharField(max_length=225, **nb)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, **nb)
    job_title = models.CharField(max_length=128, **nb)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='contacts')

    status = models.CharField(
        choices=ContactStatus,
        default=ContactStatus.LEAD,
    )
    last_interaction = models.DateTimeField(**nb)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
