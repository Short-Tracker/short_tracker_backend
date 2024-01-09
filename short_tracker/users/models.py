from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователей"""

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя',
        validators=[
            RegexValidator(
                regex=r'^[а-яА-Я\-]{2,30}\Z',
                message='Только кирилица и дефис'
            )],
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='Фамилия',
        validators=[
            RegexValidator(
                regex=r'^[а-яА-Я\-]{2,30}\Z',
                message='Только кирилица и дефис'
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
        verbose_name='Электронная    почта',
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$',
                message='email содержит недопустимый символ'
            )],
    )
    is_team_lead = models.BooleanField(
        default=False,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
