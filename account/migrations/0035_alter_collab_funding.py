# Generated by Django 3.2.4 on 2022-11-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_collab_funding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collab',
            name='funding',
            field=models.CharField(choices=[('Institution Internal Funding', 'Institution Internal Funding'), ('External Funding', 'External Funding'), ('No funding', 'No funding')], default='No funding', max_length=100, null=True, verbose_name='Funding'),
        ),
    ]