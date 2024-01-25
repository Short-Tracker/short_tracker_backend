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
    
    def validate(self, data):
        validated_data = super().validate(data)
        total_percentage = (
            validated_data['completed_on_time_percentage'] +
            validated_data['completed_with_delay_percentage']
        )
        if total_percentage != 100:
            raise serializers.ValidationError(
                "Сумма процентов должна быть равна 100%."
            )
        for field in [
            'average_time_todo_to_inprogress',
            'average_time_todo_to_done',
            'average_time_inprogress_to_done',
        ]:
            if validated_data[field] < 0:
                raise serializers.ValidationError(
                    f"{field} не может быть отрицательным."
                )
        return validated_data
