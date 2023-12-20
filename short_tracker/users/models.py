from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователей"""

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    username = models.CharField(
        max_length=150,
        verbose_name='Ник пользователя',
        unique=True,
        # db_index=True, Если True, для этого поля будет созданиндексбазыданных
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='username содержит недопустимый символ'
            )],
    )
    telegram_nickname = models.CharField(
        max_length=150,
        verbose_name='Никнейм Телеграм',
        validators=[
            RegexValidator(
                regex=r'^@[a-zA-Z0-9_]{5,32}\Z',
                message='nickname содержит недопустимый символ'
            )],
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Электронная почта',
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    is_team_lead = models.BooleanField(
        default=False,
        verbose_name='Статус',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
