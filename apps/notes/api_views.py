from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import NoteCategorySerializer, NoteSerializer
from .models import NoteCategory, Note
from core.pagination import MediumPagination, StandardPagination

class NoeCategoryViewSet(ModelViewSet):
    queryset = NoteCategory.objects.all()
    serializer_class = NoteCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MediumPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = [
        'title',
        'lead',
        'contact',
        'deal',
    ]

    search_fields = [
        'title',
        'content',
    ]

    ordering_fields = [
        'title',
        'updated_at',
        'created_at',
        'pinned',
        'archived',
        'priority'
    ]

    ordering = ['-pinned', '-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(methods=["patch"], detail=True, url_path='pin')
    def pin(self, request, pk=None):
        instance = self.get_object()
        instance.pinned = True
        instance.save(update_fields=['pinned'])
        return Response(
            data=self.serializer_class(instance).data
        )

    @action(methods=["patch"], detail=True, url_path='unpin')
    def unpin(self, request, pk=None):
        instance = self.get_object()
        instance.pinned = False
        instance.save(update_fields=['pinned'])
        return Response(
            data=self.serializer_class(instance).data
        )

    @action(methods=['patch'], detail=True, url_path='archive')
    def archive(self, request, pk=None):
        instance = self.get_object()
        instance.archived = True
        instance.save(update_fields=['archived'])
        return Response(
            data=self.serializer_class(instance).data
        )

    @action(methods=['patch'], detail=True, url_path='unarchive')
    def unarchive(self, request, pk=None):
        instance = self.get_object()
        instance.archived = False
        instance.save(update_fields=['archived'])
        return Response(
            data=self.serializer_class(instance).data
        )
