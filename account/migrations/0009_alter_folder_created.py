# Generated by Django 3.2.4 on 2022-10-17 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20221017_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
