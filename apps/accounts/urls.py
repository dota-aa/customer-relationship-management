from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from . import api_views


jwt_urlpatterns = [
    path('register/', api_views.UserRegisterView.as_view(), name='user_register'),
    path('login/', api_views.CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


app_name = 'accounts'
urlpatterns = [
    path('auth/', include(jwt_urlpatterns)),
    path('user/', api_views.UserProfileView.as_view()),
]
