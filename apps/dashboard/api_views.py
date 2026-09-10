from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import ActivityLog
from .serializers import ActivityLogSerializer
from core.pagination import MediumPagination


class ActivityLogListView(ListAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    pagination_class = MediumPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    fieldset_filters = ['activity_type']
    ordering_fields = ['created_at', '']

    ordering = ['-created_at']

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs
