from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ROLES = {
    'lead': 'lead',
    'employee': 'employee',
}


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель пользователей"""

    REQUIRED_FIELDS = [
        'first_name', 'last_name',
        'telegram_nickname', 'is_team_lead'
    ]
    USERNAME_FIELD = 'email'

    objects = UserManager()

    username = None
    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя',
        validators=[
            RegexValidator(
                regex=r'^[а-яА-Я\-]{2,30}\Z',
                message='Только кирилица и дефис'
            )
        ],
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='Фамилия',
        validators=[
            RegexValidator(
                regex=r'^[а-яА-Я\-]{2,30}\Z',
                message='Только кирилица и дефис'
            )
        ],
    )
    telegram_nickname = models.CharField(
        max_length=33,
        verbose_name='Никнейм Телеграм',
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^@[a-zA-Z0-9_]{5,33}\Z',
                message='nickname содержит недопустимый символ'
            )
        ],
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Электронная почта',
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$',
                message='email содержит недопустимый символ'
            )
        ],
    )
    is_team_lead = models.BooleanField(
        default=False,
        verbose_name='Роль',
    )
    photo = models.ImageField(
        upload_to='profile_photo/',
        null=True,
        blank=True,
        default=None
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_lead(self):
        return self.is_team_lead
