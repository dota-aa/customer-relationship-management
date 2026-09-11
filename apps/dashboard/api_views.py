import csv
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

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


class ActivityLogExportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qs = ActivityLog.objects.filter(user=request.user).order_by('-created_at')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="activity_log.csv"'
        writer = csv.writer(response)
        writer.writerow(['activity_type', 'description', 'user_agent', 'ip_address'])
        for log in qs:
            writer.writerow([
                log.activity_type, log.description,
                log.user_agent, log.ip_address
            ])
        return response
