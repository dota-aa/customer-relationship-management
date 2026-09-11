from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed

from .models import User, Profile
from apps.dashboard.services import log_activity, ActivityLogPayLoad


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Create profile for new users
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    """
    Create a Log activity record for every time user logs in.
    """
    payload = ActivityLogPayLoad(
        request=request,
        activity_type='login',
        description='You logged in',
    )
    log_activity(payload)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    identifier = credentials.get('username')
    payload = ActivityLogPayLoad(
        request=request,
        activity_type='login_failed',
        description=f'Anonymous user tried to logged in by username: {identifier}',
    )
    log_activity(payload)
