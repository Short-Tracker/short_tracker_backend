from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'creator',
        'performer',
        'description',
        'status',
        'create_date',
        'deadline_date',
    )
    search_fields = (
        'description',
        'performer__username',
    )
    list_filter = (
        'status',
    )
