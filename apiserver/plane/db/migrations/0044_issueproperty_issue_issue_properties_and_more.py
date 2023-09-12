# Generated by Django 4.2.3 on 2023-09-12 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0043_auto_20230905_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueProperty',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=255)),
                ('icon', models.CharField(blank=True, max_length=255, null=True)),
                ('color', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('entity', 'entity'), ('text', 'text'), ('number', 'number'), ('checkbox', 'checkbox'), ('select', 'select'), ('multi_select', 'multi_select'), ('date', 'date'), ('relation', 'relation'), ('files', 'files'), ('email', 'email'), ('url', 'url'), ('datetime', 'datetime'), ('option', 'option')])),
                ('is_required', models.BooleanField(default=False)),
                ('sort_order', models.FloatField(default=65535)),
                ('default_value', models.TextField(blank=True, null=True)),
                ('is_shared', models.BooleanField(default=True)),
                ('extra_settings', models.JSONField(blank=True, default=None, null=True)),
                ('unit', models.CharField(blank=True, max_length=100, null=True)),
                ('is_multi', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='db.issueproperty')),
            ],
            options={
                'verbose_name': 'IssueProperty',
                'verbose_name_plural': 'IssueProperties',
                'db_table': 'issue_properties',
                'ordering': ('sort_order',),
            },
        ),
        migrations.AddField(
            model_name='issue',
            name='issue_properties',
            field=models.JSONField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='default_object_settings',
            field=models.JSONField(blank=True, null=True),
        ),

        migrations.CreateModel(
            name='IssuePropertyValue',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('value', models.TextField(blank=True, db_index=True, null=True)),
                ('type', models.CharField(choices=[('text', 'text'), ('uuid', 'uuid')], max_length=10)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_values', to='db.issue')),
                ('issue_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_values', to='db.issueproperty')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_%(class)s', to='db.project')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Last Modified By')),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workspace_%(class)s', to='db.workspace')),
            ],
            options={
                'verbose_name': 'IssuePropertyValue',
                'verbose_name_plural': 'IssuePropertyValues',
                'db_table': 'issue_property_values',
            },
        ),
        migrations.AddField(
            model_name='issueproperty',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_properties', to='db.project'),
        ),
        migrations.AddField(
            model_name='issueproperty',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Last Modified By'),
        ),
        migrations.AddField(
            model_name='issueproperty',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_properties', to='db.workspace'),
        ),
        migrations.AddField(
            model_name='issue',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='db.issueproperty'),
        ),
    ]