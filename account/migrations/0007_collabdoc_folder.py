# Generated by Django 3.2.4 on 2022-10-15 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_folder_is_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='collabdoc',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collab_collab_folder', to='account.folder'),
        ),
    ]
