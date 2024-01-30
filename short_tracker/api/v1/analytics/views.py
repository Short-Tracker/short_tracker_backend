from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response

from .analytics import TasksAnalyticsFactory
from .serializers import TaskAnalyticsSerializer
from api.v1.filters import TaskAnalyticsFilter
from api.v1.permissions import IsTeamLead
from tasks.models import Task


class TaskAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskAnalyticsSerializer
    permission_classes = (IsTeamLead,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskAnalyticsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = TaskAnalyticsSerializer(
            data=TasksAnalyticsFactory.calculate_analytics(queryset)
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
