from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Deal
from .serializers import DealSerializer
from core.pagination import StandardPagination


class DealViewSet(ModelViewSet):
    queryset = Deal.objects.select_related('contact', 'created_by').all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        'contact',
        'amount',
        'stage'
    ]

    search_fields = [
        'title',
        'contact__first_name',
        'contact__last_name',
        'note'
    ]

    ordering_fields = [
        'amount',
        'created_at',
        'expected_close_date',
        'closed_date',
    ]

    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

