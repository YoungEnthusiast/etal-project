# Generated by Django 3.2.4 on 2022-11-02 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_auto_20221102_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcher',
            name='award2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Award'),
        ),
        migrations.AddField(
            model_name='researcher',
            name='employer_location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Employer's Location"),
        ),
        migrations.AddField(
            model_name='researcher',
            name='employer_name',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name="Employer's Name"),
        ),
        migrations.AddField(
            model_name='researcher',
            name='position',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Position/Rank'),
        ),
        migrations.AddField(
            model_name='researcher',
            name='year_exit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Year Exited'),
        ),
        migrations.AddField(
            model_name='researcher',
            name='year_join',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Year Joined'),
        ),
    ]
