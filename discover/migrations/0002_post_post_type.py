# Generated by Django 3.2.4 on 2022-10-08 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discover', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('Anyone', 'Anyone'), ('Affiliation', 'Affiliation')], default='Anyone', max_length=11, null=True),
        ),
    ]