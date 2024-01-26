from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from api.v1.message.serializers import MessageSerializer, ReplySerializer
from api.v1.tasks.serializers import TaskShowSerializer

User = get_user_model()


class BotSerializer(ModelSerializer):
    messages = MessageSerializer(many=True)
    reply = ReplySerializer(many=True)
    tasks_for_user = TaskShowSerializer(many=True)

    class Meta:
        model = User
        fields = ['messages', 'reply', 'tasks_for_user']


