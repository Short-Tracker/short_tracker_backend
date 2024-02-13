from django.contrib.auth import get_user_model
from django.utils import timezone
from message.models import Message
from rest_framework import serializers

from api.v1.message.serializers import MessageSerializer
from api.v1.users.serializers import ShortUserSerializer
from tasks.models import Task
from users.models import ROLES

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
            'id', 'description', 'status', 'create_date', 'inprogress_date',
            'done_date', 'deadline_date', 'archive_date', 'link'
        )
        read_only_fields = (
            'id', 'archive_date', 'inprogress_date', 'done_date', 'is_expired'
        )


class TaskShowSerializer(TaskSerializer):
    """Serializer for show tasks."""

    creator = ShortUserSerializer(read_only=True)
    performer = ShortUserSerializer()
    is_expired = serializers.SerializerMethodField()
    resolved_status = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + (
            'creator', 'performer', 'is_expired', 'resolved_status', 'message',
        )
        read_only_fields = TaskSerializer.Meta.read_only_fields + (
            'is_expired', 'resolved_status', 'message',
        )

    def get_is_expired(self, obj):
        """
        Check if the task is expired or not.
        """
        return (
            obj.deadline_date < timezone.now()
            and obj.status not in ('done', 'archived')
        )

    def get_resolved_status(self, obj):
        """
        Get the resolved status of the task.
        """
        is_lead = self.context['request'].user.is_lead
        role = ROLES.get('lead') if is_lead else ROLES.get('employee')
        return RESOLVED_STATUS.get(
            role, ROLES.get('employee')).get(obj.status, ())

    def get_message(self, obj):
        """
        Get the messages of the task.
        """
        messages = Message.objects.filter(task=obj)
        return MessageSerializer(messages, many=True).data


class TaskCreateSerializer(TaskSerializer):
    """Serializer for create tasks."""
    performers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True
    )

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ('performer', 'performers',)
        read_only_fields = TaskSerializer.Meta.read_only_fields + (
            'performer',)

    def create(self, validated_data):

        performers = validated_data.pop('performers')
        if len(performers) == 1:
            validated_data['performer'] = performers[0]
            return [Task.objects.create(**validated_data)]

        tasks = []
        for performer in performers:
            tasks.append(Task(performer=performer, **validated_data))

        Task.objects.bulk_create(tasks)
        return tasks

    def to_representation(self, instance):
        """
        Serialize objects.
        """
        tasks_data = {
            'id': [task.id for task in instance],
        }
        return tasks_data


class TaskUpdateSerializer(TaskCreateSerializer):
    """Serializer for update tasks."""

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            time = STATUS_TIME.get(validated_data.get('status'))
            if time:
                validated_data[time] = timezone.now()
            if (
                validated_data.get('status') == task_status.DONE
                and timezone.now() <= instance.deadline_date
            ):
                validated_data['get_medals'] = True
        return super().update(instance, validated_data)
