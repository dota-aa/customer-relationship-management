from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    """
    all crm models inherit from BaseModel
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-created',)
