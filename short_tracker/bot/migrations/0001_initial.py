# Generated by Django 4.2.8 on 2024-02-12 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Название уведомления"
                    ),
                ),
            ],
            options={
                "verbose_name": "Уведомление",
                "verbose_name_plural": "Уведолмления",
            },
        ),
        migrations.CreateModel(
            name="AllowNotification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "allow_notification",
                    models.BooleanField(verbose_name="Разрешить уведомления"),
                ),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="allow",
                        to="bot.notification",
                        verbose_name="Уведомление",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="allow",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Разрешения уведомлений",
                "verbose_name_plural": "Разрешения уведомлений",
            },
        ),
    ]