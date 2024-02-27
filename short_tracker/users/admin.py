from django.contrib.admin import ModelAdmin, register

from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'telegram_nickname',
        'email',
        'is_team_lead',
    )
    search_fields = (
        'telegram_nickname',
    )
    list_filter = (
        'is_team_lead',
    )
