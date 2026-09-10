from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Contact
from .serializers import ContactSerializer
from core.pagination import StandardPagination
from apps.notifications.services import NotificationPayLoad, set_notification


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.select_related('created_by').all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        contact = serializer.save(created_by=self.request.user)
        payload = NotificationPayLoad(
            user_id=self.request.user.id,
            title='New Contact',
            message=f'a new contact has been added.',
            type='new_contact',
            source_type=f'{contact.__class__}',
            source_id=contact.id,
        )
        set_notification(payload)

    def perform_update(self, serializer):
        serializer.save()
        # TODO: add Notification if needed

    def perform_destroy(self, instance):
        instance.delete()
        # TODO: add Notification if needed
