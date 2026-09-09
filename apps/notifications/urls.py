from django.urls import path
from rest_framework.routers import SimpleRouter
from . import api_views


app_name = 'notifications'
urlpatterns = [
    # path('notifications/', api_views.NotificationListView.as_view()),
    # path('notifications/unread-list/', api_views.NotificationUnReadListView.as_view()),
    # path('notifications/mark-all-read/', api_views.NotificationMarkAllReadView.as_view()),
    # path('notifications/<uuid:notification_id>/read/', api_views.NotificationMarkReadView.as_view()),
    path('notification-settings/', api_views.NotificationSettingsRetrieveUpdateView.as_view()),
]


router = SimpleRouter()
router.register('notifications', api_views.NotificationReadOnlyViewSet)
urlpatterns += router.urls
