# Generated by Django 3.2.7 on 2022-09-16 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_chatnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcher',
            name='envelope_unreads',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ChatNotification',
        ),
    ]