from django.db.models import Case, Q, Value, When
from django.utils import timezone
from django_filters.rest_framework import FilterSet, filters

from tasks.models import Task


class TaskFilter(FilterSet):
    """
    A filter set for the Task model.

    Available filters:
    - creator: Filter tasks by the ID of the creator.
    - performer: Filter tasks by the ID of the performer.
    - status: Filter tasks by the status.
    - description: Filter tasks based on the description field.
    - is_expired: Filter tasks based on whether they are expired.
    - start_date: Filter tasks based on the start date.
    - end_date: Filter tasks based on the end date.
    """

    creator = filters.CharFilter(field_name='creator__id',)
    performer = filters.CharFilter(field_name='performers__id',)
    status = filters.CharFilter(field_name='status',)
    description = filters.CharFilter(method='filter_description',)
    is_expired = filters.BooleanFilter(method='filter_is_expired',)
    start_date = filters.DateFilter(
        field_name='create_date', lookup_expr=('gt')
    )
    end_date = filters.DateFilter(field_name='create_date', lookup_expr=('lt'))

    class Meta:
        model = Task
        fields = (
            'creator', 'performer', 'status', 'description', 'is_expired',
        )

    def filter_description(self, queryset, _, value):
        """
        Filter the queryset based on the description field.
        """
        words = value.lower().split()
        for i in range(1, len(words)):
            words.append(' '.join(words[:i+1]))

        query = Q()
        for word in words:
            query |= Q(description__icontains=word)

        phrase_start = Case(
            *[When(
                description__istartswith=word, then=Value(True)
            ) for word in words],
            default=Value(False),
        )

        return queryset.filter(query).annotate(
            description_start=phrase_start,
        ).order_by('-description_start', '-description')

    def filter_is_expired(self, queryset, _, value):
        """
        Filter the queryset based on the is_expired field.
        """
        if value:
            queryset = queryset.filter(
                deadline_date__lt=timezone.now(),
                status__in=('in progress', 'hold', 'to do'),
            )
        else:
            queryset = queryset.filter(
                deadline_date__gte=timezone.now(),
            )
        return queryset


class TaskAnalyticsFilter(FilterSet):
    performer_id = filters.NumberFilter(
        field_name='performers', method='filter_by_performer'
    )
    week = filters.NumberFilter(
        field_name='start_date__week', method='filter_by_week'
    )
    month = filters.NumberFilter(
        field_name='start_date__month', method='filter_by_month'
    )
    custom_period = filters.DateFromToRangeFilter(
        field_name='start_date', method='filter_by_custom_period'
    )

    class Meta:
        model = Task
        fields = ['week', 'month', 'custom_period']

    def filter_by_performer(self, queryset, name, value):
        if value:
            return queryset.filter(performers__in=[value])
        return queryset

    def filter_by_week(self, queryset, name, value):
        performer_id = self.request.query_params.get('performer_id')
        if value:
            return queryset.filter(
                start_date__week=value, performers__id=performer_id)
        return queryset

    def filter_by_month(self, queryset, name, value):
        performer_id = self.request.query_params.get('performer_id')
        if value:
            return queryset.filter(
                start_date__month=value, performers__id=performer_id)
        return queryset

    def filter_by_custom_period(self, queryset, name, value):
        performer_id = self.request.query_params.get('performer_id')
        if value:
            return queryset.filter(
                start_date__range=(value.start, value.stop),
                performers__id=performer_id)
        return queryset
