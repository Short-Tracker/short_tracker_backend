# Generated by Django 4.2.8 on 2024-02-20 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_tasks_task_create__81ab0d_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='done_date',
            field=models.DateTimeField(auto_now_add=True, help_text='The done date of the task', null=True, verbose_name='done date'),
        ),
    ]
