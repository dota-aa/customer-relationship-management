from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()  # default -> read only = Ture

    class Meta:
        model = Contact
        fields = (
            'id',
            'full_name',
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
        first_name = creator.first_name
        last_name = creator.last_name

        if first_name and last_name:
            return f'{first_name} {last_name}'
        return creator.email
