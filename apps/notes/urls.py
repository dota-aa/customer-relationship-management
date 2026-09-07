from rest_framework.routers import SimpleRouter
from .api_views import NoeCategoryViewSet, NoteViewSet

app_name = 'notes'
urlpatterns = []

router = SimpleRouter()
router.register('notes', NoteViewSet)
router.register('note-categories', NoeCategoryViewSet)

urlpatterns += router.urls
