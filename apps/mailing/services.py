from typing import Dict, Any
from pydantic import BaseModel, EmailStr, field_validator, Field
from django.template import loader, TemplateDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone


class EmailPayload(BaseModel):
    subject: str
    body: str
    template_name: str
    context: Dict[str, Any] | None = None
    receivers: list[EmailStr] = Field(min_length=1, max_length=100)

    @field_validator('template_name')
    @classmethod
    def check_template(cls, v: str) -> str:
        try:
            loader.get_template(template_name=v)
        except TemplateDoesNotExist:
            raise ValueError('template path does not exist')
        return v


def send_email(payload: EmailPayload) -> None:
    html_content = loader.render_to_string(payload.template_name, context=payload.context)
    timestamp = timezone.now().strftime("%b %d, %H:%M:%S")
    email = EmailMultiAlternatives(
        subject=f'{payload.subject} - {timestamp}',
        body=payload.body,
        from_email=f'crm <{settings.HOST_USER}>',
        to=payload.receivers,
    )
    email.attach_alternative(content=html_content, mimetype='text/html')
    email.send()
