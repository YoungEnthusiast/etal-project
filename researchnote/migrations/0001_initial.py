# Generated by Django 3.2.4 on 2022-10-08 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='')),
                ('aims', models.CharField(max_length=255, verbose_name='')),
                ('date_conducted', models.DateTimeField(blank=True, null=True, verbose_name='')),
                ('location', models.CharField(blank=True, max_length=200, null=True, verbose_name='')),
                ('setup', models.CharField(blank=True, max_length=255, null=True, verbose_name='')),
                ('method', models.TextField(blank=True, null=True, verbose_name='')),
                ('result', models.TextField(blank=True, null=True, verbose_name='')),
                ('observations', models.TextField(blank=True, null=True, verbose_name='')),
                ('document', models.FileField(blank=True, null=True, upload_to='research_notes/', verbose_name='File')),
                ('is_pinned', models.BooleanField(blank=True, default=False, max_length=5, null=True)),
                ('serial', models.CharField(blank=True, max_length=4, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collab_research_note', to='account.collab')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='research_note', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]