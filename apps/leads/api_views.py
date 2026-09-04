from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import LeadSerializer
from .models import Lead
from core.pagination import StandardPagination


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        serializer.save()
        # TODO: add Notification

    def perform_update(self, serializer):
        serializer.save()
        # TODO: add Notification

    def perform_destroy(self, instance):
        instance.delete()
        # TODO: add Notification
