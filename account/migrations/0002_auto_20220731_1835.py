# Generated by Django 3.2.4 on 2022-07-31 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcher',
            name='affiliation_address',
            field=models.CharField(max_length=255, null=True, verbose_name='Affiliation Address'),
        ),
        migrations.AddField(
            model_name='researcher',
            name='affiliation_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Affiliation Name'),
        ),
        migrations.AddField(
            model_name='researcher',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='researcher',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='researcher',
            name='state',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='researcher',
            name='type',
            field=models.CharField(choices=[('Researcher', 'Researcher'), ('Collaborator', 'Collaborator'), ('Admin', 'Admin'), ('SuperAdmin', 'SuperAdmin')], default='Researcher', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='researcher',
            name='first_name',
            field=models.CharField(max_length=45, null=True, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='researcher',
            name='last_name',
            field=models.CharField(max_length=45, null=True, verbose_name='Last Name'),
        ),
    ]
