# Generated by Django 3.2.4 on 2022-08-27 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_collab_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='collab',
            name='is_locked',
            field=models.BooleanField(default=False, max_length=5),
        ),
    ]
