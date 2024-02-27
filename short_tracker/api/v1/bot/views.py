from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from .serializer import BotSerializer, AllowNotificationSerializer
from bot.models import AllowNotification

User = get_user_model()


class BotAPIView(ListAPIView):
    serializer_class = BotSerializer

    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(id=user)


class AllowAPIView(CreateAPIView, UpdateAPIView):
    serializer_class = AllowNotificationSerializer

    def get_queryset(self):
        user = self.request.user.id
        return AllowNotification.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




