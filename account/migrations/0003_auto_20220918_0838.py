# Generated by Django 3.2.7 on 2022-09-18 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20220918_0836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collaborators_type', models.CharField(choices=[('Anyone', 'Anyone'), ('Affiliation', 'Affiliation')], default='Anyone', max_length=11, null=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('abstract', models.TextField(max_length=2000, null=True)),
                ('proposed_timeline', models.CharField(max_length=255, null=True, verbose_name='Proposed Timeline')),
                ('education', models.CharField(choices=[('Bachelor (BSc.)', 'Bachelor (BSc.)'), ('Masters (MSc.)', 'Masters (MSc.)'), ('Doctorate (PhD)', 'Doctorate (PhD)')], max_length=15, null=True)),
                ('field', models.CharField(max_length=255, null=True)),
                ('expertise_required', models.CharField(max_length=255, null=True, verbose_name='Expertise Required')),
                ('on_premises', models.CharField(max_length=255, null=True, verbose_name='On Premises')),
                ('funding', models.CharField(max_length=255, null=True)),
                ('collaborators_no', models.CharField(max_length=255, null=True, verbose_name='Number of Collaborators')),
                ('ownership', models.CharField(max_length=255, null=True, verbose_name='Research Ownership')),
                ('interest', models.BooleanField(default=False, max_length=5)),
                ('is_locked', models.BooleanField(default=False, max_length=5)),
                ('locked_date', models.DateTimeField(blank=True, null=True)),
                ('accepted_date', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collaborators', models.ManyToManyField(blank=True, related_name='collaborator', to=settings.AUTH_USER_MODEL, verbose_name='My Selection')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Stranger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_username', models.EmailField(max_length=255, verbose_name='Enter institution email address')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('status', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Stopped', 'Stopped')], default='Ongoing', max_length=9, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ManyToManyField(blank=True, related_name='assigned_to', to=settings.AUTH_USER_MODEL)),
                ('collab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collab_task', to='account.collab')),
                ('is_selected', models.ManyToManyField(blank=True, related_name='is_selected_task', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'ordering': ('serial',),
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_reported', models.BooleanField(default=False, max_length=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='researcher_collab', to='account.collab')),
                ('complainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_complainer', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('unreads', models.PositiveIntegerField(default=0)),
                ('room', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_collab', to='account.collab')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_flagged', models.BooleanField(default=False, max_length=5)),
                ('reason', models.CharField(blank=True, max_length=255, null=True, verbose_name='flag_reason')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flag_collab', to='account.collab')),
                ('complainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flag_complainer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='CollabDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('document', models.FileField(upload_to='collab_documents/', verbose_name='File')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collab_collab_doc', to='account.collab')),
                ('doc_collaborators', models.ManyToManyField(blank=True, related_name='doc_collaborators', to=settings.AUTH_USER_MODEL)),
                ('is_selected', models.ManyToManyField(blank=True, related_name='is_selected', to=settings.AUTH_USER_MODEL)),
                ('shared_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='collab',
            name='flag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flag_collab', to='account.flag'),
        ),
        migrations.AddField(
            model_name='collab',
            name='interested_people',
            field=models.ManyToManyField(blank=True, related_name='interested_people', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collab',
            name='removed_people',
            field=models.ManyToManyField(blank=True, related_name='removed_people', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collab',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collab_report', to='account.report'),
        ),
        migrations.AddField(
            model_name='collab',
            name='request_removed_people',
            field=models.ManyToManyField(blank=True, related_name='request_removed_people', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collab',
            name='researcher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='researcher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=2000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collab_chat', to='account.collab')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
