from pydantic import BaseModel, field_validator, SkipValidation, ConfigDict, computed_field
from rest_framework.request import Request
from django.contrib.auth import get_user_model

from . models import ActivityLog
from utils.request_utils import get_client_ip, get_user_agent


User = get_user_model()


class ActivityLogPayLoad(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    request: SkipValidation[Request] | None = None
    activity_type: ActivityLog.ActivityType
    description: str | None = None

    @computed_field
    @property
    def user(self) -> User:
        if self.request and getattr(self.request, 'user') and self.request.user.is_authenticated:
            return self.request.user
        return None

    @computed_field
    @property
    def user_agent(self) -> str | None:
        return get_user_agent(self.request) if self.request else None

    @computed_field
    @property
    def ip_address(self) -> str | None:
        return get_client_ip(self.request) if self.request else None


def log_activity(payload: ActivityLogPayLoad):
    log = ActivityLog.objects.create(
        user=payload.user,
        activity_type=payload.activity_type.value,
        description=payload.description,
        user_agent=payload.user_agent,
        ip_address=payload.ip_address,
    )
    return log
