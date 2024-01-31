import datetime
from datetime import timedelta

from django.db.models import F

from tasks.models import Task


class TasksAnalyticsFactory:
    @staticmethod
    def calculate_analytics(queryset):
        analytics = {}
        total_tasks = queryset.count()
        analytics.update(
            TasksAnalyticsFactory.tasks_count(queryset, total_tasks)
        )
        avg_time = {
            'avg_time_create_date_to_inprogress_date': 
                TasksAnalyticsFactory.avg_time(
                    queryset, 'create_date', 'inprogress_date'
            ),
            'avg_time_create_date_to_done_date': 
                TasksAnalyticsFactory.avg_time(
                    queryset, 'create_date', 'done_date'
            ),
            'avg_time_inprogress_date_to_done_date': 
                TasksAnalyticsFactory.avg_time(
                    queryset, 'inprogress_date', 'done_date'
            )
        }
        analytics.update(**avg_time)
        return analytics

    @staticmethod
    def tasks_count(queryset, total_tasks):
        completed_on_time_count = queryset.filter(
            status=Task.TaskStatus.DONE,
            done_date__lte=F('deadline_date')
        ).count()
        completed_with_delay_count = queryset.filter(
            status=Task.TaskStatus.DONE,
            done_date__gt=F('deadline_date')
        ).count()
        completed_on_time_percentage = (
            int((completed_on_time_count / total_tasks) * 100)
        ) if total_tasks > 0 else 0
        completed_with_delay_percentage = (
            int((completed_with_delay_count / total_tasks) * 100)
        ) if total_tasks > 0 else 0
        return {
            'completed_on_time_count': completed_on_time_count,
            'completed_with_delay_count': completed_with_delay_count,
            'completed_on_time_percentage': completed_on_time_percentage,
            'completed_with_delay_percentage': completed_with_delay_percentage,
        }

    @staticmethod
    def avg_time(queryset, field1, field2):
        datetime_list = [
            getattr(task, field2) - getattr(task, field1)
            for task in queryset
            if task.status == Task.TaskStatus.DONE and
            getattr(task, field1) and getattr(task, field2)
        ]
        sum_of_time = sum(datetime_list, datetime.timedelta())
        length = len(datetime_list)
        avg_time = sum_of_time // length if length > 0 else timedelta()
        return str(avg_time).rsplit(':', 1)[0]
