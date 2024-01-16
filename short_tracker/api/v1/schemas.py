from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ('https', 'http')
        return schema


schema_view = get_schema_view(
   openapi.Info(
      title='Short Tracker API',
      default_version='v1',
      description=(
          'API для taskmanager (Short Tracker)'
        ),
      terms_of_service='https://www.google.com/policies/terms/',
      license=openapi.License(name='BSD License'),
   ),
   generator_class=BothHttpAndHttpsSchemaGenerator,
   public=True,
   permission_classes=(permissions.AllowAny,),
)

LOGIN_SCHEMA = openapi.Schema(
   type=openapi.TYPE_OBJECT,
   required=('email', 'password',),
   properties={
      'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
      'password': openapi.Schema(type=openapi.TYPE_STRING, min_length=8),
   },
)

LOGIN_DONE_SCHEMA = openapi.Schema(
   type=openapi.TYPE_OBJECT,
   required=('id', 'full_name', 'telegram_nickname', 'email'),
   properties={
      'id': openapi.Schema(type=openapi.TYPE_STRING),
      'full_name': openapi.Schema(type=openapi.TYPE_STRING),
      'telegram_nickname': openapi.Schema(type=openapi.TYPE_STRING),
      'email': openapi.Schema(type=openapi.TYPE_STRING, format='email')
   }
)

LOGOUT_SCHEMA = openapi.Schema(
   type=openapi.TYPE_OBJECT,
   required=('signout',),
   properties={
      'signout': openapi.Schema(
         type=openapi.TYPE_STRING,
         default=('Вы успешно вышли из учетной записи!')
      )
   }
)

REFRESH_DONE_SCHEMA = openapi.Schema(
   type=openapi.TYPE_OBJECT,
   required=('refresh',),
   properties={
      'refresh': openapi.Schema(
         type=openapi.TYPE_STRING,
         default=('Токен успешно обновлен!')
      )
   }
)
