# Generated by Django 3.2.4 on 2022-10-19 15:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_task_update_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='text_editor',
            field=models.ManyToManyField(blank=True, related_name='text_editor', to=settings.AUTH_USER_MODEL, verbose_name='Assign'),
        ),
    ]