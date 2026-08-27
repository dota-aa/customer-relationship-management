from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source='is_staff', read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'date_joined',
            'last_login',
            'is_active',
            'is_admin',
            'is_superuser',
        )


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


class UserProfileSerializer(serializers.Serializer):
    user_info = serializers.ModelSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('full_name', 'job', 'birth_date', 'avatar', 'bio')

    def get_user_info(self, obj):
        user = User.objects.get(id=obj.user.id)
        return UserSerializer(instance=user).data  # serialize
