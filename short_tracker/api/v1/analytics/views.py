from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from .analytics import TasksAnalyticsFactory
from .serializers import TaskAnalyticsSerializer
from api.v1.filters import TaskAnalyticsFilter
from api.v1.permissions import IsTeamLead
from tasks.models import Task


class TaskAnalyticsViewSet(viewsets.ReadOnlyModelViewset):
    queryset = Task.objects.all()
    serializer_class = TaskAnalyticsSerializer
    permission_classes = (IsTeamLead,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskAnalyticsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(
        TasksAnalyticsFactory.calculate_analytics(queryset)
        )
        return Response(serializer.data)
