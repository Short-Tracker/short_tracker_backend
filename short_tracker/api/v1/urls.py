from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .schemas import schema_view
from .views import TaskViewSet

router_v1 = DefaultRouter()
router_v1.register('tasks', TaskViewSet, basename='tasks')


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.jwt')),
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
