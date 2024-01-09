from rest_framework import serializers

from message.models import Answer, Question


class QuestionSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(read_only=True)
    team_lead = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_team_lead(self, obj):
        return obj.task.creator.id


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = '__all__'


