from django.contrib import admin
from .models import NoteCategory, Note


@admin.register(NoteCategory)
class NoteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'category', 'priority', 'pinned', 'archived', 'tags', 'created_by')
