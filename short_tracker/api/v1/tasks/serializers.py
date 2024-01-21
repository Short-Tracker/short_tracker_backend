from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from api.v1.users.serializers import ShortUserSerializer
from tasks.models import Task

User = get_user_model()

task_status = Task.TaskStatus

STATUS_TIME = {
    task_status.IN_PROGRESS: 'inprogress_date',
    task_status.DONE: 'done_date',
    task_status.ARCHIVED: 'archive_date',
}

RESOLVED_STATUS = {
    'employee': {
        task_status.TO_DO: (task_status.IN_PROGRESS, task_status.HOLD),
        task_status.IN_PROGRESS: (task_status.DONE, task_status.HOLD),
    },
    'lead': {
        task_status.TO_DO: (task_status.IN_PROGRESS, task_status.HOLD),
        task_status.IN_PROGRESS: (task_status.DONE, task_status.HOLD),
        task_status.DONE: (task_status.ARCHIVED),
        task_status.ARCHIVED: (task_status.TO_DO),
    }
}


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    class Meta:
        model = Task
        fields = (
            'description', 'status', 'create_date', 'inprogress_date',
            'done_date', 'deadline_date', 'archive_date', 'link'
        )
        read_only_fields = (
            'archive_date', 'inprogress_date', 'done_date', 'is_expired'
        )


class TaskShowSerializer(TaskSerializer):
    """Serializer for show tasks."""

    creator = ShortUserSerializer(read_only=True)
    performers = ShortUserSerializer(many=True)
    is_expired = serializers.SerializerMethodField()
    resolved_status = serializers.SerializerMethodField()

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + (
            'creator', 'performers', 'is_expired', 'resolved_status',
        )
        read_only_fields = TaskSerializer.Meta.read_only_fields + (
            'is_expired', 'resolved_status',
        )

    def get_is_expired(self, obj):
        """
        Check if the task is expired or not.
        """
        return (
            obj.deadline_date < timezone.now().date()
            and obj.status not in ('done', 'archived')
        )

    def get_resolved_status(self, obj):
        """
        Get the resolved status of the task.
        """
        role = 'lead' if self.context['request'].user.is_lead else 'employee'
        return RESOLVED_STATUS.get(role, 'employee').get(obj.status, ())


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
