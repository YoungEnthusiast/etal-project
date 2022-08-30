# Generated by Django 3.2.4 on 2022-08-30 09:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_auto_20220830_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collab',
            name='is_left',
        ),
        migrations.RemoveField(
            model_name='collab',
            name='is_removed',
        ),
        migrations.AddField(
            model_name='collab',
            name='removed_people',
            field=models.ManyToManyField(blank=True, related_name='removed_people', to=settings.AUTH_USER_MODEL),
        ),
    ]