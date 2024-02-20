from rest_framework import serializers


class PerformerAnalyticsSerializer(serializers.Serializer):
    performer_name = serializers.CharField()
    total_tasks = serializers.IntegerField()
    completed_on_time_count = serializers.IntegerField()
    completed_with_delay_count = serializers.IntegerField()
    avg_time_create_date_to_inprogress_date = serializers.CharField()
    avg_time_create_date_to_done_date = serializers.CharField()
    avg_time_inprogress_date_to_done_date = serializers.CharField()

class TaskAnalyticsSerializer(serializers.Serializer):
    total_tasks_on_time = serializers.IntegerField()
    total_tasks_with_delay = serializers.IntegerField()
    performers_analytics = serializers.DictField(
        child=PerformerAnalyticsSerializer(), allow_empty=True, default={})

    def create(self, validated_data):
        total_tasks_on_time = validated_data.get('total_tasks_on_time', 0)
        total_tasks_with_delay = validated_data.get('total_tasks_with_delay', 0)
        performers_analytics_data = validated_data.get(
            'performers_analytics', {}
        )

        task_analytics_instance = {
            'total_tasks_on_time': total_tasks_on_time,
            'total_tasks_with_delay': total_tasks_with_delay,
            'performers_analytics': performers_analytics_data
        }
        return task_analytics_instance
