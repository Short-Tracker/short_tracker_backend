from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from tasks.models import Task

User = get_user_model()


STATUS_TIME = {
    'in progress': 'inprogress_date',
    'done': 'finish_date',
    'archived': 'archive_date',
}


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""

    class Meta:
        model = User
        fields = (
            'username', 'telegram_nickname', 'email',
            'first_name', 'last_name', 'is_team_lead'
        )


class ShortUserSerializer(serializers.ModelSerializer):
    """Serializer for short representation of users."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'telegram_nickname', 'email',
        )

    def get_full_name(self, obj):
        """
        Get the full name of an object or return the nickname of telegram.
        """

        if obj.last_name and obj.first_name:
            return f'{obj.first_name} {obj.last_name[:1]}.'
        return 'ФИО не указано.'


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    class Meta:
        model = Task
        fields = (
            'description', 'status', 'start_date', 'inprogress_date',
            'finish_date', 'deadline_date', 'archive_date', 'comment', 'link'
        )
        read_only_fields = (
            'archive_date', 'inprogress_date', 'finish_date', 'is_expired'
        )


class TaskShowSerializer(TaskSerializer):
    """Serializer for show tasks."""

    creator = ShortUserSerializer(read_only=True)
    performers = ShortUserSerializer(many=True)
    is_expired = serializers.SerializerMethodField()

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + (
            'creator', 'performers', 'is_expired',
        )
        read_only_fields = TaskSerializer.Meta.read_only_fields + (
            'is_expired',
        )

    def get_is_expired(self, obj):
        """
        Check if the task is expired or not.
        """
        return (
            obj.deadline_date < timezone.now().date()
            and obj.status not in ('done', 'archived')
        )


class TaskCreateSerializer(TaskSerializer):
    """Serializer for create tasks."""

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ('performers',)


class TaskUpdateSerializer(TaskCreateSerializer):
    """Serializer for update tasks."""

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            validated_data[
                STATUS_TIME.get(validated_data.get('status'))
            ] = timezone.now().date()
        return super().update(instance, validated_data)
