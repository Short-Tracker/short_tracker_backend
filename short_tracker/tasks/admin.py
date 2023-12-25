from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'creator',
        'display_performers',
        'description',
        'status',
        'start_date',
        'deadline_date',
    )
    search_fields = (
        'description',
        'performers__username',
    )
    list_filter = (
        'status',
    )

    def display_performers(self, obj):
        """
        Generates a string with the first name and last initial
        of each performer in the given object.
        """
        objs = obj.performers.all()
        return ' '.join(
            [f'{user.first_name} {user.last_name[:1]}.' for user in objs]
        )
    display_performers.short_description = 'Performers'
