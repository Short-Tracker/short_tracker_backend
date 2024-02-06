from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView

from .serializer import BotSerializer

User = get_user_model()


class BotAPIView(ListAPIView):
    serializer_class = BotSerializer

    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(id=user)


