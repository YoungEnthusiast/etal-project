# Generated by Django 3.2.4 on 2022-09-20 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20220919_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='poster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poster_task', to=settings.AUTH_USER_MODEL),
        ),
    ]
