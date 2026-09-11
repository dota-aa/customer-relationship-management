from django.urls import path
from . import api_views


app_name = 'dashboard'
urlpatterns = [
    path('', api_views.ActivityLogListView.as_view()),
    path('export/', api_views.ActivityLogExportView.as_view())
]
