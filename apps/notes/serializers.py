from rest_framework import serializers
from .models import NoteCategory, Note


class NoteCategorySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = NoteCategory
        fields = (
            'id', 'name',
            'created_by', 'created_by_name',
            'updated_at', 'created_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')

    def validate_name(self, value):
        if NoteCategory.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('this category already exists.')
        return value


class NoteSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    related_to = serializers.SerializerMethodField()
    related_type = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=32), required=False)

    class Meta:
        model = Note
        fields = (
            'id', 'title', 'content',
            'category', 'category_name', 'priority',
            'tags', 'pinned', 'archived',
            'related_to', 'related_type',
            'lead', 'contact', 'deal',
            'created_by', 'created_by_name',
            'updated_at', 'created_at',
        )

        read_only_fields = (
            'id', 'created_at',
            'updated_at', 'created_by'
        )

    def get_related_to(self, obj):
        if obj.lead:
            return f'{obj.lead.first_name} {obj.lead.last_name}'
        elif obj.contact:
            return f'{obj.contact.first_name} {obj.contact.last_name}'
        elif obj.deal:
            return f'{obj.deal.title}'
        return None

    def get_related_type(self, obj):
        if obj.lead:
            return 'Lead'
        elif obj.contact:
            return 'Contact'
        elif obj.deal:
            return 'Deal'
        return None

    def validate_tags(self, value):
        tags = [t.strip() for t in value if t.strip() and t.strip != ""]  # serializer checks for empty strings anyway
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError("Duplicate tags are not allowed.")
        return tags

    def validate(self, attrs):
        lead = attrs.get('lead', getattr(self.instance, 'lead', None))
        contact = attrs.get('contact', getattr(self.instance, 'contact', None))
        deal = attrs.get('deal', getattr(self.instance, 'deal', None))

        results = [lead, contact, deal]
        if not sum(1 for result in results if result) == 1:
            raise serializers.ValidationError(
                'Note should be related to one object at a time.'
            )
        return attrs
