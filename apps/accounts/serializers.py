from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .models import User, Profile
from utils.bucket import bucket

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source='is_staff')
    registered_date = serializers.DateTimeField(source='date_joined', format='%Y/%m/%d - %H:%M:%S')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'registered_date',
            'last_login',
            'is_active',
            'is_admin',
            'is_superuser',
        )
        read_only_fields = ['is_superuser', 'registered_date']


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    email = serializers.EmailField()
    password1 = serializers.CharField(max_length=128, label='password')
    password2 = serializers.CharField(max_length=128, label='confirm password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('this email is available.')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('this username is available.')
        return value

    def validate(self, attrs):
        password1 = attrs['password1']
        password2 = attrs['password2']
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError('passwords must match')
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add necessary PayLoad later
        return token


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']
        if new_password and confirm_password and new_password != confirm_password:
            raise serializers.ValidationError('Passwords must match.')
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, max_length=128)
    confirm_password = serializers.CharField(min_length=8, max_length=128)

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']
        if new_password and confirm_password and new_password != confirm_password:
            raise serializers.ValidationError('Passwords must match.')
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(source='avatar', write_only=True)
    image_path = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('full_name', 'job', 'birth_date', 'image', 'image_path', 'bio', 'user_info')

    def get_user_info(self, obj):
        user = User.objects.get(id=obj.user.id)
        return UserSerializer(instance=user).data  # serialize

    def get_image_path(self, obj):
        if obj.avatar:
            return bucket.generate_download_url(key=obj.avatar.name, expiration=86400)
        return None
