# Generated by Django 3.2.4 on 2022-09-28 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchnote', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchnote',
            name='is_pinned',
            field=models.BooleanField(default=False, max_length=5),
        ),
    ]
