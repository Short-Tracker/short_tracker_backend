from django.db.models import ExpressionWrapper, F, Sum, fields

from tasks.models import Task


class TasksAnalyticsFactory:
    @staticmethod
    def calculate_analytics(queryset):
        analytics = {}
        total_tasks = queryset.count()
        analytics.update({
            'completed_on_time_count': queryset.filter(
                status=Task.TaskStatus.DONE,
                finish_date__lte=F('deadline_date')
            ).count(),
            'completed_with_delay_count': queryset.filter(
                status=Task.TaskStatus.DONE,
                finish_date__gt=F('deadline_date')
            ).count(),
        })

        analytics.update(
            TasksAnalyticsFactory._calculate_percentage(analytics, total_tasks)
        )

        analytics.update(
            TasksAnalyticsFactory._calculate_average_time(
                queryset, total_tasks
            )
        )

        return analytics

    @staticmethod
    def _calculate_percentage(analytics, total_tasks):
        return {
            f'{key}_percentage': (
                (value / total_tasks) * 100
            ) if total_tasks > 0 else 0
            for key, value in analytics.items()
        }

    @staticmethod
    def _calculate_average_times(queryset, total_tasks):
        def calculate_avg_time(field1, field2):
            avg_time_key = f'average_time_{field1}_to_{field2}'
            avg_time = queryset.filter(
                status=Task.TaskStatus.DONE,
                **{f'{field1}__isnull': False, f'{field2}__isnull': False}
            ).aggregate(
                avg_time=ExpressionWrapper(
                    Sum(F(field2) - F(field1)),
                    output_field=fields.DurationField()
                )
            )['avg_time']

            return {
                avg_time_key: avg_time / total_tasks if total_tasks > 0 else 0
            }

        return {
            **calculate_avg_time('start_date', 'inprogress_date'),
            **calculate_avg_time('start_date', 'finish_date'),
            **calculate_avg_time('inprogress_date', 'finish_date'),
        }
