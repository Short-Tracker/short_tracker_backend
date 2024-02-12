from api.v1.filters import TaskFilter
from django.contrib.auth import get_user_model
from django.db.models import F, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    TaskCreateSerializer,
    TaskShowSerializer,
    TaskUpdateSerializer,
)
from api.v1.filters import TaskFilter
from api.v1.permissions import (IsCreatorAndLidOrPerformerOnly,
                                IsLeadOrPerformerHimselfOnly)
from tasks.models import Task

from .serializers import (TaskCreateSerializer, TaskShowSerializer,
                          TaskUpdateSerializer)

User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_class = TaskFilter
    search_fields = ['performers__first_name', 'performers__last_name']
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'create':
            return (IsLeadOrPerformerHimselfOnly(),)
        elif self.action == 'partial_update':
            return (IsCreatorAndLidOrPerformerOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_lead:
            queryset = Task.objects.exclude(
                Q(creator=F('performers')) & ~Q(performers=user)
            ).distinct()
        else:
            queryset = Task.objects.filter(performers=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return TaskUpdateSerializer
        elif self.action == 'create':
            return TaskCreateSerializer
        return TaskShowSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
