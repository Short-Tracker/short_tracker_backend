# Generated by Django 4.2.8 on 2024-02-12 14:37

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Только кирилица и дефис', regex='^[а-яА-Я\\-]{2,30}\\Z')], verbose_name='Имя')),
                ('last_name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Только кирилица и дефис', regex='^[а-яА-Я\\-]{2,30}\\Z')], verbose_name='Фамилия')),
                ('telegram_nickname', models.CharField(max_length=33, unique=True, validators=[django.core.validators.RegexValidator(message='nickname содержит недопустимый символ', regex='^@[a-zA-Z0-9_]{5,33}\\Z')], verbose_name='Никнейм Телеграм')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator(message='email содержит недопустимый символ', regex='^((?!\\.)[\\w\\-_.]*[^.])(@\\w+)(\\.\\w+(\\.\\w+)?[^.\\W])$')], verbose_name='Электронная почта')),
                ('is_team_lead', models.BooleanField(default=False, verbose_name='Роль')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('id',),
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]
