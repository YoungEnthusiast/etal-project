# Generated by Django 3.2.4 on 2022-11-07 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_remove_collab_collaborators_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collab',
            name='funding',
        ),
    ]
