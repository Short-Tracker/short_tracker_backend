from django.urls import include, path

from api.v1.schemas import schema_view
from api.v1.users.views import (
    login,
    logout,
    refresh_token,
)

auth_url = [
    path('login/', login, name='login'),
    path('refresh/', refresh_token, name='refresh_token'),
    path('logout/', logout, name='logout'),
]


urlpatterns = [
    path('', include('djoser.urls')),
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
