# Generated by Django 4.2.8 on 2024-02-20 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_alter_allownotification_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allownotification',
            name='notification',
            field=models.CharField(choices=[('status', 'Статусы'), ('tasks', 'Задачи'), ('deadline', 'Дедлайн'), ('msg', 'Сообщения')], max_length=10, verbose_name='Уведомление'),
        ),
    ]