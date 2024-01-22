# Generated by Django 4.2.8 on 2024-01-22 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('message', '0001_initial'),
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to=settings.AUTH_USER_MODEL, verbose_name='Автор ответа'),
        ),
        migrations.AddField(
            model_name='reply',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='message.message', verbose_name='Сообщение'),
        ),
        migrations.AddField(
            model_name='message',
            name='message_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message', to='message.messagestatus', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
        migrations.AddField(
            model_name='message',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='tasks.task', verbose_name='Задача'),
        ),
        migrations.AddIndex(
            model_name='reply',
            index=models.Index(fields=['reply_date'], name='message_rep_reply_d_b8f97c_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['message_date'], name='message_mes_message_b45720_idx'),
        ),
    ]
