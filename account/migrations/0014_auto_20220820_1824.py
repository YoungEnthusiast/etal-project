# Generated by Django 3.2.4 on 2022-08-20 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_collab_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collab',
            name='user',
        ),
        migrations.AddField(
            model_name='collab',
            name='researcher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='researcher', to=settings.AUTH_USER_MODEL),
        ),
    ]