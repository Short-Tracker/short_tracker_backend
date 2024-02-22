# Generated by Django 4.2.8 on 2024-02-13 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_hold_alter_task_archive_date_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['create_date', 'status', 'deadline_date', 'performer'], name='tasks_task_create__81ab0d_idx'),
        ),
    ]