# Generated by Django 3.2.14 on 2022-09-24 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0004_remove_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
