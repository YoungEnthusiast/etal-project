# Generated by Django 3.2.4 on 2022-09-20 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_task_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='poster',
        ),
    ]
