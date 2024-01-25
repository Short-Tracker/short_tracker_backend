from django.contrib.auth import get_user_model
from message.models import Message, Reply
from rest_framework import serializers

from api.v1.users.serializers import ShortUserSerializer

User = get_user_model()


class ReplyShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'reply_body', 'reply_date']


class MessageSerializer(serializers.ModelSerializer):
    recipient = serializers.SerializerMethodField()
    reply = ReplyShortSerializer(many=True)

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
