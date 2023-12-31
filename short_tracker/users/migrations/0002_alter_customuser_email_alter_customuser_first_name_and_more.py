# Generated by Django 4.2.8 on 2023-12-25 13:43

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator(message='email содержит недопустимый символ', regex='^((?!\\.)[\\w\\-_.]*[^.])(@\\w+)(\\.\\w+(\\.\\w+)?[^.\\W])$')], verbose_name='Электронная    почта'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Только кирилица и дефис', regex='^[а-яА-Я\\-]{2,30}\\Z')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_team_lead',
            field=models.BooleanField(default=False, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Только кирилица и дефис', regex='^[а-яА-Я\\-]{2,30}\\Z')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
