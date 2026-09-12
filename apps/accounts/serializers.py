from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.signals import user_logged_in
from django.core.cache import cache

from .models import User, Profile
from .validators import validate_avatar, process_image
from utils.bucket import bucket


S3_LINK_EXPIRATION = 12 * 60 * 60
CACHE_TIMEOUT = S3_LINK_EXPIRATION - 3600


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
    def validate(self, attrs):
        """
        User logged in, fire signal
        """
        data = super().validate(attrs)

        request = self.context.get("request")
        request.user = self.user

        user_logged_in.send(
            sender=self.user.__class__,
            request=request,
            user=self.user
        )
        return data

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
    """
    image: the field to upload an image
    image_path: the object storage presigned url
    delete_image(bool): if true delete the current profile image
    """
    user_info = serializers.SerializerMethodField()
    image = serializers.ImageField(source='avatar', write_only=True, required=False)
    image_path = serializers.SerializerMethodField(read_only=True)
    delete_image = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = Profile
        fields = ('full_name', 'job', 'birth_date', 'image', 'image_path', 'delete_image', 'bio', 'user_info')

    def validate_image(self, value):
        if value:
            validate_avatar(value)
            return process_image(value)
        return value

    def update(self, instance, validated_data):
        cache_key = f'accounts:profile:avatar:{instance.avatar.name}'
        delete_image = validated_data.pop('delete_image', False)
        new_image = validated_data.get('avatar')  # the source of image field == avatar

        if instance.avatar and delete_image:
            """
            Delete avatar from both s3 object storage and database
            Delete cache
            """
            instance.avatar.delete(save=False)  # Delete from s3 object storage to prevent orphanage files
            instance.avatar = None  # it will be saved later by the super method
            cache.delete(key=cache_key)

        elif new_image and instance.avatar and new_image != instance.avatar:
            """
            Delete the previous avatar from s3 object storage and cache
            The image path in database will be updated.
            """
            instance.avatar.delete(save=False)
            cache.delete(key=cache_key)

        return super().update(instance, validated_data)

    def get_user_info(self, obj):
        return UserSerializer(instance=obj.user).data  # serialize

    def get_image_path(self, obj):
        avatar = None
        if obj.avatar:
            cache_key = f'accounts:profile:avatar:{obj.avatar.name}'
            avatar = cache.get(key=cache_key)

            if not avatar:
                try:
                    avatar = bucket.generate_download_url(key=obj.avatar.name, expiration=S3_LINK_EXPIRATION)
                    cache.set(key=cache_key, value=avatar, timeout=CACHE_TIMEOUT)
                except Exception as e:
                    print(e)
        return avatar
