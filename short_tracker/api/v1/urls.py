from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .bot.views import BotAPIView, AllowAPIView
from .message.views import MessageViewSet, ReplyViewSet
from api.v1.analytics.views import TaskAnalyticsViewSet
from api.v1.schemas import schema_view
from api.v1.tasks.views import TaskViewSet
from api.v1.users.views import login, logout, refresh_token

router_v1 = DefaultRouter()
router_v1.register('tasks', TaskViewSet, basename='tasks')
router_v1.register(
    'task-analytics', TaskAnalyticsViewSet, basename='task-analytics'
)
router_v1.register('messages', MessageViewSet, basename='messages')
router_v1.register('replies', ReplyViewSet, basename='replies')

auth_url = [
    path('login/', login, name='login'),
    path('refresh/', refresh_token, name='refresh_token'),
    path('logout/', logout, name='logout'),
]


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router_v1.urls)),
    path('notifications/', AllowAPIView.as_view()),
    path('auth/', include(auth_url)),
    path(
        'swagger<format>/',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path('bot/', BotAPIView.as_view(), name='bot')
]
