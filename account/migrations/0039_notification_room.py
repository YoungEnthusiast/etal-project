# Generated by Django 3.2.7 on 2022-09-10 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0038_auto_20220909_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='room',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
