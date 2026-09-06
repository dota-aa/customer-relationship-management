from .models import Lead
from apps.contacts.services import create_contact_from_lead


def check_lead_status(*, lead, user) -> None:
    """
    make a contact for converted leads
    """
    if lead.status == 'converted':
        create_contact_from_lead(lead=lead, user=user)
