from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

NOTIFICATIONS = {
    ('msg', 'Сообщения'),
    ('tasks', 'Задачи'),
    ('status', 'Статусы'),
    ('deadline', 'Дедлайн'),
}


class AllowNotification(models.Model):
    allow_notification = models.BooleanField(
        'Разрешить уведомления',
        default=True
    )
    notification = models.CharField(
        choices=NOTIFICATIONS,
        max_length=10,
        verbose_name='Уведомление',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='allow'
    )

    class Meta:
        verbose_name = 'Разрешения уведомлений'
        verbose_name_plural = 'Разрешения уведомлений'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'notification'),
                name='unique_notification_for_user'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.notification}'


