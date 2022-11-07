# Generated by Django 3.2.4 on 2022-11-07 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='current_bill',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Funding'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='last_payment',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscription_ends',
            field=models.DateField(blank=True, null=True),
        ),
    ]