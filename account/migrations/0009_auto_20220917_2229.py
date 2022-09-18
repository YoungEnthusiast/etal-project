# Generated by Django 3.2.7 on 2022-09-17 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_task_is_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Assigned To'),
        ),
        migrations.RemoveField(
            model_name='task',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(blank=True, related_name='assigned_to', to=settings.AUTH_USER_MODEL),
        ),
    ]