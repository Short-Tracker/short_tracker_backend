from django.db import models
from users.models import CustomUser
from tasks.models import Task


class Question(models.Model):
    """Модель вопроса по задаче."""

    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Отправитель'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Задача'
    )
    text_question = models.TextField(
        'Текст сообщения'
    )
    date_question = models.DateTimeField(
        'Дата',
        auto_now=True
    )

    def __str__(self):
        return f'Сообщение №{self.pk}  по задаче {self.task}'

    class Meta:
        verbose_name = 'Вопрос по задаче'
        verbose_name_plural = 'Вопросы по задачам'
        indexes = [
            models.Index(fields=['date_question', ])
        ]


class Answer(models.Model):
    """Модель ответа на запрос от исполнителя."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='answer',
        verbose_name='Автор ответа'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer',
        verbose_name='Вопрос'
    )
    text_answer = models.TextField(
        'Текст'
    )
    date_answer = models.DateTimeField(
        'Дата',
        auto_now=True,
    )

    def __str__(self):
        return f'Ответ №{self.pk} на {self.question}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        indexes = [
            models.Index(fields=['date_answer', ])
        ]
