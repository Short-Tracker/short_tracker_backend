# Generated by Django 4.2.8 on 2023-12-28 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_email_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, verbose_name='никнейм'),
        ),
    ]