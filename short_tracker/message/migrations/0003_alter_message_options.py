# Generated by Django 4.2.8 on 2024-02-13 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-message_date'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
    ]
