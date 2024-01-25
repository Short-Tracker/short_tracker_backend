from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from .serializer import BotSerializer

User = get_user_model()


class BotAPIView(ListAPIView):
    serializer_class = BotSerializer

    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(id=user)


