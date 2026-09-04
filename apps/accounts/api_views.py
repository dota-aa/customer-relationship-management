from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction

from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
)
from .services import (
    create_user,
    validate_user_token,
    activate_user_account,
    send_reset_password_email,
    change_user_password,
)
from .selectors import (
    get_user_by_email,
    get_users,
    get_profile_for_update
)
from core.pagination import StandardPagination


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)  # deserialize
        serializer.is_valid(raise_exception=True)
        user = create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password1']
        )
        return Response(UserSerializer(instance=user).data)


class UserActivationView(APIView):
    def get(self, request, uidb64, token):
        validation_result = validate_user_token(uidb64=uidb64, token=token)
        if validation_result.is_valid:
            activate_user_account(user=validation_result.user)
            return Response(
                data={'message': 'user account activated successfully'},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'errors': 'invalid link'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ---------------------------------------------------------------------------------------
# --change password--
# ---------------------------------------------------------------------------------------
class UserChangePasswordView(APIView):
    """
    An endpoint for authenticated users to change their current password.

    Permissions:
        - Requires user authentication (IsAuthenticated).

    Request Body:
        - new_password (str): The desired new password (must meet complexity requirements).
        - confirm_new_password (str): Confirmation matching the new password.

    Responses:
        - 200 OK: Password successfully updated.
        - 400 Bad Request: password mismatch, or validation errors.
        - 401 Unauthorized: User is not authenticated.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_user_password(user=request.user, password=serializer.validated_data['new_password'])
        return Response(data={'message': 'password changed successfully.'})


# ---------------------------------------------------------------------------------------
# --password recovery flow--
# ---------------------------------------------------------------------------------------
class ForgotPasswordView(APIView):
    """
       Initiates the password recovery flow for unauthenticated users.

       Sends a password reset link to the user's registered email.

       Security Note:
        To prevent User Enumeration attacks, this endpoint always returns a generic
        success response regardless of whether the email exists in the database.

       Permissions:
           - Open to all users (AllowAny).

       Request Body:
           - email (str): Registered email address to receive the reset token.

       Responses:
           - 200 OK: Password reset link sent successfully.
           - 400 Bad Request: Invalid input format.
       """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = get_user_by_email(email=serializer.validated_data['email'])
            if user:
                send_reset_password_email(user=user)

        except Exception:
            return Response(data={'errors': 'something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={'message': "a password reset link has been sent."})


class CheckResetPasswordTokenView(APIView):
    """
    Validates whether a password reset token is valid and unexpired.

    Typically used by the frontend before rendering the "Set New Password" form
    to ensure the reset link/token is still usable.

    Permissions:
        - Open to all users (AllowAny).

    Request Parameters (Query params):
        - uidb64 (str): Base64 encoded user ID.
        - token (str): The password reset token generated for the user.

    Responses:
        - 200 OK: Token is valid and ready for password reset.
        - 400 Bad Request: Token is invalid, malformed, or has expired.
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        validation_result = validate_user_token(uidb64=uidb64, token=token)
        if validation_result.is_valid:
            return Response(data={'message': 'token is verified'})
        return Response(data={'error': 'something went wrong.'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
        Completes the password reset process using a verified token.

        Permissions:
            - Open to all users (AllowAny).

        Request Body:
            - token (str): The verification token
            - uidb64(str):
            - new_password (str): The new password to replace the forgotten one.
            - confirm_new_password (str): Confirmation of the new password.

        Responses:
            - 200 OK: Password successfully reset, user can now log in with new credentials.
            - 400 Bad Request: Invalid/expired token/OTP or password validation failure.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        validation_result = validate_user_token(uidb64=vd['uidb64'], token=vd['token'])
        if validation_result.is_valid:
            change_user_password(user=validation_result.user, password=vd['new_password'])
            return Response(data={'message': 'password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(data={'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------------------
# --profile--
# ---------------------------------------------------------------------------------------
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(instance=user.profile)
        return Response(data=serializer.data)

    def patch(self, request):
        with transaction.atomic():
            profile = get_profile_for_update(user=request.user)
            serializer = UserProfileSerializer(instance=profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAdminUser]
    queryset = get_users()
    pagination_class = StandardPagination

    def list(self, request):
        serializer = UserSerializer(instance=self.queryset, many=True)
        return Response(data=serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, id=pk)
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, id=pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def destroy(self, request, pk):
        user = get_object_or_404(self.queryset, id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
