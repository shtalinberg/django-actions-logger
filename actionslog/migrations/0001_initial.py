# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.BigIntegerField(db_index=True, null=True, verbose_name='object id', blank=True)),
                ('object_pk', models.CharField(db_index=True, max_length=255, null=True, verbose_name='object pk', blank=True)),
                ('object_repr', models.TextField(null=True, verbose_name='object representation', blank=True)),
                ('object_extra_info', jsonfield.fields.JSONField(null=True, verbose_name='object information', blank=True)),
                ('action', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='action', choices=[(100, 'create'), (150, 'view'), (200, 'change'), (300, 'delete')])),
                ('action_info', jsonfield.fields.JSONField(null=True, verbose_name='action information', blank=True)),
                ('changes', models.TextField(verbose_name='change message', blank=True)),
                ('remote_ip', models.GenericIPAddressField(null=True, verbose_name='remote IP', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('content_type', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='content type', blank=True, to='contenttypes.ContentType', null=True)),
                ('user', models.ForeignKey(related_name='actionlogs', on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'log action',
                'verbose_name_plural': 'log actions',
            },
        ),
    ]
