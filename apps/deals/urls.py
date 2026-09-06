from rest_framework.routers import SimpleRouter
from .api_views import DealViewSet


app_name = 'deals'
urlpatterns = []


router = SimpleRouter()
router.register('', DealViewSet)
urlpatterns += router.urls
