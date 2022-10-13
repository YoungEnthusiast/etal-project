# Generated by Django 3.2.4 on 2022-10-10 16:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collab',
            name='abstract',
            field=models.TextField(max_length=2000, null=True, verbose_name='Reearch Description'),
        ),
        migrations.AlterField(
            model_name='collab',
            name='collaborators',
            field=models.ManyToManyField(blank=True, default=None, related_name='collaborator', to=settings.AUTH_USER_MODEL, verbose_name='My Selection'),
        ),
        migrations.AlterField(
            model_name='collab',
            name='collaborators_type',
            field=models.CharField(choices=[('Anyone', 'Anyone')], default='Anyone', max_length=11, null=True),
        ),
    ]