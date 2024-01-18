from django_filters.rest_framework import DjangoFilterBackend
from message.models import Message, Reply
from rest_framework.viewsets import ModelViewSet

from .serializers import MessageSerializer, ReplySerializer


class MessageViewSet(ModelViewSet):
    """Вьюсет запрос к тимлиду."""
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('task', 'message_status', )

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ReplyViewSet(ModelViewSet):
    """Вьюсет ответа от тимлида.."""
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Reply.objects.filter(author=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
