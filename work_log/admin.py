from django.contrib import admin
from .models import Tag, WorkLog

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'task_description', 'created_at')
    list_filter = ('user', 'date', 'tags')
    search_fields = ('task_description', 'user__username')
    filter_horizontal = ('tags',)
