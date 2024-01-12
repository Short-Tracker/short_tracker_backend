from rest_framework import serializers

from message.models import Reply, Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    message = MessageSerializer()

    class Meta:
        model = Reply
        fields = '__all__'


