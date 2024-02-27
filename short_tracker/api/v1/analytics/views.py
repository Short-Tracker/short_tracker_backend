from datetime import timedelta

from django.db.models import Prefetch, Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response

from .analytics import TasksAnalyticsFactory
from .serializers import TaskAnalyticsSerializer
from api.v1.filters import TaskAnalyticsFilter
from api.v1.permissions import IsTeamLead
from tasks.models import Task
from users.models import CustomUser


class TaskAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskAnalyticsSerializer
    permission_classes = (IsTeamLead,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskAnalyticsFilter

    def get_queryset(self):
        queryset = Task.objects.filter(
                 status=Task.TaskStatus.DONE
                 ).prefetch_related(
                      Prefetch(
                           'performer',
                            queryset=CustomUser.objects.filter(
                                 is_team_lead=False
                            )
                      )
        )
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date or end_date:
            filterset = TaskAnalyticsFilter(
                self.request.query_params,
                queryset=queryset, request=self.request
            )
            if filterset.is_valid():
                queryset = filterset.qs
        else:
                return queryset.filter(
                     Q(done_date__gte=timezone.now() - timedelta(days=7)))
        return queryset

    def list(self, request, *args, **kwargs):
        sort_by = request.query_params.get('sort_by')
        serializer = TaskAnalyticsSerializer(
            data=TasksAnalyticsFactory.calculate_analytics(
                self.get_queryset(), sort_by=sort_by
        ))
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)