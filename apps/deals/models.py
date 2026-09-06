from django.db import models
from django.conf import settings

from core.models import BaseModel
from utils.texts import nb


User = settings.AUTH_USER_MODEL


class Deal(BaseModel):
    class LeadStage(models.TextChoices):
        LEAD = "lead", "Lead"
        QUALIFIED = "qualified", "Qualified"
        PROPOSAL = "proposal", "Proposal"
        NEGOTIATION = "negotiation", "Negotiation"
        CLOSED_WON = "closed_won", "Closed Won"
        CLOSED_LOST = "closed_lost", "Closed Lost"

    title = models.CharField(max_length=128)
    contact = models.ForeignKey('contacts.contact', on_delete=models.SET_NULL, related_name='contact_deals', null=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, **nb)
    stage = models.CharField(choices=LeadStage, default=LeadStage.LEAD)
    expected_close_date = models.DateTimeField(**nb)
    closed_date = models.DateTimeField(**nb)
    probability = models.PositiveIntegerField(default=50)
    notes = models.TextField(**nb)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='deals', null=True)

    def __str__(self):
        return f'{self.title}'
