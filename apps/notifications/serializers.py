from rest_framework import serializers
from .models import Notification, NotificationSettings


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user',)


class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        exclude = ('created_at',)
        read_only_fields = ('user',)
