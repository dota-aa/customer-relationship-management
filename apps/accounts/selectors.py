from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

from apps.accounts.models import Profile


User = get_user_model()


def get_users():
    return User.objects.all()


def get_user_by_email(*, email: str) -> User | None:
    """
    Retrieve a user by their email.
    Returns None if no user matches.
    """
    if not email:
        return None

    try:
        return User.objects.get(email=email.strip())
    except User.DoesNotExist:
        return None


def get_user_by_uidb64(*, uidb64) -> User:
    uid = urlsafe_base64_decode(uidb64).decode()
    return User.objects.get(id=uid)


# --------------------
# --profile--
# ====================
def get_profile_for_update(*, user: User) -> Profile:
    """
       Acquires a row-level DB lock on the user's profile.
       Must be executed inside transaction.atomic().
    """
    return Profile.objects.select_for_update().select_related('user').get(user=user)
