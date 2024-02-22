# Generated by Django 4.2.8 on 2024-02-20 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_done_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='done_date',
            field=models.DateTimeField(blank=True, help_text='The done date of the task', null=True, verbose_name='done date'),
        ),
    ]