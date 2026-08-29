from dataclasses import dataclass
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from apps.mailing.services import EmailPayload, send_email


User = get_user_model()

# -----------------------------------------------------------------------
# change user data in db
def create_user(*, username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    activation_link = _build_activation_link(user=user)
    payload = EmailPayload(
        subject=f'Verify your account {user.id}',
        body=f'Your activation link: {activation_link}',
        template_name='mailing/activation_email.html',
        context={
            'user': user,
            'activation_link': activation_link
        },
        receivers=[email],
    )
    send_email(payload)
    return user


def change_user_password(*, user: User, password: str) -> User:
    user.set_password(raw_password=password)
    user.save(update_fields=['password'])
    return user


def activate_user_account(*, user: User) -> User:
    user.is_active = True
    user.save(update_fields=['is_active'])
    return user


def deactivate_user_account(*, user: User) -> User:
    user.is_active = False
    user.save(update_fields=['is_active'])
    return user


# -----------------------------------------------------------------------
# Link

def _build_activation_link(*, user: User) -> str:
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user=user)
    return f'https://127.0.0.1:8000/api/auth/activate/{uidb64}/{token}/'  # change to frontend url


def _build_rest_password_link(*, user: User) -> str:
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user=user)
    return f'https://127.0.0.1:8000/api/auth/reset-password/verify/{uidb64}/{token}/'


def send_reset_password_email(*, user: User) -> User:
    reset_password_link = _build_rest_password_link(user=user)
    payload = EmailPayload(
        subject='Reset Password request',
        body=f'Your reset password link: {reset_password_link}',
        template_name='mailing/reset_password_email.html',
        context={
            'user': user,
            'reset_password_link': reset_password_link
        },
        receivers=[user.email],
    )
    send_email(payload)
    return user


@dataclass(slots=True, frozen=True)
class TokenValidationResult:
    is_valid: bool
    user: User | None = None


def validate_user_token(*, uidb64, token) -> TokenValidationResult:
    uid = urlsafe_base64_decode(uidb64).decode()
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return TokenValidationResult(user=None, is_valid=False)
    is_valid = default_token_generator.check_token(user=user, token=token)
    return TokenValidationResult(user=user, is_valid=is_valid)
