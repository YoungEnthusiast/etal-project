# Generated by Django 3.2.4 on 2022-10-20 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_remove_task_updated_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='text_editor',
        ),
        migrations.RemoveField(
            model_name='task',
            name='update_text',
        ),
        migrations.CreateModel(
            name='TextUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='update_text',
            field=models.ManyToManyField(blank=True, related_name='update_text', to='account.TextUpdate', verbose_name='Description'),
        ),
    ]
