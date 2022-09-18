# Generated by Django 3.2.7 on 2022-09-18 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20220918_0838'),
        ('chat', '0002_remove_chatnotification_collab'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatnotification',
            name='collab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_notification_collab', to='account.collab'),
        ),
    ]
