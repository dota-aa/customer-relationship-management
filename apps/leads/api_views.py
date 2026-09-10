from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from .serializers import LeadSerializer
from .models import Lead
from .services import check_lead_status
from core.pagination import StandardPagination
from apps.notifications.services import NotificationPayLoad, set_notification


class LeadViewSet(ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        lead = serializer.save()
        check_lead_status(lead=lead, user=self.request.user)
        payload = NotificationPayLoad(
            user_id=self.request.user.id,
            title='New Lead',
            message=f'a new lead has been added.',
            type='new_lead',
            source_type=f'{lead.__class__}',
            source_id=lead.id,
        )
        set_notification(payload)
