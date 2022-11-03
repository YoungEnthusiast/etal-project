# Generated by Django 3.2.4 on 2022-11-02 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_auto_20221102_0819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='researcher',
            old_name='specialzation',
            new_name='specialization',
        ),
        migrations.AddField(
            model_name='researcher',
            name='award',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='researcher',
            name='course',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Course of Study'),
        ),
        migrations.AddField(
            model_name='researcher',
            name='degree',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Class of Degree'),
        ),
        migrations.AddField(
            model_name='researcher',
            name='year',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='Year of Graduation'),
        ),
    ]