from rest_framework import serializers

from api.v1.tasks.serializers import TaskSerializer


class TaskAnalyticsSerializer(TaskSerializer):
    completed_on_time_count = serializers.IntegerField()
    completed_on_time_percentage = serializers.FloatField()
    completed_with_delay_count = serializers.IntegerField()
    completed_with_delay_percentage = serializers.FloatField()
    average_time_todo_to_inprogress = serializers.DurationField()
    average_time_todo_to_done = serializers.DurationField()
    average_time_inprogress_to_done = serializers.DurationField()
    
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + (
            'completed_on_time_count', 'completed_on_time_percentage',
            'completed_with_delay_count', 'completed_with_delay_percentage',
            'average_time_todo_to_inprogress', 'average_time_todo_to_done',
            'average_time_inprogress_to_done',
        )
