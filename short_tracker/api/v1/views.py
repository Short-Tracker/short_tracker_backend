from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .filters import TaskFilter
from .serializers import (
    TaskCreateSerializer,
    TaskShowSerializer,
    TaskUpdateSerializer,
)
from tasks.models import Task
from api.v1.serializers import (
    AuthSignInSerializer,
    ShortUserSerializer,
)

User = get_user_model()

ACCESS_TOKEN_LIFETIME = int(
    django_settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', 0).total_seconds()
)
REFRESH_TOKEN_LIFETIME = int(
    django_settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME', 0).total_seconds()
)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    serializer = AuthSignInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    access_token = AccessToken.for_user(
        serializer.validated_data.get('user')
    )
    refresh_token = RefreshToken.for_user(
        serializer.validated_data.get('user')
    )
    response = Response(
        ShortUserSerializer(user).data, status=status.HTTP_200_OK
    )
    response.set_cookie(
        'jwt_access', str(access_token), expires=ACCESS_TOKEN_LIFETIME,
        httponly=True, samesite='None', secure=True,
    )
    response.set_cookie(
        'jwt_refresh', str(refresh_token), expires=REFRESH_TOKEN_LIFETIME,
        httponly=True, samesite='None', secure=True,
    )
    return response


@api_view(['POST'])
def sign_out(request):
    response = Response(
        data={'signout': ('Вы успешно вышли из учетной записи!')},
        status=status.HTTP_200_OK
    )
    response.delete_cookie('jwt_access', samesite='None',)
    response.delete_cookie('jwt_refresh', samesite='None',)
    return response


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return TaskUpdateSerializer
        elif self.action == 'create':
            return TaskCreateSerializer
        return TaskShowSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)