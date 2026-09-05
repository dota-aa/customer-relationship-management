from django.urls import path
from rest_framework.routers import SimpleRouter

from . import api_views


app_name = 'contacts'
urlpatterns = []


router = SimpleRouter()
router.register('', api_views.ContactViewSet)
urlpatterns += router.urls
