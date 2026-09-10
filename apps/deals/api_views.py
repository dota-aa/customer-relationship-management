from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Deal
from .serializers import DealSerializer
from core.pagination import StandardPagination
from apps.notifications.services import NotificationPayLoad, set_notification


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
        deal = serializer.save(created_by=self.request.user)
        payload = NotificationPayLoad(
            user_id=self.request.user.id,
            title='New Deal',
            message=f'a new deal has been added.',
            type='new_deal',
            source_type=f'{deal.__class__}',
            source_id=deal.id,
        )
        set_notification(payload)

    def perform_update(self, serializer):
        deal = serializer.save()
        if deal.stage == 'deal_won':
            payload = NotificationPayLoad(
                user_id=self.request.user.id,
                title='Deal Won',
                message=f'You won the DEAL.',
                type='deal_won',
                source_type=f'{deal.__class__}',
                source_id=deal.id,
            )
            set_notification(payload)

        elif deal.stage == 'deal_lost':
            payload = NotificationPayLoad(
                user_id=self.request.user.id,
                title='Deal Lost',
                message=f'You Lost the DEAL.',
                type='lost_deal',
                source_type=f'{deal.__class__}',
                source_id=deal.id,
            )
            set_notification(payload)
