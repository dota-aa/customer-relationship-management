from .models import Contact


def create_contact_from_lead(*, lead, user) -> Contact:
    contact = Contact.objects.create(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        created_by=user,
        phone_number=lead.phone_number or None,
        company=lead.company or None,
    )
    return contact
