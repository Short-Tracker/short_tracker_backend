from django.contrib.auth import get_user_model
from rest_framework import serializers
from message.models import Reply, Message

from api.v1.serializers import ShortUserSerializer

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    recipient = serializers.SerializerMethodField()

    def get_recipient(self, obj):
        queryset = User.objects.filter(is_team_lead=True)
        serializer_data = ShortUserSerializer(queryset, many=True)
        return serializer_data.data

    class Meta:
        model = Message
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    message = MessageSerializer()

    class Meta:
        model = Reply
        fields = '__all__'
