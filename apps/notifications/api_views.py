"""

    All these views are for test. the best option is to use
    ReadOnlyModelViewSet and actions for implementing notification endpoints.

"""

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend

from .models import Notification, NotificationSettings
from .serializers import NotificationSerializer, NotificationSettingsSerializer
from core.pagination import MediumPagination
from apps.dashboard.services import log_activity, ActivityLogPayLoad

class NotificationListView(APIView):
    """
    Show all user's notification

    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_num = self.request.query_params.get('page_num', 1)
        page_size = self.request.query_params.get('limit', 10)
        qs = Notification.objects.filter(user=request.user)

        paginator = Paginator(qs, page_size)

        serializer = NotificationSerializer(instance=paginator.page(page_num), many=True)
        return Response(data=serializer.data)


class NotificationUnReadListView(APIView):
    """
    Show all user's unread notification

    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_num = self.request.query_params.get('page_num', 1)
        page_size = self.request.query_params.get('limit', 10)
        qs = Notification.objects.filter(user=request.user, is_read=False)

        paginator = Paginator(qs, page_size)

        serializer = NotificationSerializer(instance=paginator.page(page_num), many=True)
        return Response(data=serializer.data)


class NotificationMarkReadView(APIView):
    """
        Mark a single notification as read for the authenticated user.

    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
        except Notification.DoesNotExist:
            return Response({"message": "notification not found"}, status=status.HTTP_400_BAD_REQUEST)

        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({"message": "notification successfully marked as READ"})


class NotificationMarkAllReadView(APIView):
    """
    Mark all notifications as read for the authenticated user.

    """
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        Notification.objects.filter(user=request.user).update(is_read=True)
        return Response({"message": "All notifications marked as READ"})


# -------------------------------------------------------------
# --Use GenericViewSet for implementing same purpose view--
# -------------------------------------------------------------
class NotificationGenericViewSet(GenericViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MediumPagination
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = ['is_read', 'type']

    search_fields = ['title', 'message']

    ordering_fields = ['created_at', 'is_read']

    ordering = ['-created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def list(self, request):
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)
        if page is not None:  # page is always not None
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------------------------------------------------
# -- Best Practice --
# -------------------------------------------------------------
class NotificationReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MediumPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = ['is_read', 'type']

    search_fields = ['title', 'message']

    ordering_fields = ['is_read', 'created_at']

    ordering = ['-created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(methods=['patch'], detail=True, url_path='read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()  # check if a notification with this pk and user exists or not.
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({"message": "notification successfully marked as READ"})

    @action(methods=['patch'], detail=False, url_path='mark-all-read')
    def mark_all_read(self, request):
        count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({"message": f"{count} notifications marked as READ"})

    @action(methods=['get'], detail=False, url_path='options')
    def get_options(self, request):
        data = {

            "notification_type": [
                {
                    "value": value,
                    "label": label,
                }
                for value, label in Notification.NotificationType.choices
            ],
            "statuses": {
                "read": [
                    {
                        "value": "True",
                        "label": 'Read'
                    },
                    {
                        "value": "False",
                        "label": 'Not Read'
                    }
                ],
            },

        }
        return Response(data)


# -------------------------------------------------------------
# -- notification settings --
# -------------------------------------------------------------
class NotificationSettingsRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        settings, _ = NotificationSettings.objects.get_or_create(user=self.request.user)
        return settings

    def update(self, request, *args, **kwargs):

        payload = ActivityLogPayLoad(
            request=request,
            activity_type='notification_update',
            description='You updated your notification settings',
        )
        log_activity(payload)

        return super().update(request, *args, **kwargs)
