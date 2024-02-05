import datetime
from datetime import timedelta

from django.db.models import F

from users.models import CustomUser


class TasksAnalyticsFactory:
    @staticmethod
    def calculate_analytics(queryset):
        analytics = {}
        analytics.update(
            TasksAnalyticsFactory.tasks_count(queryset)
        )
        analytics.update(
            TasksAnalyticsFactory.performers_analytics(
                queryset)
        )
        return analytics

    @staticmethod
    def tasks_count(queryset):
        return {
            'total_tasks_on_time': 
            queryset.filter(
                done_date__lte=F('deadline_date')).count(),
            'total_tasks_with_delay':
            queryset.filter(
                done_date__gt=F('deadline_date')).count()
        }
    
    @staticmethod
    def performers_analytics(queryset):
        performers_analytics = {}
        performers_ids = queryset.values_list(
            'performers', flat=True).distinct()
        for performer_id in performers_ids:
            performer = CustomUser.objects.get(id=performer_id)
            filtered_queryset = queryset.filter(performers=performer)
            performer_name = f"{performer.first_name} {performer.last_name}"
            completed_on_time_count = filtered_queryset.filter(
                done_date__lte=F('deadline_date'),
                performers=performer).count()
            completed_with_delay_count = filtered_queryset.filter(
                done_date__gt=F('deadline_date'),
                performers=performer).count()
            performers_analytics[performer_id] = {
                'performer_name': performer_name,
                'completed_on_time_count': completed_on_time_count,
                'completed_with_delay_count': 
                completed_with_delay_count,
                'avg_time_create_date_to_inprogress_date': 
                TasksAnalyticsFactory.avg_time(
                    filtered_queryset, 'create_date', 'inprogress_date'),
                'avg_time_create_date_to_done_date': 
                TasksAnalyticsFactory.avg_time(
                    filtered_queryset, 'create_date', 'done_date'),
                'avg_time_inprogress_date_to_done_date': 
                TasksAnalyticsFactory.avg_time(
                    filtered_queryset, 'inprogress_date', 'done_date'),
            }
        return {'performers_analytics': performers_analytics}

    @staticmethod
    def avg_time(queryset, field1, field2):
        datetime_list = [
            getattr(task, field2) - getattr(task, field1)
            for task in queryset
            if getattr(task, field1) and getattr(task, field2)
        ]
        sum_of_time = sum(datetime_list, datetime.timedelta())
        length = len(datetime_list)
        avg_time = sum_of_time // length if length > 0 else timedelta()
        return str(avg_time).rsplit(':', 1)[0]
