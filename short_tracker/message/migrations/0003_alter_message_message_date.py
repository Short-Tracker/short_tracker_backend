# Generated by Django 4.2.8 on 2024-01-31 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("message", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="message_date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата"),
        ),
    ]
