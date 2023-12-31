# Generated by Django 4.2.8 on 2023-12-23 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='The description of the task', max_length=100, verbose_name='description')),
                ('comment', models.TextField(blank=True, help_text='The comment of the task', max_length=100, verbose_name='comment')),
                ('link', models.URLField(blank=True, help_text='The link of the task', max_length=100, verbose_name='link')),
                ('status', models.CharField(choices=[('to do', 'to do'), ('in progress', 'in progress'), ('done', 'done'), ('archived', 'archived'), ('hold', 'hold')], default='to do', help_text='The status of the task', max_length=15, verbose_name='status')),
                ('start_date', models.DateField(auto_now_add=True, help_text='The start date of the task', verbose_name='start date')),
                ('inprogress_date', models.DateField(blank=True, help_text='The "in progress" date of the task', verbose_name='"in progress" date')),
                ('finish_date', models.DateField(blank=True, help_text='The finish date of the task', verbose_name='finish date')),
                ('deadline_date', models.DateField(help_text='The deadline date of the task', verbose_name='deadline date')),
                ('archive_date', models.DateField(blank=True, help_text='The archive date of the task', verbose_name='archive date')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
                'ordering': ('-start_date',),
            },
        ),
    ]
