from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .schemas import schema_view
from .views import (
    TaskViewSet,
    login,
    logout,
    refresh_token,
)

router_v1 = DefaultRouter()
router_v1.register('tasks', TaskViewSet, basename='tasks')


auth_url = [
    path('login/', login, name='login'),
    path('refresh/', refresh_token, name='refresh_token'),
    path('logout/', logout, name='logout'),
]


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router_v1.urls)),
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
]
