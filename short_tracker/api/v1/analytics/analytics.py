
from django.db.models import F

from users.models import CustomUser


class TasksAnalyticsFactory:
    @staticmethod
    def calculate_analytics(queryset, sort_by=None):
        analytics = {}
        analytics.update(
            TasksAnalyticsFactory.tasks_count(queryset)
        )
        analytics.update(
            TasksAnalyticsFactory.performers_analytics(
                queryset, sort_by)
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
    def performers_analytics(queryset, sort_by=None):
        performers_analytics = []
        performers_ids = queryset.values_list(
            'performer_id', flat=True).distinct()
        for performer_id in performers_ids:
            performer = CustomUser.objects.get(id=performer_id)
            filtered_queryset = queryset.filter(performer=performer)
            performer_name = f"{performer.first_name} {performer.last_name}"
            on_time_count = filtered_queryset.filter(
                done_date__lte=F('deadline_date'),
                performer=performer).count()
            with_delay_count = filtered_queryset.filter(
                done_date__gt=F('deadline_date'),
                performer=performer).count()
            total_tasks = on_time_count + with_delay_count
            performer_data = {
                'performer_id': performer_id,
                'performer_name': performer_name,
                'total_tasks': total_tasks,
                'on_time_count': on_time_count,
                'with_delay_count': with_delay_count,
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
            performers_analytics.append(performer_data)
        performers_analytics = TasksAnalyticsFactory.sort_by(
            performers_analytics, sort_by)
        return {'performers_analytics': performers_analytics}
    
    @staticmethod
    def sort_by(performers_analytics, sort_by=None):
        key_mapping = {
        'total_tasks': 'total_tasks',
        'on_time_count': 'on_time_count',
        'with_delay_count': 'with_delay_count',
        }
        key = key_mapping.get(sort_by, 'on_time_count')
        performers_analytics = sorted(
                performers_analytics,
                key=lambda x: x[key], reverse=True
                )
        return performers_analytics

    @staticmethod
    def avg_time(queryset, field1, field2):
        time_list_minutes  = [
            (getattr(task, field2) - getattr(task, field1)).total_seconds() / 60
            for task in queryset
            if getattr(task, field1) and getattr(task, field2)
        ]
        avg_time = (
            sum(time_list_minutes ) / len(time_list_minutes )
            if len(time_list_minutes ) > 0
            else 0
        )
        return int(avg_time)