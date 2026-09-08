from django.db import models
from django.conf import settings

from core.models import BaseModel
from utils.texts import nb


User = settings.AUTH_USER_MODEL


class NoteCategory(BaseModel):
    name = models.CharField(max_length=128)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='note_categories', null=True)

    class Meta:
        verbose_name = 'Note Category'
        verbose_name_plural = 'Note Categories'

    def __str__(self):
        return self.name


class Note(BaseModel):
    class NotePriority(models.TextChoices):
        LOW = 'low', 'Low priority'
        MEDIUM = 'medium', 'Medium priority'
        HIGH = 'high', 'High priority'

    title = models.CharField(max_length=128)
    content = models.TextField(**nb)
    category = models.ForeignKey(NoteCategory, on_delete=models.SET_NULL, related_name='category_notes', null=True)
    priority = models.CharField(choices=NotePriority, default=NotePriority.MEDIUM)

    tags = models.JSONField(default=list, **nb)

    pinned = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    # can use content type here too
    lead = models.ForeignKey(
        'leads.Lead',
        on_delete=models.CASCADE,
        related_name='lead_notes',
        **nb
    )

    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.CASCADE,
        related_name='contact_notes',
        **nb
    )

    deal = models.ForeignKey(
        'deals.Deal',
        on_delete=models.CASCADE,
        related_name='deal_notes',
        **nb
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='notes',
        null=True
    )

    class Meta:
        ordering = ('-pinned', '-created_at')  # baseModel -> ('-created',)

    def __str__(self):
        return self.title
