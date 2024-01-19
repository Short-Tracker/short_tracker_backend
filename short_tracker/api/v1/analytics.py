from django.db.models import ExpressionWrapper, F, Sum, fields

from tasks.models import Task


class TasksAnalyticsFactory:
    @staticmethod
    def calculate_analytics(queryset):
        analytics = {}
        total_tasks = queryset.count()
        completed_on_time = queryset.filter(
            status=Task.TaskStatus.DONE,
            finish_date__lte=F('deadline_date')
        ).count()
        analytics['completed_on_time_count'] = completed_on_time
        analytics['completed_on_time_percentage'] = (
            (completed_on_time / total_tasks) * 100
        ) if total_tasks > 0 else 0
        completed_with_delay = queryset.filter(
            status=Task.TaskStatus.DONE,
            finish_date__gt=F('deadline_date')
        ).count()
        analytics['completed_with_delay_count'] = completed_with_delay
        analytics['completed_with_delay_percentage'] = (
            (completed_with_delay / total_tasks) * 100
        ) if total_tasks > 0 else 0

        average_time_todo_to_inprogress = queryset.aggregate(
            avg_time=ExpressionWrapper(
                Sum(F('inprogress_date') - F('start_date')),
                output_field=fields.DurationField()
            )
        )['avg_time_todo_to_inprogress']
        analytics['average_time_todo_to_inprogress'] = (
            average_time_todo_to_inprogress / total_tasks
        ) if total_tasks > 0 else 0

        average_time_todo_to_done = queryset.filter(
            status=Task.TaskStatus.DONE,
            inprogress_date__isnull=False,
            start_date__isnull=False
        ).aggregate(
            avg_time=ExpressionWrapper(
                Sum(F('finish_date') - F('start_date')),
                output_field=fields.DurationField()
            )
        )['avg_time_todo_to_done']
        analytics['average_time_todo_to_done'] = (
            average_time_todo_to_done / total_tasks
        ) if total_tasks > 0 else 0

        average_time_inprogress_to_done = queryset.filter(
            status=Task.TaskStatus.DONE,
            inprogress_date__isnull=False
        ).aggregate(
            avg_time=ExpressionWrapper(
                Sum(F('finish_date') - F('inprogress_date')),
                output_field=fields.DurationField()
            )
        )['avg_time_inprogress_to_done']
        analytics['average_time_inprogress_to_done'] = (
            average_time_inprogress_to_done / total_tasks
        )if total_tasks > 0 else 0
        
        return analytics
