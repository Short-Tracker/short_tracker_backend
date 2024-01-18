from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from api.v1.tasks.serializers import TaskShowSerializer
from api.v1.message.serializers import MessageSerializer, ReplySerializer


User = get_user_model()


class BotSerializer(ModelSerializer):
    messages = MessageSerializer(many=True)
    reply = ReplySerializer(many=True)
    performers = TaskShowSerializer(many=True)

    class Meta:
        model = User
        fields = ['messages', 'reply', 'performers']


