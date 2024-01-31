from django.contrib.auth import get_user_model
from django.db.models import F, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    TaskCreateSerializer,
    TaskShowSerializer,
    TaskUpdateSerializer,
)
from api.v1.filters import TaskFilter
from api.v1.permissions import IsCreatorOnly, IsLeadOrPerformerHimselfOnly
from tasks.models import Task

User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'create':
            return (IsLeadOrPerformerHimselfOnly(),)
        elif self.action == 'partial_update':
            return (IsCreatorOnly(),)
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
