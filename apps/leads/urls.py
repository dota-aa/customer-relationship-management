from rest_framework.routers import SimpleRouter

from . import api_views

app_name = 'leads'
urlpatterns = []


router = SimpleRouter()
router.register('', api_views.LeadViewSet)
urlpatterns += router.urls
