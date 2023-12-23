from django.db.models import Q
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
    """

    creator = filters.CharFilter(field_name='creator__id',)
    performer = filters.CharFilter(field_name='performers__id',)
    status = filters.CharFilter(field_name='status',)
    description = filters.CharFilter(method='filter_description',)
    is_expired = filters.BooleanFilter(method='filter_is_expired',)

    class Meta:
        model = Task
        fields = (
            'creator', 'performer', 'status', 'description', 'is_expired',
        )

    def filter_description(self, queryset, _, value):
        """
        Filter the queryset based on the description field.
        """
        query = Q()
        for word in value.split():
            query |= Q(description__icontains=word)
        return queryset.filter(query).distinct()

    def filter_is_expired(self, queryset, _, value):
        """
        Filter the queryset based on the is_expired field.
        """
        return queryset.filter(
            deadline_date__lt=timezone.now(),
            status__in=('in progress', 'hold', 'to do'),
        )
