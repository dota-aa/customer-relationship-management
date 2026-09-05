from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Contact
from .serializers import ContactSerializer
from core.pagination import StandardPagination


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.select_related('created_by').all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        # TODO: add Notification

    def perform_update(self, serializer):
        serializer.save()
        # TODO: add Notification

    def perform_destroy(self, instance):
        instance.delete()
        # TODO: add Notification
