from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()  # default -> read only = Ture

    class Meta:
        model = Contact
        fields = (
            'id',
            'first_name',
            'last_name',
            'company',
            'email',
            'phone_number',
            'job_title',
            'creator',
            'status',
            'last_interaction',
        )
        read_only_fields = ('id', 'created_by', 'created_at')

    def get_creator(self, obj):
        creator = obj.created_by
        username = creator.username

        if username:
            return f'{username}'
        return creator.email
