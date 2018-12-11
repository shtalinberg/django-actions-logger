# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actionslog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logaction',
            name='session_key',
            field=models.CharField(max_length=40, null=True, verbose_name='session key', blank=True),
        ),
        migrations.AlterField(
            model_name='logaction',
            name='action',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='action', blank=True),
        ),
        migrations.AlterField(
            model_name='logaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at', db_index=True),
        ),
    ]
