# Generated by Django 3.2.4 on 2022-09-26 14:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendarapp', '0009_auto_20220925_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_selected',
            field=models.ManyToManyField(blank=True, related_name='is_selected_event', to=settings.AUTH_USER_MODEL),
        ),
    ]
