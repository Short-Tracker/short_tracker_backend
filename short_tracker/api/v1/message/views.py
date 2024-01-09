from rest_framework.viewsets import ModelViewSet
from .serializers import AnswerSerializer, QuestionSerializer
from message.models import Answer, Question


class QuestionViewSet(ModelViewSet):
    """Вьюсет запрос к тимлиду."""
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(sender=1)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class AnswerViewSet(ModelViewSet):
    """Вьюсет ответа от тимлида.."""
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Answer.objects.filter(author=1)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
