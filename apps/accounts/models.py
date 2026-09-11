from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import file_upload_path
from utils.texts import nb


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=128, **nb)
    bio = models.CharField(max_length=256, **nb)
    job = models.CharField(max_length=32, **nb)
    avatar = models.ImageField(upload_to=file_upload_path, **nb)
    birth_date = models.DateField(**nb)

    def __str__(self):
        return f'{self.full_name}'
