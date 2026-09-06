from rest_framework import serializers
from .models import Deal


class DealSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.first_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Deal
        fields = (
            'pk',
            'title',
            'contact',
            'contact_name',
            'amount',
            'stage',
            'expected_close_date',
            'closed_date',
            'probability',
            'notes',
            'created_by',
            'created_by_name',
            'updated_at',
            'created_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('amount acn not be less than zero')
        return value

    def validate_probability(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError('Probability must be between 0 and 100.')
        return value
