# Generated by Django 4.2.8 on 2024-02-19 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_alter_allownotification_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allownotification',
            name='notification',
            field=models.CharField(choices=[('msg', 'Сообщения'), ('tasks', 'Задачи'), ('deadline', 'Дедлайн'), ('status', 'Статусы')], max_length=10, verbose_name='Уведомление'),
        ),
    ]
