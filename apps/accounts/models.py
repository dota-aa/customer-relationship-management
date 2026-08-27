from django.db import models
from django.contrib.auth.models import AbstractUser

from utils import nb


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=128, **nb)
    bio = models.CharField(max_length=256, **nb)
    job = models.CharField(max_length=32, **nb)
    avatar = models.ImageField(upload_to='users/avatar', **nb)
    birth_date = models.DateField(**nb)
