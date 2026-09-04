from django.db import models

from core.models import BaseModel
from utils.texts import nb


class Lead(BaseModel):
    class LeadSource(models.TextChoices):
        WEBSITE = 'website', 'Website'
        REFERRAL = 'referral', 'Referral'
        SOCIAL = 'social', 'Social Media'
        EMAIL = 'email', 'Email'
        OTHER = 'other', 'Other'

    class LeadStatus(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In Progress'
        QUALIFIED = 'qualified', 'Qualified'
        CONVERTED = 'converted', 'Converted'
        LOST = 'lost', 'Lost'
        JUNK = 'junk', 'Junk / Spam'

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True, **nb)
    phone_number = models.CharField(max_length=11, **nb)
    company = models.CharField(max_length=64, **nb)

    source = models.CharField(
        choices=LeadSource,
        default=LeadSource.WEBSITE,
    )

    status = models.CharField(
        choices=LeadStatus,
        default=LeadStatus.NEW,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
