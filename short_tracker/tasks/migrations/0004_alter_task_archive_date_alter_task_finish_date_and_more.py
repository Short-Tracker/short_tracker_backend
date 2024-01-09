# Generated by Django 4.2.8 on 2023-12-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_archive_date_alter_task_finish_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='archive_date',
            field=models.DateField(blank=True, help_text='The archive date of the task', null=True, verbose_name='archive date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='finish_date',
            field=models.DateField(blank=True, help_text='The finish date of the task', null=True, verbose_name='finish date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='inprogress_date',
            field=models.DateField(blank=True, help_text='The "in progress" date of the task', null=True, verbose_name='"in progress" date'),
        ),
    ]
