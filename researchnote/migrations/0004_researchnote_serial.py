# Generated by Django 3.2.4 on 2022-09-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchnote', '0003_auto_20220928_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchnote',
            name='serial',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
