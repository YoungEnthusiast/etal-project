# Generated by Django 3.2.4 on 2022-09-28 16:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0017_alter_task_serial'),
        ('researchnote', '0005_alter_researchnote_serial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ResearchNote',
            new_name='Note',
        ),
    ]