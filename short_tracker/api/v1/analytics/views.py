from datetime import datetime, timedelta

from django.db.models import Prefetch
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
                           'performers',
                            queryset=CustomUser.objects.filter(
                                 is_team_lead=False
                            )
                      )
        )
        if self.request.query_params:
            filterset = TaskAnalyticsFilter(
                self.request.query_params,
                queryset=queryset, request=self.request)
            if filterset.is_valid():
                    queryset = filterset.qs
        else:
            queryset = Task.objects.filter(
                 done_date__gte=datetime.today() - timedelta(days=7))
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = TaskAnalyticsSerializer(
            data=TasksAnalyticsFactory.calculate_analytics(
                self.get_queryset()
                )
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
