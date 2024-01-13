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
