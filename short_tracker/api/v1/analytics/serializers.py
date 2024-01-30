from rest_framework import serializers

from api.v1.tasks.serializers import TaskSerializer
from tasks.models import Task


class TaskAnalyticsSerializer(serializers.ModelSerializer):
    completed_on_time_count = serializers.IntegerField()
    completed_on_time_percentage = serializers.IntegerField()
    completed_with_delay_count = serializers.IntegerField()
    completed_with_delay_percentage = serializers.IntegerField()
    avg_time_create_date_to_inprogress_date = serializers.CharField()
    avg_time_create_date_to_done_date  = serializers.CharField()
    avg_time_inprogress_date_to_done_date  = serializers.CharField()
    
    class Meta(TaskSerializer.Meta):
        model = Task 
        fields = (
            'completed_on_time_count', 'completed_on_time_percentage',
            'completed_with_delay_count', 'completed_with_delay_percentage',
            'avg_time_create_date_to_inprogress_date',
            'avg_time_create_date_to_done_date',
            'avg_time_inprogress_date_to_done_date',
        )
    
    def validate(self, data):
        validated_data = super().validate(data)
        total_tasks = self.context.get('total_tasks', None)
        total_percentage = (
            validated_data['completed_on_time_percentage'] +
            validated_data['completed_with_delay_percentage']
        )
        if (
            total_tasks is not None and 
            total_tasks > 0 and 
            total_percentage != 100):
            raise serializers.ValidationError(
                "Сумма процентов должна быть равна 100%."
            )
        return validated_data
