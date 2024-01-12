from django.db import models
from users.models import CustomUser
from tasks.models import Task


class Message(models.Model):
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
        verbose_name='Задача',
        null=True,
        blank=True,
    )
    message_body = models.TextField(
        'Текст сообщения'
    )
    message_date = models.DateTimeField(
        'Дата',
        auto_now=True
    )

    def __str__(self):
        return self.message_body

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        indexes = [
            models.Index(fields=['message_date', ])
        ]


class Reply(models.Model):
    """Модель ответа на запрос от исполнителя."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reply',
        verbose_name='Автор ответа'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='reply',
        verbose_name='Cjj,otybt'
    )
    reply_body = models.TextField(
        'Текст'
    )
    reply_date = models.DateTimeField(
        'Дата',
        auto_now=True,
    )

    def __str__(self):
        return self.reply_body

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        indexes = [
            models.Index(fields=['reply_date', ])
        ]
