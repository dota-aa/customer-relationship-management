from django.urls import path
from . import api_views


app_name = 'dashboard'
urlpatterns = [
    path('activities/', api_views.ActivityLogListView.as_view())
]
