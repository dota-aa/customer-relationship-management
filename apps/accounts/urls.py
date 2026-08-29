from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from . import api_views


jwt_urlpatterns = [
    path('register/', api_views.UserRegisterView.as_view()),
    path('activate/<uidb64>/<token>/', api_views.UserActivationView.as_view()),
    path('login/', api_views.CustomTokenObtainView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('change-password/', api_views.UserChangePasswordView.as_view()),
    path('reset-password/', api_views.ForgotPasswordView.as_view()),
    path('reset-password/verify/<uidb64>/<token>/', api_views.CheckResetPasswordTokenView.as_view()),
    path('reset-password/confirm/', api_views.ResetPasswordView.as_view()),

]


app_name = 'accounts'
urlpatterns = [
    path('auth/', include(jwt_urlpatterns)),
    path('user/', api_views.UserProfileView.as_view()),
]
